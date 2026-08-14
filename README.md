# Athlete Wellness and Performance Monitoring Dashboard

An interactive dashboard for analyzing athlete wellness, training load, injury, illness, and performance data using Python, pandas, and Streamlit.

## Project Overview

The Athlete Wellness and Performance Monitoring Dashboard was developed as a project for CSPB 3112. The goal of the project was to create a functional, interactive application for exploring athlete monitoring data while developing practical skills in data analysis, software development, dashboard design, and documentation.

The project also builds on my previous academic and professional background in Exercise Science and Athletic Training. Before transitioning into software development, I worked in sports medicine where athlete and patient monitoring information helped guide clinical decisions and track wellness and recovery.

This project allowed me to explore the intersection of sports performance, healthcare, and technology while developing a portfolio quality software application.

## Data Source

The dashboard uses an athlete monitoring dataset published through Zenodo and described in the associated research article.

- **Title:** A large-scale multivariate soccer athlete health, performance, and position monitoring dataset
- **Dataset:** https://zenodo.org/records/10033832
- **Research article:** https://www.nature.com/articles/s41597-024-03386-x

## Features

The dashboard provides several ways to explore and compare athlete monitoring data.

### Interactive Filtering

- Select different athlete wellness metrics
- Filter data by player or athlete
- Select a custom date range
- Adjust the time aggregation between daily, weekly, and monthly views
- View filtered data tables directly within the dashboard

### Wellness Monitoring

The dashboard includes several subjective wellness measures:

- Readiness
- Fatigue
- Mood
- Sleep Duration
- Sleep Quality
- Stress
- Soreness

For individual wellness metrics, the dashboard provides summary statistics including:

- Average
- Maximum
- Minimum
- Standard deviation

### Training Load

Training load data can be viewed over time using the same date filtering and time aggregation options.

Summary statistics are also provided for training load, including average, maximum, minimum, and standard deviation.

### Injury and Illness Monitoring

The dashboard includes:

- Injury reports over time
- Most commonly reported illness symptoms

Injury reports can be viewed using the selected time aggregation to make longer time periods easier to interpret.

### Performance Data

Game performance data is summarized using team, offensive, and defensive performance scores.

### Dataset Comparisons

The dashboard includes comparisons between several datasets, including:

- Training load vs. injury reports
- Training load vs. fatigue
- Sleep quality vs. fatigue
- Training load vs. readiness

Because these datasets use different scales, selected comparison charts use normalized values to allow their trends to be compared more effectively.

## Technologies

- **Python**
- **pandas**
- **Streamlit**
- **Git/GitHub**

## Deployment

The application is deployed using Streamlit Community Cloud.

**Live Application:**  
https://athlete-wellness-dashboard.streamlit.app

**GitHub Repository:**  
https://github.com/mongovencm/athlete-wellness-dashboard

## Project Structure

```text
athlete-wellness-dashboard/
│
├── streamlit_app.py
├── explore_data.py
├── requirements.txt
├── README.md
│
├── scripts/
│   ├── clean_game_performance.py
│   ├── clean_illness.py
│   ├── clean_injury.py
│   ├── clean_training_load.py
│   └── clean_wellness.py
│
└── data/
    └── processed/
        ├── game-performance/
        ├── illness/
        ├── injury/
        ├── training-load/
        └── wellness/
```
