import pandas as pd
from pathlib import Path

def clean_game_performance(input_file, output_file):
    df = pd.read_csv(input_file)

    df = df.rename(columns={
        "player_name": "player",
        "timestamp": "date"
    })

    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")

    df = df.sort_values(["player", "date"])

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"Saved cleaned file to {output_file}")

clean_game_performance(
    "data/raw/subjective/game-performance/game-performance.csv",
    "data/processed/game-performance/game-performance.csv"
)