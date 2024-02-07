import pandas as pd
from konlpy.tag import Okt
import re

locations = ['대전 월평동', '대전 대흥동', '대전 은행동', '대전 둔산동', '대구 반원당역', '대구 중앙로역', '대구 명덕역',
             '수원 수원역', '수원 신동', '수원 인계동', '수원 정자동', '수원 행궁동', '부산 서면역', '부산 해운대역']

for i in locations:

    df = pd.read_csv('../crawling_data/reviews_{}_cafe.csv'.format(i))
    df.info()

    df_stopwords = pd.read_csv('./stopwords.csv')
    stopwords = list(df_stopwords['stopword'])

    okt = Okt()
    cleaned_sentences = []
    for review in df.reviews:
        review = re.sub('[^가-힣]', ' ', review)
        tokened_review = okt.pos(review, stem=True)
        df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
        df_token = df_token[(df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                if word not in stopwords:
                    words.append(word)
        cleaned_sentence = ' '.join(words)
        cleaned_sentences.append(cleaned_sentence)
    df['reviews'] = cleaned_sentences
    df.dropna(inplace=True)
    df.to_csv('./cleaned_{}_reviews.csv'.format(i), index=False)
    df.info()