import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 1]
    return recmovieList[1:11]

df_reviews = pd.read_csv('./cleaned_reviews_cafe_jm.csv')
Tfidf_metrix = mmread('./models/Tfidf_cafe_review').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

#영화 index 이용
# ref_idx = 10
# print(df_reviews.iloc[ref_idx, 0])
# cosine_sim = linear_kernel(Tfidf_metrix[ref_idx], Tfidf_metrix)
# print(cosine_sim[0])
# print(len(cosine_sim))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

#keyword 이용
embedding_model = Word2Vec.load('./models/word2vec_cafe_review.model')
keyword = '라떼'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = [keyword]
for word, _ in sim_word:
    words.append(word)
sentence = []
count = 10
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)
print(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_metrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)