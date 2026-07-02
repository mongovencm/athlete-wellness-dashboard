import pandas as pd

fatigue_df = pd.read_csv("data/raw/subjective/wellness/fatigue.csv")

print(fatigue_df.head())
print(fatigue_df.info())
print(fatigue_df.columns)

mood_df = pd.read_csv("data/raw/subjective/wellness/mood.csv")

print(mood_df.head())
print(mood_df.info())
print(mood_df.columns)

stress_df = pd.read_csv("data/raw/subjective/wellness/stress.csv")
print(stress_df.head())
print(stress_df.info())
print(stress_df.columns)

soreness_df = pd.read_csv("data/raw/subjective/wellness/soreness.csv")
print(soreness_df.head())
print(soreness_df.info())
print(soreness_df.columns)

readiness_df = pd.read_csv("data/raw/subjective/wellness/readiness.csv")
print(readiness_df.head())
print(readiness_df.info())      
print(readiness_df.columns)

sleep_duration_df = pd.read_csv("data/raw/subjective/wellness/sleep_duration.csv")
print(sleep_duration_df.head()) 
print(sleep_duration_df.info())
print(sleep_duration_df.columns)

sleep_quality_df = pd.read_csv("data/raw/subjective/wellness/sleep_quality.csv")
print(sleep_quality_df.head())
print(sleep_quality_df.info())
print(sleep_quality_df.columns)

injury_df = pd.read_csv("data/raw/subjective/injury/injury.csv")

print(injury_df.head())
print(injury_df.info())
print(injury_df.columns)

illness_df = pd.read_csv("data/raw/subjective/illness/illness.csv")

print(illness_df.head())
print(illness_df.info())
print(illness_df.columns)

game_performance_df = pd.read_csv("data/raw/subjective/game-performance/game-performance.csv")
print(game_performance_df.head())
print(game_performance_df.info())
print(game_performance_df.columns)  


