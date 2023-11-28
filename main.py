import os

import pandas as pd

import filewriters as fw
import macrofunctions as maf
import microfunctions as mif
import sql_database as sd

mif.fastf1.plotting.setup_mpl()


def deleteall():
    """
    Deletes all csv-files in the given directory
    """
    bestanden = os.listdir(projectroot())
    csv_bestanden = [bestand for bestand in bestanden if bestand.endswith('.csv')]
    for csv_bestand in csv_bestanden:
        bestand_pad = os.path.join(projectroot(), csv_bestand)
        os.remove(bestand_pad)
        print(f'{csv_bestand} is verwijderd.')
    print('Alle CSV-bestanden zijn verwijderd.')


def deleteunnecessary():
    # TODO: move deletions to this function
    pass


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
    circuit_info = session.get_circuit_info() # VRAAG: is dit een kaart?
    try:
        fw.writecsv('ci_cornerinfo', circuit_info.corners)
        fw.writecsv('ci_marshallights', circuit_info.marshal_lights)
        fw.writecsv('ci_marshalsectors', circuit_info.marshal_sectors)
    except TypeError as te:
        print(f'\x1b[31mTypeError: {te}\x1b[0m')


def writeallseason(year, sprinttype):
    """
    TODO: BESCHRIJVING
    - Laps
    - Cars
    - Weather
    """
    fw.writecsv(f'schedule_{year}', mif.loadschedule(year))
    schedule = pd.read_csv(f'schedule_{year}.csv')
    bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('schedule_')]
    [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]

    if os.path.exists(os.path.join(projectroot(), f'master_cardata-{sprinttype}.csv')) == True:
        print(f'master_cardata-{sprinttype}.csv exists')
        high_car = True
    else:
        high_car = False
    if os.path.exists(os.path.join(projectroot(), f'master_lapdata-{sprinttype}.csv')) == True:
        print(f'master_lapdata-{sprinttype}.csv exists')
        high_lap = True
    else:
        high_lap = False
    if os.path.exists(os.path.join(projectroot(), f'master_weather-{sprinttype}.csv')) == True:
        print(f'master_weather-{sprinttype}.csv exists')
        high_weather = True
    else:
        high_weather = False

    # Exits function if masterdata already exists
    if high_car == high_lap == high_weather == True:
        print(f'\n\n\nSkipping {sprinttype} | {year}')
        return None

    if os.path.exists(os.path.join(projectroot(), f'macro_cardata_{year}-{sprinttype}.csv')) == True:
        print(f'macro_cardata_{year}-{sprinttype}.csv exists')
        medium_car = True
    else:
        medium_car = False
    if os.path.exists(os.path.join(projectroot(), f'macro_lapdata_{year}-{sprinttype}.csv')) == True:
        print(f'macro_lapdata_{year}-{sprinttype}.csv exists')
        medium_lap = True
    else:
        medium_lap = False
    if os.path.exists(os.path.join(projectroot(), f'macro_weatherdata_{year}-{sprinttype}.csv')) == True:
        print(f'macro_weatherdata_{year}-{sprinttype}.csv exists')
        medium_weather = True
    else:
        medium_weather = False

    if medium_car == medium_lap == medium_weather == True:
        return None

    for track in schedule.EventName:
        # TODO: skip session load when file already exists
        low_car = low_lap = low_weather = False

        if os.path.exists(os.path.join(projectroot(), f'micro_cardata_{year}_{track}-{sprinttype}.csv')) == True:
            print(f'micro_cardata_{year}_{track}-{sprinttype}.csv exists')
            low_car = True
        else:
            low_car = False
        if os.path.exists(os.path.join(projectroot(), f'micro_lapdata_{year}_{track}-{sprinttype}.csv')) == True:
            print(f'micro_lapdata_{year}_{track}-{sprinttype}.csv exists')
            low_lap = True
        else:
            low_lap = False
        if os.path.exists(os.path.join(projectroot(), f'micro_weatherdata_{year}_{track}-{sprinttype}.csv')) == True:
            print(f'micro_weatherdata_{year}-{sprinttype}.csv exists')
            low_weather = True
        else:
            low_weather = False

        try:
            # TODO: Check conditionals for file hierarchies
            if low_car == medium_car == False or low_lap == medium_car == False or low_weather == medium_car == False:
                session = mif.loadsession(year, track, sprinttype)
                if low_car == medium_car == False:
                    fw.writecsv(f'micro_cardata_{year}_{track}-{sprinttype}', maf.allcardata(track, year, session, sprinttype))
                    print('cardata retrieved')
                if low_lap == medium_car == False:
                    fw.writecsv(f'micro_lapdata_{year}_{track}-{sprinttype}', maf.alllapdata(track, year, session, sprinttype))
                    print('lapdata retrieved')
                if low_weather == medium_car == False:
                    fw.writecsv(f'micro_weatherdata_{year}_{track}-{sprinttype}', maf.allweatherdata(track, year, session, sprinttype))
                    print('weatherdata retrieved')
        except AttributeError as ae:
            print(f'\x1b[31m{ae}\x1b[0m')
        except KeyError as ke:
            print(f'\x1b[31m{ke}\x1b[0m')

    try:
        # TODO: Check conditionals for file hierarchies
        if medium_car == False:
            print('\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('micro_cardata')]
            fw.writecsv(f'macro_cardata_{year}-{sprinttype}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('cardata written...')
            if deletefiles:
                [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')
    try:
        if medium_lap == False:
            print('\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('micro_lapdata')]
            fw.writecsv(f'macro_lapdata_{year}-{sprinttype}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('lapdata written...')
            if deletefiles == True:
                [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')
    try:
        if medium_weather == False:
            print('\nData is being written, it will take a while...')
            bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('micro_weatherdata')]
            fw.writecsv(f'macro_weatherdata_{year}-{sprinttype}', pd.concat([pd.read_csv(bestand) for bestand in bestanden]).drop_duplicates())
            print('weatherdata written...')
            if deletefiles == True:
                [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]
    except UnboundLocalError as ule:
        print(f'\x1b[31m{ule}\x1b[0m')
    except ValueError as ve:
        print(f'\x1b[31m{ve}\x1b[0m')

    print("Season written")


def circuitdict():
    thisdict = {
        'jack': 4098,
        'sape': 4139,
        'kaas': 'Fromage'
    }
    return thisdict


def projectroot():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # TODO: Write files to dedicated maps
    _macrodatamap = os.path.join(projectroot(), 'Data/Macrodata/')
    _microdatamap = os.path.join(projectroot(), 'Data/Microdata/')
    
    yearschedule = 2023
    sprinttype = ['FP1', 'FP2', 'FP3', 'Q', 'R']
    sprinttype.reverse()

    # deleteall() # Deletes all csv files, ONLY USE FOR DATA RENEWAL AS THIS RENEWAL PROCESS TAKES A CONIDERABLE AMOUNT OF TIME
    global deletefiles
    deletefiles = True # This deletes temporary csv-files that are used to aggregate to masterdatasets

    # SCHEDULES
    try:
        pd.read_csv(f'master_schedule.csv')
        print(f'master_schedule.csv exists')
    except FileNotFoundError as fnfe:
        while yearschedule >= 1950:
            try:
                pd.read_csv(f'schedule_{yearschedule}.csv')
                print(f'schedule_{yearschedule}.csv exists')
                yearschedule -= 1
            except FileNotFoundError as fnfe:
                print(f'Writing Schedule\t{yearschedule}')
                fw.writecsv(f'schedule_{yearschedule}', mif.loadschedule(yearschedule))
                yearschedule -= 1
        fw.writecsv('master_schedule', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('schedule')]).drop_duplicates())
        try:
            if deletefiles == True:
                bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('schedule')]
                [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]
        except UnboundLocalError as ule:
            print(f'\x1b[31m{ule}\x1b[0m')
        except ValueError as ve:
            print(f'\x1b[31m{ve}\x1b[0m')

    # WARNING: Hard limit for data is 2018
    for sessiontype in sprinttype:
        yearsession = 2023
        while yearsession >= 2018:
            print(f'\nSeason {sessiontype} {yearsession}')
            writeallseason(yearsession, sessiontype)
            yearsession -= 1
    
        # Iterative filereading and bulkwrite to one
        try:
            print(f'\n\nData is being aggregated...')
            fw.writecsv(f'master_cardata-{sessiontype}', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(projectroot()) if bestand.endswith(f'{sessiontype}.csv') and bestand.startswith(f'macro_cardata')]).drop_duplicates())
            fw.writecsv(f'master_lapdata-{sessiontype}', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(projectroot()) if bestand.endswith(f'{sessiontype}.csv') and bestand.startswith(f'macro_lapdata')]).drop_duplicates())
            fw.writecsv(f'master_weather-{sessiontype}', pd.concat([pd.read_csv(bestand) for bestand in os.listdir(projectroot()) if bestand.endswith(f'{sessiontype}.csv') and bestand.startswith(f'macro_weatherdata')]).drop_duplicates())
            try:
                if deletefiles == True:
                    bestanden = [bestand for bestand in os.listdir(projectroot()) if bestand.endswith('.csv') and bestand.startswith('macro_')]
                    [os.remove(os.path.join(projectroot(), bestand)) for bestand in bestanden]
            except UnboundLocalError as ule:
                print(f'\x1b[31m{ule}\x1b[0m')
            except ValueError as ve:
                print(f'\x1b[31m{ve}\x1b[0m')
        except:
            pass


    # TODO: SESSION.POS_DATA
    pass

    # deleteall()

# l.fastf1.Cache.clear_cache()
