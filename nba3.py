import pandas as pd

def calculate_weighted_scores(team_name):
    file_name = f"{team_name}_2024_games.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"{file_name} bulunamadı!")
        return

    df.rename(columns={df.columns[5]: 'homeaway'}, inplace=True)
    df['homeaway'] = df['homeaway'].astype(str)

    for col in ['Tm', 'Opp']:
        df[col] = pd.to_numeric(df[col], errors='coerce')  
    df = df.dropna(subset=['Tm', 'Opp'])  

    last_5_games = df.tail(5).copy()

    weights = [0.1, 0.1, 0.2, 0.3, 0.3]
    weighted_home_scores = (last_5_games['Tm'] * weights[:len(last_5_games)]).sum()
    weighted_opponent_scores = (last_5_games['Opp'] * weights[:len(last_5_games)]).sum()

    home_games = df[df['homeaway'] != '@'].copy()
    away_games = df[df['homeaway'] == '@'].copy()

    home_games['Tm'] = pd.to_numeric(home_games['Tm'], errors='coerce')
    away_games['Tm'] = pd.to_numeric(away_games['Tm'], errors='coerce')
    home_games['Opp'] = pd.to_numeric(home_games['Opp'], errors='coerce')
    away_games['Opp'] = pd.to_numeric(away_games['Opp'], errors='coerce')

    home_games = home_games.dropna(subset=['Tm', 'Opp'])
    away_games = away_games.dropna(subset=['Tm', 'Opp'])

    expected_home_score = weighted_home_scores * 0.6 + weighted_opponent_scores * 0.4
    expected_away_score = away_games['Tm'].mean() * 0.4 + home_games['Opp'].mean() * 0.6
    expected_total_basket = expected_home_score * 0.6 + expected_away_score * 0.4

 
    print(f"{team_name} için beklenen ev sahibi toplam basket değeri:", expected_home_score)
    print(f"{team_name} için beklenen deplasman toplam basket değeri:", expected_away_score)
    print(f"Maç için beklenen toplam basket değeri:", expected_total_basket)
    print("----")

team_1 = input("Birinci takımın adını girin (örneğin: LAL): ")
team_2 = input("İkinci takımın adını girin (örneğin: BOS): ")

calculate_weighted_scores(team_1)
calculate_weighted_scores(team_2)
