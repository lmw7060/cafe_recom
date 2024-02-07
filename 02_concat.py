import pandas as pd
import glob


data_paths = glob.glob('./naver_seoul_data/*')
print(data_paths)

df = pd.DataFrame()

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.columns = ['area', 'titles', 'reviews']
    df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)

df.drop_duplicates(inplace=True, subset='titles')
df.info()
df.to_csv('./naver_cafe_jm.csv', index=False)