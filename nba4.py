import pandas as pd

def calculate_weighted_scores(team_name):
    file_name = f"{team_name}_2024_games.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"{file_name} bulunamadı!")
        return None 
    except Exception as e:
        print(f"Dosya okuma sırasında bir hata oluştu: {e}")
        return None

    df.rename(columns={df.columns[5]: 'homeaway'}, inplace=True)
    df['homeaway'] = df['homeaway'].astype(str)

    for col in ['Tm', 'Opp']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Tm', 'Opp'])

    home_games = df[df['homeaway'] != '@'].copy()
    away_games = df[df['homeaway'] == '@'].copy()

    home_games['Tm'] = pd.to_numeric(home_games['Tm'], errors='coerce')
    away_games['Tm'] = pd.to_numeric(away_games['Tm'], errors='coerce')
    home_games['Opp'] = pd.to_numeric(home_games['Opp'], errors='coerce')
    away_games['Opp'] = pd.to_numeric(away_games['Opp'], errors='coerce')

    home_games = home_games.dropna(subset=['Tm', 'Opp'])
    away_games = away_games.dropna(subset=['Tm', 'Opp'])

    expected_home_score = home_games['Tm'].mean() * 0.6 + away_games['Opp'].mean() * 0.4
    expected_away_score = away_games['Tm'].mean() * 0.4 + home_games['Opp'].mean() * 0.6

    return expected_home_score, expected_away_score

team_1 = input("Birinci takımın adını girin (örneğin: LAL): ")
team_2 = input("İkinci takımın adını girin (örneğin: BOS): ")

home_scores = calculate_weighted_scores(team_1)
away_scores = calculate_weighted_scores(team_2)

if home_scores and away_scores:
    home_expected, _ = home_scores
    _, away_expected = away_scores

    total_basket = home_expected + away_expected
    print(f"{team_1} (ev sahibi) vs {team_2} (deplasman) maçında beklenen toplam basket sayısı: {total_basket:.2f}")
else:
    print("Hesaplama sırasında bir hata oluştu.")
