import requests
from bs4 import BeautifulSoup
import pandas as pd

team_url_name = "GSW"  
season = 2024          

url = f"https://www.basketball-reference.com/teams/{team_url_name}/{season}_games.html"

response = requests.get(url)
if response.status_code != 200:
    print("Sayfa yüklenemedi!")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", {"id": "games"})
if table is None:
    print("Maç tablosu bulunamadı!")
    exit()

headers = [th.text for th in table.find("thead").find_all("th")]
rows = table.find("tbody").find_all("tr")

data = []
for row in rows:
    cells = row.find_all(["th", "td"])
    data.append([cell.text.strip() for cell in cells])

df = pd.DataFrame(data, columns=headers)


output_file = f"{team_url_name}_{season}_games.csv"
df.to_csv(output_file, index=False)
print(f"Deplasman maçları '{output_file}' dosyasına kaydedildi.")
