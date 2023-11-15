from time import perf_counter

import fastf1
import fastf1.plotting
import pandas as pd

import filewriters as fw
import macrofunctions as maf
import microfunctions as mif

def writetocsv(carname, cardata, lapname, lapdata, weathername, weatherdata):
    fw.writecsv(carname, cardata)
    fw.writecsv(lapname, lapdata)
    fw.writecsv(weathername, weatherdata)


def writealldata(year, sessiontype, combinedcar=[], combinedlap=[], combinedweather=[]):
    schedule = mif.loadschedule(year)
    fw.writecsv(f'schedule_{year}', schedule)
    for event in schedule.OfficialEventName:
        session = mif.loadsession(year, event, sessiontype)
        # CAR DATA
        try:
            content = pd.read_csv(f'cardata_{year}.csv')
            content.shape
            content.info()
            print(f'cardata_{year}.csv exists')
        except FileNotFoundError as fnfe:
            starttijdcar = perf_counter()
            print(f'\x1b[32mGetting Car Telemetry Data... {event}')
            cardata = maf.allcardata(event, year, session)
            combinedcar.append(cardata.drop_duplicates())
            # TODO VRAAG: Data voegt zichzelf toe zonder append?
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdcar) * 1000:.0f}ms")
            pass
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")

        # LAP DATA
        try:
            content = pd.read_csv(f'lapdata_{year}.csv')
            content.shape
            content.info()
            print(f'lapdata_{year}.csv exists')
        except FileNotFoundError as fnfe:
            starttijdlap = perf_counter()
            print(f'\x1b[32mGetting Lap Data... {event}')
            lapdata = maf.alllapdata(event, year, session)
            combinedlap.append(lapdata.drop_duplicates())
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdlap) * 1000:.0f}ms")
            if lapdata.empty:
                pass
            else:
                combinedlap.append(lapdata)
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")

        # WEATHER DATA
        try:
            contentweather = pd.read_csv(f'weatherdata_{year}.csv')
            contentweather.shape
            contentweather.info()
            print(f'weatherdata_{year}.csv exists')
        except FileNotFoundError as fnfe:
            starttijdweather = perf_counter()
            print(f'\x1b[32mGetting Weather Data... {event}')
            weatherdata = maf.allweatherdata(event, year, session)
            combinedweather.append(weatherdata.drop_duplicates())
            # TODO VRAAG: Data voegt zichzelf toe zonder append?
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdweather) * 1000:.0f}ms")
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")
    writetocsv(f'cardata_{year}', cardata, f'lapdata_{year}', lapdata, f'weatherdata_{year}', weatherdata)
