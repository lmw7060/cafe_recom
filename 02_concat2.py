import pandas as pd
import glob

locations = ['홍대입구역', '합정역', '망원역', '상수역',
             '신촌역', '용산역', '삼각지역', '이태원역',
             '녹사평역', '신용산역', '이촌역', '남영역',
             '효창공원앞역', '공덕역', '숙대입구역', '서울역',
             '강남역', '교대역', '양재역', '서초역',
             '대전 월평동', '대전 대흥동', '대전 은행동', '대전 둔산동',
             '대구 반원당역', '대구 중앙로역', '대구 명덕역', '부산 서면역',
             '부산 해운대역', '수원 수원역', '수원 신동', '수원 인계동',
             '수원 정자동', '수원 행궁동', '인사동', '명동', '회기동', '돈암동', '혜화동']
for i in locations:
    data_paths = glob.glob('./data_naver/naver_data_{}_*.csv'.format(i))
    print(data_paths)

    df = pd.DataFrame()

    for path in data_paths:
        df_temp = pd.read_csv(path)
        df_temp.columns = ['titles', 'reviews']
        df_temp.insert(loc=0, column='area', value=i)
        df_temp.dropna(inplace=True)
        df = pd.concat([df, df_temp], ignore_index=True)

        df.drop_duplicates(inplace=True)
        df.info()
        df.to_csv('./naver_seoul_{}_cafe_jm.csv'.format(i), index=False)