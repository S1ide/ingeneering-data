import json
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

file_paths = ["resources/[1]game_logs.csv", "resources/[3]flights.csv", "resources/CIS_Automotive_Kaggle_Sample.csv",
              "resources/dataset.csv", "resources/vacancies_2020.csv"]


def analyze_data(source_dataframe: pd.DataFrame):
    file_size = source_dataframe.memory_usage(deep=True).sum()  # считаем объем, который занимает файл
    memory_usage = source_dataframe.memory_usage(deep=True).sum()  # считаем объем памяти, который занимает набор данных
    col_sizes = []

    for col in source_dataframe.columns:
        col_size = source_dataframe[col].memory_usage(deep=True)  # объем который занимает отдельная колонка
        col_type = source_dataframe[col].dtype  # вычисляем тип данных
        percent = col_size / memory_usage  # доля отдельной колонки от общего объъема памяти
        col_sizes.append({'column': col, 'size': col_size, 'percent': percent, 'type': str(col_type)})

    sorted_df = source_dataframe.loc[:, source_dataframe.dtypes != object]
    sorted_sizes = []

    for col in sorted_df.columns:
        col_size = source_dataframe[col].memory_usage(deep=True)
        col_type = source_dataframe[col].dtype
        percent = col_size / memory_usage
        sorted_sizes.append(
            {'column': col, 'size': col_size, 'percent': percent, 'type': str(col_type)})

    return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


def optimize_data(df):
    converted_data = df.copy()

    for column in converted_data.columns:
        if converted_data[column].dtype == 'object':
            unique_values = converted_data[column].unique()

            if len(unique_values) < 50:
                converted_data[column] = converted_data[column].astype('category')

            if converted_data[column].dtype == 'int64':
                converted_data[column] = converted_data[column].astype(np.int32)
            elif converted_data[column].dtype == 'float64':
                converted_data[column] = converted_data[column].astype(np.float32)

    return converted_data


def compare_memory_usage(source_data, optimized_data):
    source_data_memory = source_data.memory_usage(deep=True).sum()
    optimized_data_memory = optimized_data.memory_usage(deep=True).sum()

    if source_data_memory > optimized_data_memory:
        print("Success optimization diff between src data and optimized data - " + str(
            source_data_memory - optimized_data_memory))
    else:
        print("Fail optimization diff between src data and optimized data - " + str(
            optimized_data_memory - source_data_memory))


def read_data(file_path, columns):
    df = pd.concat(
        pd.read_csv(file_path, chunksize=10000, usecols=columns, low_memory=False, index_col=False),
        ignore_index=True
    )
    return df


def plot_linear(data, x, y, name):
    plt.title(name)
    sns.lineplot(data=data.sample(1000), x=x, y=y, errorbar=None)
    plt.savefig(f'results/{name}.png')
    plt.close()


def plot_step(data, x, y, name):
    plt.title(name)
    sns.stripplot(data=data.sample(1000), x=x, y=y, dodge=True)
    plt.savefig(f'results/{name}.png')
    plt.close()


def plot_boxplot(df, x, y, name):
    sns.boxplot(data=df.sample(1000), x=x, y=y)
    plt.savefig(f'results/{name}.png')
    plt.close()


def plot_histogram(df, x, y, name):
    sns.histplot(data=df.sample(1000), x=x, y=y)
    plt.savefig(f'results/{name}.png')
    plt.close()


def create_plots(df, index):
    if index == 1:
        plot_linear(df, "v_score", "h_score", f"df_{index}_plot_1")
        plot_linear(df, "v_hits", "v_doubles", f"df_{index}_plot_2")
        plot_linear(df, "v_hits", "v_triples", f"df_{index}_plot_3")
        plot_step(df, "v_homeruns", "v_hits", f"df_{index}_plot_4")
        plot_step(df, "v_homeruns", "v_score", f"df_{index}_plot_5")

    elif index == 2:
        plot_linear(df, "DISTANCE", "AIR_TIME", f"df_{index}_plot_6")
        plot_linear(df, "FLIGHT_NUMBER", "TAXI_IN", f"df_{index}_plot_7")
        plot_histogram(df, "DISTANCE", "TAXI_OUT", f"df_{index}_plot_8")
        plot_histogram(df, "FLIGHT_NUMBER", "TAXI_OUT", f"df_{index}_plot_9")
        plot_histogram(df, "FLIGHT_NUMBER", "AIR_TIME", f"df_{index}_plot_10")

    elif index == 3:
        plot_linear(df, "vf_ForwardCollisionWarning", "vf_EngineCylinders", f"df_{index}_plot_11")
        plot_linear(df, "vf_EngineCylinders", "vf_FuelTypePrimary", f"df_{index}_plot_12")
        plot_step(df, "vf_EngineKW", "vf_FuelTypeSecondary", f"df_{index}_plot_13")
        plot_linear(df, "vf_EngineCylinders", "vf_FuelTypeSecondary", f"df_{index}_plot_14")
        plot_histogram(df, "vf_EngineCylinders", "vf_EngineKW", f"df_{index}_plot_15")

    elif index == 4:
        plot_linear(df, "class", "diameter", f"df_{index}_plot_1")
        plot_step(df, "spkid", "class", f"df_{index}_plot_2")
        plot_histogram(df, "spkid", "diameter", f"df_{index}_plot_3")
        plot_boxplot(df, "class", "albedo", f"df_{index}_plot_4")
        plot_histogram(df, "diameter", "diameter_sigma", f"df_{index}_plot_5")

    elif index == 5:
        plot_linear(df, "id", "salary_to", f"df_{index}_plot_1")
        plot_linear(df, "id", "salary_from", f"df_{index}_plot_2")
        plot_step(df, "schedule_id", "experience_id", f"df_{index}_plot_3")
        plot_boxplot(df, "experience_id", "salary_to", f"df_{index}_plot_4")
        plot_histogram(df, "experience_id", "salary_from", f"df_{index}_plot_5")


def main():
    columns = [
        ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
         "v_homeruns", "v_rbi"],
        ["FLIGHT_NUMBER", "ORIGIN_AIRPORT", "DAY_OF_WEEK", "DESTINATION_AIRPORT", "DISTANCE", "AIR_TIME",
         "TAXI_OUT", "ARRIVAL_DELAY", "AIRLINE", "TAXI_IN"],
        ["vf_Make", "stockNum", "vf_EngineCylinders", "vf_EngineKW", "vf_EngineModel", "vf_EntertainmentSystem",
         "vf_ForwardCollisionWarning", "vf_FuelInjectionType", "vf_FuelTypePrimary", "vf_FuelTypeSecondary"],
        ["name", "spkid", "class", "diameter", "albedo", "diameter_sigma", "epoch", "epoch_cal", "om", "w"],
        ["id", "key_skills", "schedule_name", "experience_id", "experience_name", "salary_from", "salary_to",
         "employer_name", "employer_industries", "schedule_id"],
    ]

    df_list = []

    for i, cols in enumerate(columns, start=0):
        df_list.append(read_data(file_paths[i], cols))

    for i, df in enumerate(df_list):
        result_analyze = analyze_data(df)
        col_sizes = result_analyze['col_sizes']
        with open(f'results/df_results{i}.json', 'a') as f:
            json.dump({f'df{i}_memory_usage': sorted(col_sizes, key=lambda x: x['percent'], reverse=True)}, f)

        optimized_data = optimize_data(df)
        compare_memory_usage(df, optimized_data)
        optimized_data.to_csv(f'optimized_df_{i + 1}.csv')

        create_plots(df, i + 1)


if __name__ == "__main__":
    main()
