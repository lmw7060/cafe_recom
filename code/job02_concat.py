import pandas as pd
import glob

locations = ['대전 월평동', '대전 대흥동', '대전 은행동', '대전 둔산동', '대구 반원당역', '대구 중앙로역', '대구 명덕역',
             '부산 서면역', '부산 해운대역']

for i in locations:
    data_path = glob.glob('../data_naver/naver_data_{}_*.csv'.format(i))

    df = pd.DataFrame()

    for path in data_path:
        df_temp = pd.read_csv(path)
        df_temp.columns = ['names', 'reviews']
        df_temp.insert(loc=0, column='area', value=i)
        df_temp.dropna(inplace=True)
        df = pd.concat([df, df_temp], ignore_index=True)

    df.drop_duplicates(inplace=True)
    df.info()

    df.to_csv('../crawling_data/reviews_{}.csv'.format(i), index=False)
