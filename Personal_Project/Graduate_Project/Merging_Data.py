import pandas as pd
import re
import os

# CSV 파일들이 있는 폴더 경로
folder_path = './Dataset'  # 예: './data'
csv_files = sorted(
    [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')],
    key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group())
)
# 모든 CSV 파일을 읽어오되, source_index를 부여
df_list = []

for idx, file in enumerate(csv_files):
    df = pd.read_csv(file)
    df['source_index'] = idx  # 각 파일에 고유 인덱스 부여
    df_list.append(df)


# 병합
merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv("merged_data.csv")

print(merged_df['source_index'].value_counts().sort_index())
