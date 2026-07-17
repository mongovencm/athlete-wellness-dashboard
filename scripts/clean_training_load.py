import pandas as pd
from pathlib import Path


def clean_training_load(input_folder, output_file):
    input_folder = Path(input_folder)

    # files and output column names
    files = {
        "acwr.csv": "acwr",
        "atl.csv": "atl",
        "ctl28.csv": "ctl28",
        "ctl42.csv": "ctl42",
        "daily_load.csv": "daily_load",
        "weekly_load.csv": "weekly_load",
        "monotony.csv": "monotony",
        "strain.csv": "strain"
    }

    merged_df = None

    for filename, column_name in files.items():
        file_path = input_folder / filename

        print(f"Processing {file_path}")

        # read wide-format CSV
        df = pd.read_csv(file_path)

        # convert date column name
        df = df.rename(columns={"Date": "date"})

        # convert wide format to long format
        df = df.melt(
            id_vars=["date"],
            var_name="athlete",
            value_name=column_name
        )

        # convert dates
        df["date"] = pd.to_datetime(
            df["date"],
            format="%d.%m.%Y"
        )

        # merge each metric dataframe
        if merged_df is None:
            merged_df = df
        else:
            merged_df = merged_df.merge(
                df,
                on=["date", "athlete"],
                how="outer"
            )

    # replace missing values with zeros
    metric_columns = [
        "acwr",
        "atl",
        "ctl28",
        "ctl42",
        "daily_load",
        "weekly_load",
        "monotony",
        "strain"
    ]

    merged_df[metric_columns] = (
        merged_df[metric_columns]
        .fillna(0)
    )

    # remove days where every metric is zero
    merged_df = merged_df[
        (merged_df[metric_columns] != 0).any(axis=1)
    ]

    # sort for dashboard usage
    merged_df = merged_df.sort_values(
        ["athlete", "date"]
    )

    # create output folder if needed
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # save cleaned dataframe
    merged_df.to_csv(
        output_file,
        index=False
    )

    print(f"Saved cleaned file to {output_file}")


clean_training_load(
    "data/raw/subjective/training-load",
    "data/processed/training-load/training-load.csv"
)