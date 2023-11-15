import concurrent.futures
import os
import threading
from time import perf_counter

import pandas as pd

import filewriters as fw
import macrofunctions as maf
import megafunctions as mef
import microfunctions as mif

mif.fastf1.plotting.setup_mpl()


def deleteall():
    """
    TODO: kan ik relatieve paden gebruiken?

    Deletes all csv-files in the given directory
    """
    directory_path = '/Users/delano/Documents/GitHub/Data_Drivers'
    bestanden = os.listdir(directory_path)
    csv_bestanden = [
        bestand for bestand in bestanden if bestand.endswith('.csv')]
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
    - session
    - year

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
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=6)
    pool.submit(fw.writecsv(f'Schedule_{year}', mif.loadschedule(year)))
    pool.submit(maf.writeseasoncardata(year, sprinttype))
    pool.submit(maf.writeseasonlapdata(year, sprinttype))
    pool.submit(maf.writeseasonweatherdata(year, sprinttype))
    pool.shutdown(wait=True)
    print("Done")


if __name__ == "__main__":
    # TODO: Write files to dedicated maps
    project_root_dir = os.path.dirname(os.path.abspath(__file__))
    _datamap = os.path.join(project_root_dir, 'Data/Macrodata/cardata_2022.csv')
    
    year, lstyear = 2023, []
    sprinttype = ['FP1', 'FP2', 'FP3', 'Q', 'R']
    while year >= 2016: # 1950
        print(f'\n\n{year}')
        writeallseason(year, sprinttype[4])
        year -= 1

    # TODO: SESSION.POS_DATA

    # THE WHOLE SEASON
    # writeallseason(year, sprinttype[4])
    pass

    # ALL AVAILABLE FROM 2023-1950
    # mef.writealldata(year, sprinttype[4])
    pass

    # WRITE ONE SESSION
    year, location = 2018, 'monza'
    print("\x1b[32m")
    # session = mif.loadsession(year, location, sprinttype[4])  # Requests the session
    print("\x1b[0m")
    # writeallsingle(session, year)

    # deleteall()

# l.fastf1.Cache.clear_cache()
