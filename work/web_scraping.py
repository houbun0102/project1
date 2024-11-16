import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 目次ページのURL
index_url = "https://indico.belle2.org/category/62/"  # 目次ページのURLを指定

# 検索する文字列
target_text = "Tomoyuki"

# データ保存用のリスト
data = []

# 目次ページからリンクを収集
response = requests.get(index_url)
soup = BeautifulSoup(response.content, "html.parser")

# 目次ページ内のリンクを取得
links = [a.get("href") for a in soup.find_all("a", href=True)]

for link in links:
    try:
        # ページのURLを取得
        page_url = requests.compat.urljoin(index_url, link)
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, "html.parser")

        # ページ内に特定の文字列が存在するか確認
        if target_text in page_soup.get_text():
            data.append({"URL": page_url, "Found Text": target_text})

        # 適宜、サーバーに負担をかけないように待機
        time.sleep(1)

    except Exception as e:
        print(f"Error accessing {page_url}: {e}")

# データをCSVファイルに保存
df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)
print("CSVファイルに保存しました")
