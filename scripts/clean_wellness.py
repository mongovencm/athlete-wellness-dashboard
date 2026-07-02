import pandas as pd
from pathlib import Path


def clean_wellness_csv(input_file, output_file, value_name):
    """
    Clean wellness data CSV files 

    Parameters:
    input_file : str or Path
        Path to the raw CSV file.

    output_file : str or Path
        Path where the cleaned CSV will be saved.

    value_name : str
        Name of the wellness metric
        (e.g. "readiness", "sleep_quality", "soreness").
    """

    # read CSV
    df = pd.read_csv(input_file)

    # rename first column to "date"
    df = df.rename(columns={df.columns[0]: "date"})

    # convert date column
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # convert from wide to long
    df = df.melt(
        id_vars="date",
        var_name="player",
        value_name=value_name
    )

    # remove rows with missing values
    df = df.dropna(subset=[value_name])

    # sort data
    df = df.sort_values(["player", "date"])

    # create output folder if needed
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # save cleaned file
    df.to_csv(output_path, index=False)

    print(f"Saved cleaned data to {output_path}")


if __name__ == "__main__":

    csv_file = "data/raw/subjective/wellness/stress.csv"

    clean_wellness_csv(
        input_file=csv_file,
        output_file="data/processed/wellness/stress.csv",
        value_name="stress"
    )