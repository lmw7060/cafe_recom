import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
from gensim.models import Word2Vec
import pickle
from PyQt5.QtCore import QStringListModel
import webbrowser
from qt_material import apply_stylesheet
from qt_material import list_themes






form_window = uic.loadUiType('./cafe_recommendation.ui')[0]

class Exam(QWidget,form_window):
    def initUi(self):
        self.label.setStyleSheet('background-color: #D2DE32;'
                                 # "border-radius: 15px;"
                                 "border-style: solid;"
                                 "border-width: 3px;"
                                 "border-color: #61A3BA;")

        self.label_2.setStyleSheet('background-color: #D2DE32;'
                                   # "border-radius: 15px;"
                                   "border-style: solid;"
                                   "border-width: 3px;"
                                   "border-color: #61A3BA;")

        self.btn_recommendation.setStyleSheet('background-color: #61A3BA;'
                                              "border-style: solid;"
                                              "border-width: 3px;"
                                              "border-color: #61A3BA;")
        self.le_keyword.setStyleSheet('background-color: #E6E6E6;'
                                              "border-style: solid;"
                                              "border-width: 3px;"
                                              "border-color: #D2DE32;")
        self.comboBox.setStyleSheet('background-color: #FFFFDD;'
                                              "border-style: solid;"
                                              "border-width: 3px;"
                                              "border-color: #D2DE32;")

        self.lbl_recommendation.setStyleSheet('background-color: #FFFFDD;'
                                              "border-style: solid;"
                                              "border-width: 3px;"
                                              "border-color: #D2DE32;")
        # self.lbl_recommendation.setStyleSheet('background-color: #FFA732;'
        #                                       "border-style: solid;"
        #                                       "border-width: 3px;"
        #                                       "border-color: #C21292;")
        # self.label_5.setStyleSheet('background-color: #EF4040;'
        #                          # "border-radius: 15px;"
        #                          "border-style: solid;"
        #                          "border-width: 3px;"
        #                          "border-color: #EF4040;")
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
        self.Tfidf_matrix = mmread('./models/Tfidf_cafe_review.mtx').tocsr()
        # self.Tfidf_matrix2 = mmread('./models2/Tfidf_cafe_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        # with open('./models2/tfidf.pickle', 'rb') as f:
        #     self.Tfidf2 = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_cafe_review.model')
        # self.embedding_model2 = Word2Vec.load('./models2/word2vec_cafe_review.model')
        self.df_reviews = pd.read_csv('cleaned_reviews_cafe_jm.csv')
        # self.df_reviews2 = pd.read_csv('./models2/cleaned_reviews_cafe_jm2.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        # for title in self.titles:
        #     self.comboBox.addItem(title)
        locations = ['지역을 선택하시오', '전체', '홍대입구역', '합정역', '망원역', '상수역',
                     '신촌역', '용산역', '삼각지역', '이태원역',
                     '녹사평역', '신용산역', '이촌역', '남영역',
                     '효창공원앞역', '공덕역', '숙대입구역', '서울역',
                     '강남역', '교대역', '양재역', '서초역',
                     '대전 월평동', '대전 대흥동', '대전 은행동', '대전 둔산동',
                     '대구 반원당역', '대구 중앙로역', '대구 명덕역', '부산 서면역',
                     '부산 해운대역', '수원역', '신동', '인계동',
                     '정자동', '행궁동', '인사동', '명동', '회기동', '돈암동', '혜화동']
        self.areas = locations
        for area in self.areas:
            self.comboBox.addItem(area)

        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)
        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)
        self.label_5.setText("<a href=\"https://map.naver.com/p/\">네이버 지도로 가기</a>")
        self.label_5.setOpenExternalLinks(True)

    def btn_slot(self):
        key_word = self.le_keyword.text()
        if key_word in self.titles:
            recommendation = self.recommendation_by_cafe_title(key_word)
        else:
            recommendation = self.recommendation_by_keyword(key_word)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)

    def combobox_slot(self):
        try:
            area = self.comboBox.currentText()
            recommendation = self.recommendation_by_area(area)
            recommendation = recommendation.split('\n')
            new_list = set(recommendation)
            new_list = list(new_list)
            str = ''
            for data in new_list[:10]:
                print(data)
                str += '\n' + data

            self.lbl_recommendation.setText(str)
        except Exception as e:
            print(e)

    def recommendation_by_area(self, area):
        if area == '지역을 선택하시오':
            self.lbl_recommendation.clear()
            return 0
        else:
            area_idx = self.df_reviews[self.df_reviews['area'] == area].index[2]
            cosine_sim = linear_kernel(self.Tfidf_matrix[area_idx], self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            recommendation = '\n'.join(list(recommendation))
            return recommendation

    def recommendation_by_keyword(self, key_word):
        try:
            sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
        except:
            self.lbl_recommendation.setText('없는 단어다')
            return 0
        words = [key_word]
        for word, _ in sim_word:
            words.append(word)
        sentence = []
        count = 10
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def recommendation_by_cafe_title(self, title):
        cafe_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[cafe_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        select_area = self.comboBox.currentText()
        if select_area == '지역을 선택하시오':
            pass
        elif select_area == '전체':
            simScore = simScore[:11]
            movieIdx = [i[0] for i in simScore]
            recmovieList = self.df_reviews.iloc[movieIdx, 1]
            return recmovieList[0:11]
        else:
            sim_list = []
            for i in simScore:
                area = self.df_reviews.iloc[i[0], 0]
                if area == select_area:
                    sim_list.append(i)
            h_idx = [i[0] for i in sim_list[0:10]]
            if len(h_idx) == 0:
                self.lbl_recommendation.setText('가게가 없다')
                return 0
            else:
                cafelist = self.df_reviews.iloc[h_idx]
                return cafelist.titles
        simScore = simScore[0:11]
        h_idx = [i[0] for i in simScore]
        reccafeList = self.df_reviews.iloc[h_idx, 1]
        return reccafeList[0:11]

    # def getRecommendation2(self, cosine_sim):
    #     simScore = list(enumerate(cosine_sim[-1]))
    #     simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
    #     simScore = simScore[:51]
    #     cafeIdx = [i[0] for i in simScore]
    #     reccafeList = self.df_reviews2.iloc[cafeIdx, 1]
    #     return reccafeList[1:51]

if __name__ =='__main__':
    app =QApplication(sys.argv)
    mainWindow=Exam()
    mainWindow.show()
    sys.exit(app.exec_())

