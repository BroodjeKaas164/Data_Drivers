import json
import pandas as pd


def writecsv(name, data):
    """
    Writes a DataFrame to a csv-file with the given name
    - name (str): the name of the resulted file
    - data (DataFrame): the data which to be transformed into csv-format

    Results:
    - FILE (csv)
    """
    try:
        pd.read_csv(f'{name}.csv')
        print('File already exists')
    except FileNotFoundError as fnfe:
        data.to_csv(f"{name}.csv", index=False)
    except AttributeError as ae:
        print(f'\x1b[31m{ae}\x1b[0m')


def writejson(name, data):
    """
    Source: ChatGPT
    Writes a DataFrame to a json-file with the given name
    - name (str): the name of the resulted file
    - data (DataFrame): the data which to be transformed into json-format

    Results:
    - FILE (json)
    """
    # TODO: schrijf functie zodanig dat volledige data wordt ingeladen
    try:
        pd.read_json(f'{name}.json')
        print('File already exists')
    except FileNotFoundError as fnfe:
        with open(f"{name}.json", "w") as json_file:
            json.dump(list(data), json_file, indent=4)
    except TypeError as te:
        print(f'\x1b[31m{te}\x1b[0m')
