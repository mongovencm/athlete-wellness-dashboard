import streamlit as st
import pandas as pd
import ast
from collections import Counter

st.set_page_config(page_title="Athlete Wellness Dashboard")

st.title("Athlete Wellness Dashboard")
st.write("Interactive dashboard for cleaned athlete wellness data.")

### wellness data

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

Files = {
    "Readiness": "data/processed/wellness/readiness.csv",
    "Fatigue": "data/processed/wellness/fatigue.csv",
    "Mood": "data/processed/wellness/mood.csv",
    "Sleep Duration": "data/processed/wellness/sleep_duration.csv",
    "Sleep Quality": "data/processed/wellness/sleep_quality.csv",
    "Stress": "data/processed/wellness/stress.csv",
    "Soreness": "data/processed/wellness/soreness.csv",
}

Score_ranges = {
    "Readiness": "1-10",
    "Fatigue": "1-5",
    "Mood": "1-5",
    "Sleep Duration": "hours",
    "Sleep Quality": "1-5",
    "Stress": "1-10",
    "Soreness": "1-5",
}

metric = st.sidebar.selectbox(
    "Wellness Metric",
    list(Files.keys())
)

df = load_data(Files[metric])

value_col = df.columns[-1]

players = ["All Players"] + sorted(df["player"].unique())

selected_player = st.sidebar.selectbox(
    "Player",
    players
)

if selected_player != "All Players":
    df = df[df["player"] == selected_player]

start_date = df["date"].min().date()
end_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    (start_date, end_date)
)

if len(date_range) == 2:
    start, end = date_range
    df = df[
        (df["date"] >= pd.Timestamp(start))
        & (df["date"] <= pd.Timestamp(end))
    ]

st.subheader(metric)
st.caption(f"Valid range: {Score_ranges[metric]}")

col1, col2 = st.columns(2)

col1.metric("Average Score", f"{df[value_col].mean():.2f}")
col2.metric("Records", len(df))

daily = (
    df.groupby("date")[value_col]
      .mean()
      .reset_index()
)

st.line_chart(
    daily.set_index("date")
)

st.subheader("Filtered Data")

st.dataframe(df, use_container_width=True)


### game performance data

game_performance_df = pd.read_csv("data/processed/game-performance/game-performance.csv")

st.header("Game Performance Overview")

game_performance_df["date"] = pd.to_datetime(game_performance_df["date"], errors="coerce")

avg_scores = game_performance_df[[
    "team_performance",
    "offensive_performance",
    "defensive_performance"
]].mean()

st.subheader("Average Performance Scores")

st.bar_chart(avg_scores)

### injury data 

injury_df = pd.read_csv("data/processed/injury/injury.csv")

st.header("Injury Reports")

injury_df["date"] = pd.to_datetime(injury_df["date"], errors="coerce")

# group by month
injury_counts = (
    injury_df
    .groupby(injury_df["date"].dt.to_period("M"))
    .size()
    .reset_index(name="count")
)

injury_counts["date"] = injury_counts["date"].astype(str)

st.subheader("Injury Reports Over Time")

st.line_chart(injury_counts.set_index("date"))


### training load data

training_load_df = pd.read_csv(
    "data/processed/training-load/training-load.csv"
)

st.header("Training Load Overview")

training_load_df["date"] = pd.to_datetime(
    training_load_df["date"],
    errors="coerce"
)

# select athlete
athletes = ["All Athletes"] + sorted(
    training_load_df["athlete"].unique()
)

selected_athlete = st.selectbox(
    "Training Load Athlete",
    athletes
)

if selected_athlete != "All Athletes":
    training_load_df = training_load_df[
        training_load_df["athlete"] == selected_athlete
    ]


### training load chart

st.subheader("Daily Training Load")

daily_training = (
    training_load_df
    .groupby("date")["daily_load"]
    .mean()
    .reset_index()
)

st.line_chart(
    daily_training.set_index("date")
)


### training load vs injuries comparison

st.subheader("Training Load vs Injury Reports")

# monthly training load
monthly_load = (
    training_load_df
    .groupby(training_load_df["date"].dt.to_period("M"))["daily_load"]
    .mean()
    .reset_index()
)

monthly_load["date"] = monthly_load["date"].astype(str)


# monthly injury counts
monthly_injuries = (
    injury_df
    .groupby(injury_df["date"].dt.to_period("M"))
    .size()
    .reset_index(name="injury_count")
)

monthly_injuries["date"] = monthly_injuries["date"].astype(str)


# combine datasets
load_injury_compare = monthly_load.merge(
    monthly_injuries,
    on="date",
    how="left"
)

load_injury_compare = load_injury_compare.fillna(0)


st.line_chart(
    load_injury_compare.set_index("date")
)



### illness data

illness_df = pd.read_csv("data/processed/illness/illness.csv")

st.header("Illness Reports")

# ensure clean column names
illness_df.columns = illness_df.columns.str.strip()

all_symptoms = []

for row in illness_df["symptoms"]:
    try:
        symptoms = ast.literal_eval(row)
        all_symptoms.extend(symptoms)
    except:
        pass

symptom_counts = Counter(all_symptoms)

symptom_df = pd.DataFrame(
    symptom_counts.items(),
    columns=["symptom", "count"]
).sort_values("count", ascending=False)

st.subheader("Most Common Symptoms")

st.bar_chart(symptom_df.set_index("symptom"))