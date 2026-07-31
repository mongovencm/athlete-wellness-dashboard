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

time_group = st.sidebar.selectbox(
    "Time Aggregation",
    ["Daily", "Weekly", "Monthly"]
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

default_start = max(
    df["date"].min(),
    df["date"].max() - pd.Timedelta(days=90)
)

date_range = st.sidebar.date_input(
    "Date Range",
    (
        default_start.date(),
        end_date
    )
)



if len(date_range) == 2:
    start, end = date_range
    df = df[
        (df["date"] >= pd.Timestamp(start))
        & (df["date"] <= pd.Timestamp(end))
    ]

st.subheader(metric)
st.caption(f"Valid range: {Score_ranges[metric]}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average",
    f"{df[value_col].mean():.2f}"
)

col2.metric(
    "Maximum",
    f"{df[value_col].max():.2f}"
)

col3.metric(
    "Minimum",
    f"{df[value_col].min():.2f}"
)

col4.metric(
    "Std Dev",
    f"{df[value_col].std():.2f}"
)

if time_group == "Daily":
    graph_df = (
        df.groupby("date")[value_col]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    graph_df = (
        df.groupby(
            pd.Grouper(key="date", freq="W")
        )[value_col]
        .mean()
        .reset_index()
    )

else:
    graph_df = (
        df.groupby(
            pd.Grouper(key="date", freq="ME")
        )[value_col]
        .mean()
        .reset_index()
    )

graph_df["Rolling Average"] = (
    graph_df[value_col]
    .rolling(7)
    .mean()
)

st.line_chart(
    graph_df.set_index("date")
)

with st.expander("Show Filtered Data"):
    st.dataframe(df, use_container_width=True)

### game performance data

game_performance_df = pd.read_csv("data/processed/game-performance/game-performance.csv")

st.header("Game Performance Overview")

game_performance_df["date"] = pd.to_datetime(
    game_performance_df["date"],
    errors="coerce")

game_performance_df = game_performance_df[
    (game_performance_df["date"] >= pd.Timestamp(start))
    &
    (game_performance_df["date"] <= pd.Timestamp(end))
]

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

injury_df["date"] = pd.to_datetime(
    injury_df["date"], 
    errors="coerce")

injury_df = injury_df[
    (injury_df["date"] >= pd.Timestamp(start))
    &
    (injury_df["date"] <= pd.Timestamp(end))
]

if time_group == "Daily":
    injury_counts = (
        injury_df
        .groupby("date")
        .size()
        .reset_index(name="count")
    )

elif time_group == "Weekly":
    injury_counts = (
        injury_df
        .groupby(pd.Grouper(key="date", freq="W"))
        .size()
        .reset_index(name="count")
    )

else:
    injury_counts = (
        injury_df
        .groupby(pd.Grouper(key="date", freq="ME"))
        .size()
        .reset_index(name="count")
    )

st.subheader("Injury Reports Over Time")

st.line_chart(injury_counts.set_index("date"))


### training load data

training_load_df = pd.read_csv(
    "data/processed/training-load/training-load.csv"
)

st.header("Training Load Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Load",
    f"{training_load_df['daily_load'].mean():.0f}"
)

col2.metric(
    "Maximum",
    f"{training_load_df['daily_load'].max():.0f}"
)

col3.metric(
    "Minimum",
    f"{training_load_df['daily_load'].min():.0f}"
)

col4.metric(
    "Std Dev",
    f"{training_load_df['daily_load'].std():.0f}"
)

training_load_df["date"] = pd.to_datetime(
    training_load_df["date"],
    errors="coerce"
)

training_load_df = training_load_df[
    (training_load_df["date"] >= pd.Timestamp(start))
    &
    (training_load_df["date"] <= pd.Timestamp(end))
]

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

if time_group == "Daily":
    daily_training = (
        training_load_df
        .groupby("date")["daily_load"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    daily_training = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="W"))["daily_load"]
        .mean()
        .reset_index()
    )

else:
    daily_training = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="ME"))["daily_load"]
        .mean()
        .reset_index()
    )

st.line_chart(
    daily_training.set_index("date")
)

with st.expander("Show Training Load Data"):
    st.dataframe(
        training_load_df,
        use_container_width=True
    )


### training load vs injuries comparison

st.subheader("Training Load vs Injury Reports")

if time_group == "Daily":
    monthly_load = (
        training_load_df
        .groupby("date")["daily_load"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    monthly_load = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="W"))["daily_load"]
        .mean()
        .reset_index()
    )

else:
    monthly_load = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="ME"))["daily_load"]
        .mean()
        .reset_index()
    )


if time_group == "Daily":
    monthly_injuries = (
        injury_df
        .groupby("date")
        .size()
        .reset_index(name="injury_count")
    )

elif time_group == "Weekly":
    monthly_injuries = (
        injury_df
        .groupby(pd.Grouper(key="date", freq="W"))
        .size()
        .reset_index(name="injury_count")
    )

else:
    monthly_injuries = (
        injury_df
        .groupby(pd.Grouper(key="date", freq="ME"))
        .size()
        .reset_index(name="injury_count")
    )

# combine datasets
load_injury_compare = monthly_load.merge(
    monthly_injuries,
    on="date",
    how="left"
)

load_injury_compare = load_injury_compare.fillna(0)


compare = load_injury_compare.copy()

compare["daily_load"] = (
    compare["daily_load"]
    - compare["daily_load"].min()
) / (
    compare["daily_load"].max()
    - compare["daily_load"].min()
)

compare["injury_count"] = (
    compare["injury_count"]
    - compare["injury_count"].min()
) / (
    compare["injury_count"].max()
    - compare["injury_count"].min()
)

st.line_chart(
    compare.set_index("date")
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



### training load vs wellness comparison

st.header("Wellness vs Training Load")

fatigue_df = pd.read_csv(
    "data/processed/wellness/fatigue.csv"
)

fatigue_df["date"] = pd.to_datetime(fatigue_df["date"])

fatigue_df = fatigue_df[
    (fatigue_df["date"] >= pd.Timestamp(start))
    &
    (fatigue_df["date"] <= pd.Timestamp(end))
]

if time_group == "Daily":
    daily_fatigue = (
        fatigue_df
        .groupby("date")["fatigue"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    daily_fatigue = (
        fatigue_df
        .groupby(pd.Grouper(key="date", freq="W"))["fatigue"]
        .mean()
        .reset_index()
    )

else:
    daily_fatigue = (
        fatigue_df
        .groupby(pd.Grouper(key="date", freq="ME"))["fatigue"]
        .mean()
        .reset_index()
    )

if time_group == "Daily":
    daily_load = (
        training_load_df
        .groupby("date")["daily_load"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    daily_load = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="W"))["daily_load"]
        .mean()
        .reset_index()
    )

else:
    daily_load = (
        training_load_df
        .groupby(pd.Grouper(key="date", freq="ME"))["daily_load"]
        .mean()
        .reset_index()
    )

fatigue_compare = daily_load.merge(
    daily_fatigue,
    on="date",
    how="inner"
)

st.subheader("Average Fatigue vs Daily Training Load")

st.caption(
    "Weekly average fatigue scores compared with average daily training load."
)

compare = fatigue_compare.copy()

compare["daily_load"] = (
    compare["daily_load"]
    - compare["daily_load"].min()
) / (
    compare["daily_load"].max()
    - compare["daily_load"].min()
)

compare["fatigue"] = (
    compare["fatigue"]
    - compare["fatigue"].min()
) / (
    compare["fatigue"].max()
    - compare["fatigue"].min()
)

st.line_chart(
    compare.set_index("date")
)



### sleep quality vs fatigue comparison
sleep_df = pd.read_csv(
    "data/processed/wellness/sleep_quality.csv"
)

sleep_df["date"] = pd.to_datetime(sleep_df["date"])

sleep_df = sleep_df[
    (sleep_df["date"] >= pd.Timestamp(start))
    &
    (sleep_df["date"] <= pd.Timestamp(end))
]

if time_group == "Daily":
    sleep_daily = (
        sleep_df
        .groupby("date")["sleep_quality"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    sleep_daily = (
        sleep_df
        .groupby(pd.Grouper(key="date", freq="W"))["sleep_quality"]
        .mean()
        .reset_index()
    )

else:
    sleep_daily = (
        sleep_df
        .groupby(pd.Grouper(key="date", freq="ME"))["sleep_quality"]
        .mean()
        .reset_index()
    )


if time_group == "Daily":
    fatigue_daily = (
        fatigue_df
        .groupby("date")["fatigue"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    fatigue_daily = (
        fatigue_df
        .groupby(pd.Grouper(key="date", freq="W"))["fatigue"]
        .mean()
        .reset_index()
    )

else:
    fatigue_daily = (
        fatigue_df
        .groupby(pd.Grouper(key="date", freq="ME"))["fatigue"]
        .mean()
        .reset_index()
    )


sleep_compare = sleep_daily.merge(
    fatigue_daily,
    on="date",
    how="inner"
)

sleep_compare["Sleep Quality Trend"] = (
    sleep_compare["sleep_quality"]
    .rolling(4)
    .mean()
)

sleep_compare["Fatigue Trend"] = (
    sleep_compare["fatigue"]
    .rolling(4)
    .mean()
)

st.subheader("Average Sleep Quality vs Fatigue")

st.caption(
    "Weekly averages comparing sleep quality and fatigue with four-week trend lines."
)

st.line_chart(
    sleep_compare.set_index("date")
)


### readiness vs training load comparison

readiness_df = pd.read_csv(
    "data/processed/wellness/readiness.csv"
)

readiness_df["date"] = pd.to_datetime(readiness_df["date"])

readiness_df = readiness_df[
    (readiness_df["date"] >= pd.Timestamp(start))
    &
    (readiness_df["date"] <= pd.Timestamp(end))
]

if time_group == "Daily":
    daily_readiness = (
        readiness_df
        .groupby("date")["readiness"]
        .mean()
        .reset_index()
    )

elif time_group == "Weekly":
    daily_readiness = (
        readiness_df
        .groupby(pd.Grouper(key="date", freq="W"))["readiness"]
        .mean()
        .reset_index()
    )

else:
    daily_readiness = (
        readiness_df
        .groupby(pd.Grouper(key="date", freq="ME"))["readiness"]
        .mean()
        .reset_index()
    )

readiness_compare = daily_load.merge(
    daily_readiness,
    on="date",
    how="inner"
)

readiness_compare["Readiness Trend"] = (
    readiness_compare["readiness"]
    .rolling(4)
    .mean()
)

readiness_compare["Training Trend"] = (
    readiness_compare["daily_load"]
    .rolling(4)
    .mean()
)

st.subheader("Average Readiness vs Daily Training Load")

st.caption(
    "Weekly averages comparing athlete readiness with training load over time."
)

st.line_chart(
    readiness_compare.set_index("date")
)
