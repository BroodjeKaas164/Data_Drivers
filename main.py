import os
import threading
from time import perf_counter

import pandas as pd

import filewriters as fw
import macrofunctions as maf
import microfunctions as mif

mif.fastf1.plotting.setup_mpl()


def deleteall():
    """
    TODO: kan ik relatieve paden gebruiken?

    Deletes all csv-files in the given directory
    """
    directory_path = '/Users/delano/Documents/GitHub/Data_Drivers'
    bestanden = os.listdir(directory_path)
    csv_bestanden = [bestand for bestand in bestanden if bestand.endswith('.csv')]
    for csv_bestand in csv_bestanden:
        bestand_pad = os.path.join(directory_path, csv_bestand)
        os.remove(bestand_pad)
        print(f'{csv_bestand} is verwijderd.')
    print('Alle CSV-bestanden zijn verwijderd.')


def circuit_info(session):
    """
    Requests all available information regarding a circuit via FastF1.

    Args:
    - session
    
    Result
    - CSV-file: Containing cornerinfo.
    - CSV-File: Containing marshallights.
    - CSV-File: Containing marshal sectors.
    """
    circuit_info = session.get_circuit_info()  # VRAAG: is dit een kaart?
    try:
        fw.writecsv('ci_cornerinfo', circuit_info.corners)
        fw.writecsv('ci_marshallights', circuit_info.marshal_lights)
        fw.writecsv('ci_marshalsectors', circuit_info.marshal_sectors)
    except TypeError as te:
        print(f'\x1b[31mTypeError: {te}\x1b[0m')


def writeallsingle(session, year):
    """
    Schrijft alles gedefinieerd naar csv.

    Args
    - session (DataFrame)
    - year (int/str)

    Result
    - CSV-bestanden van alles gedefinieerd, waaronder telemetries; etc.
    """
    fw.writecsv(f'schedule_{year}', mif.loadschedule(year))  # Writes the schedule of the given year
    circuit_info(session) # Writes available circuit information containing cornering; marshals.
    fw.writecsv("lapdata", maf.alllapdata(year, session)) # Writes all available lap data of the requested session
    fw.writecsv("cardata", maf.allcardata(year, session)) # Writes all available car data of the requested session
    fw.writecsv('remaining_sessions', mif.loadremaining()) # Writes the remaining sessions of the season
    fw.writecsv('weather_data', session.weather_data)  # Writes weather data
    fw.writecsv('track_status', session.track_status) # Writes track status which contains green; yellow flags; safety cars
    fw.writecsv('session_results', session.results) # writes session results


def writeallseason(year, sprinttype):
    """
    TODO: BESCHRIJVING
    - Laps
    - Cars
    - Weather
    """
    """
    fw.writecsv(f'cardata_{year}', pd.concat([maf.writeseasoncardata(track, mif.loadsession(year, track, sprinttype), year, sprinttype) for track in mif.loadschedule(year).OfficialEventName if mif.loadsession(year, track, sprinttype).session_info['Meeting']['OfficialName'] == track]))
    fw.writecsv(f'lapdata_{year}', pd.concat([maf.writeseasonlapdata(track, mif.loadsession(year, track, sprinttype), year, sprinttype) for track in mif.loadschedule(year).OfficialEventName if mif.loadsession(year, track, sprinttype).session_info['Meeting']['OfficialName'] == track]))
    fw.writecsv(f'weatherdata_{year}', pd.concat([maf.writeseasonweatherdata(track, mif.loadsession(year, track, sprinttype), year, sprinttype) for track in mif.loadschedule(year).OfficialEventName if mif.loadsession(year, track, sprinttype).session_info['Meeting']['OfficialName'] == track]))
    """
    schedule = pd.read_csv(f'schedule_{year}.csv')
    high_car = high_lap = high_weather = False
    try:
        pd.read_csv(f'cardata_{year}.csv')
        print(f'cardata_{year}.csv')
        high_car = True
    except FileNotFoundError as fnfe:
        high_car = False
    try:
        pd.read_csv(f'lapdata_{year}.csv')
        print(f'lapdata_{year}.csv exists')
        high_lap = True
    except FileNotFoundError as fnfe:
        high_lap = False
    try:
        pd.read_csv(f'weatherdata_{year}.csv')
        print(f'weatherdata_{year}.csv exists')
        high_weather = True
    except FileNotFoundError as fnfe:
        high_weather = False
    
    for track in schedule.OfficialEventName:
        low_car = low_lap = low_weather = medium_car = medium_lap = medium_weather = False
        session = mif.loadsession(year, track, sprinttype)

        try:
            pd.read_csv(f'macro_cardata_{year}.csv')
            print(f'macro_cardata_{year}.csv exists')
            medium_car = True
        except FileNotFoundError as fnfe:
            medium_car = False
        try:
            pd.read_csv(f'macro_lapdata_{year}.csv')
            print(f'macro_lapdata_{year}.csv exists')
            medium_lap = True
        except FileNotFoundError as fnfe:
            medium_lap = False
        try:
            pd.read_csv(f'macro_weatherdata_{year}.csv')
            print(f'macro_weatherdata_{year}.csv exists')
            medium_weather = True
        except FileNotFoundError as fnfe:
            medium_weather = False

        try:
            pd.read_csv(f'micro_cardata_{year}_{track}.csv')
            print(f'micro_cardata_{year}.csv exists')
            low_car = True
        except FileNotFoundError as fnfe:
            low_car = False
        try:
            pd.read_csv(f'micro_lapdata_{year}_{track}.csv')
            print(f'micro_lapdata_{year}.csv exists')
            low_lap = True
        except FileNotFoundError as fnfe:
            low_lap = False
        try:
            pd.read_csv(f'micro_weatherdata_{year}_{track}.csv')
            print(f'micro_weatherdata_{year}.csv exists')
            low_weather = True
        except FileNotFoundError as fnfe:
            low_weather = False

        try:
            if low_car == medium_car == high_car == False:
                fw.writecsv(f'micro_cardata_{year}_{track}', maf.allcardata(track, year, session, sprinttype))
                print('cardata retrieved')
            if low_lap == medium_car == high_lap == False:
                fw.writecsv(f'micro_lapdata_{year}_{track}', maf.alllapdata(track, year, session, sprinttype))
                print('lapdata retrieved')
            if low_weather == medium_car == high_weather == False:
                fw.writecsv(f'micro_weatherdata_{year}_{track}', maf.allweatherdata(track, year, session, sprinttype))
                print('weatherdata retrieved')
        except AttributeError as ae:
            print(f'\x1b[31m{ae}\x1b[0m')
        except KeyError as ke:
            print(f'\x1b[31m{ke}\x1b[0m')

    deletefiles = True
    try:
        if medium_car == False:
            print('\n\n\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('micro_cardata')]
            fw.writecsv(f'macro_cardata_{year}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('cardata written...')
            if deletefiles:
                for bestand in bestanden:
                    os.remove(os.path.join(project_root_dir, bestand))
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')
    try:
        if medium_lap == False:
            print('\n\n\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('micro_lapdata')]
            fw.writecsv(f'macro_lapdata_{year}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('lapdata written...')
            if deletefiles == True:
                for bestand in bestanden:
                    os.remove(os.path.join(project_root_dir, bestand))
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')
    try:
        if medium_weather == False:
            print('\n\n\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('micro_weatherdata')]
            fw.writecsv(f'macro_weatherdata_{year}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('weatherdata written...')
            if deletefiles == True:
                for bestand in bestanden:
                    os.remove(os.path.join(project_root_dir, bestand))
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')

    print("Season written")


if __name__ == "__main__":
    # TODO: Write files to dedicated maps
    project_root_dir = os.path.dirname(os.path.abspath(__file__))
    _macrodatamap = os.path.join(project_root_dir, 'Data/Macrodata/')
    _microdatamap = os.path.join(project_root_dir, 'Data/Microdata/')
    
    yearsession, yearschedule, lstyear = 2023, 2023, []
    sprinttype = ['FP1', 'FP2', 'FP3', 'Q', 'R']

    # deleteall() # Deletes all csv files, ONLY USE FOR DATA RENEWAL AS THIS PROCESS TAKES A CONIDERABLE AMOUNT OF TIME

    # SCHEDULES
    while yearschedule >= 1950:
        try:
            pd.read_csv(f'schedule_{yearschedule}.csv')
            print(f'schedule_{yearschedule}.csv exists')
            yearschedule -= 1
        except FileNotFoundError as fnfe:
            print(f'Writing Schedule\t{yearschedule}')
            fw.writecsv(f'schedule_{yearschedule}', mif.loadschedule(yearschedule))
            yearschedule -= 1

    # WARNING: Hard limit for data is 2018
    while yearsession >= 2018: # 1950
        print(f'\nWriting Session\t{yearsession}')
        writeallseason(yearsession, sprinttype[4])
        yearsession -= 1

    # Iterative reading per file and bulkwrite to one
    starttijd = perf_counter()
    try:
        fw.writecsv('master_cardata', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('macro_cardata')]).drop_duplicates())
        fw.writecsv('master_lapdata', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('macro_lapdata')]).drop_duplicates())
        fw.writecsv('master_weather', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('macro_weatherdata')]).drop_duplicates())
        fw.writecsv('master_schedule', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(project_root_dir) if bestand.endswith('.csv') and bestand.startswith('schedule')]).drop_duplicates())
    except:
        pass
    print(f"Tijd: \x1b[31m{(perf_counter() - starttijd) * 1000:.0f}ms")

    # TODO: SESSION.POS_DATA
    pass

    # deleteall()

# l.fastf1.Cache.clear_cache()
