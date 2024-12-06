import requests
from bs4 import BeautifulSoup
import pandas as pd

# Takım ve sezon bilgisi
team_url_name = "GSW"  # Los Angeles Lakers için örnek
season = 2024          # Sezonu belirtin
input_file = f"{team_url_name}_{season}_games.csv"  # Örnek dosya adı

# Basketball Reference URL'si
df = pd.read_csv(input_file)

# 6. sütunu 'homeaway' olarak adlandırma
df.rename(columns={df.columns[5]: 'homeaway'}, inplace=True)

# 'homeaway' sütununu string tipine dönüştürme
df['homeaway'] = df['homeaway'].astype(str)

# 'homeaway' sütununda '@' işareti olup olmadığını kontrol etme
away_games = df[df['homeaway'].str.contains('@', na=False)]

# Sonuçları CSV olarak kaydetme
output_file = f"{team_url_name}_{season}_away_games.csv"
away_games.to_csv(output_file, index=False)
print(f"Deplasman maçları '{output_file}' dosyasına kaydedildi.")