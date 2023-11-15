from time import perf_counter

import pandas as pd

import filewriters as fw
import microfunctions as mif


def cacheall(year, sprinttype):
    """
    TODO: BESCHRIJVING
    """
    schedule = mif.loadschedule(year)
    for name in schedule.OfficialEventName:
        print("\x1b[32m")
        mif.loadsession(year, name, sprinttype)
        print("\x1b[0m")


def allcardata(name, year, session, combinedcardata=[]):
    """
    # TODO: Beschrijving
    """
    try:
        for driver in session.drivers:
            lap = 1
            while lap <= session.total_laps:
                try:
                    lstdriver, lstyear, lstname, x = [], [], [], 1
                    df = session.laps.pick_driver(driver).pick_lap(int(lap)).get_car_data()
                    while x <= df.Brake.size:
                        lstdriver.append(driver)
                        lstyear.append(year)
                        lstname.append(name)
                        x += 1
                    df["driverID"] = lstdriver
                    df['year'] = lstyear
                    df['gp'] = lstname
                    combinedcardata.append(df)
                except KeyError as ke:
                    print(f"\x1b[31m{ke}\x1b[0m")
                except ValueError as ve:
                    print(f"\x1b[31m{ve}\x1b[0m")
                lap += 1
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    return pd.concat(combinedcardata)


def seasoncardata(year, sessiontype, eventiter=0):
    """
    TODO: BESCHRIJVING
    """
    schedule = mif.loadschedule(year)
    for eventcar in schedule.OfficialEventName:
        print(f'\n\n{eventiter}')
        try:
            contentcar = pd.read_csv(f'cardata_{year}.csv')
            contentcar.shape
            contentcar.info()
            print(f'cardata_{year}.csv exists')
            break
        except FileNotFoundError as fnfe:
            starttijdcar = perf_counter()
            print(f'\x1b[32mGetting Car Telemetry Data... {eventcar}')
            cardata = allcardata(eventcar, year, mif.loadsession(year, eventcar, sessiontype))
            # TODO VRAAG: Data voegt zichzelf toe zonder append?
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdcar) * 1000:.0f}ms")
            eventiter += 1
            pass
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")
    try:
        return cardata
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
        return None


def writeseasoncardata(year, sprinttype):
    """
    Extension to function above which should be called if cardata has to be written.
    """
    try:
        fw.writecsv(f'cardata_{year}', seasoncardata(year, sprinttype).drop_duplicates())
        print(f"Season {year} Car Data written!")
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")


def alllapdata(name, year, session, lap=1, combinedlapdata=[]):
    """
    # TODO: Beschrijving
    """
    try:
        while lap <= session.total_laps:
            
            try:
                lstyear, lstname, x = [], [], 1
                lapinfo = mif.loadlap(session, lap)
                while x <= lapinfo.DriverNumber.size:
                    lstyear.append(year)
                    lstname.append(name)
                    x += 1
                lapinfo['year'] = lstyear
                lapinfo['gp'] = lstname
            except KeyError as ke:
                print(f"\x1b[31m{ke}\x1b[0m")
            except ValueError as ve:
                print(f"\x1b[31m{ve}\x1b[0m")
            combinedlapdata.append(lapinfo)
            lap += 1
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    return pd.concat(combinedlapdata)


def seasonlapdata(year, sessiontype, eventiter=0, combinedlap=[]):
    schedule = mif.loadschedule(year)
    for eventlap in schedule.OfficialEventName:
        print(f'\n\n{eventiter}')
        try:
            contentlap = pd.read_csv(f'lapdata_{year}.csv')
            contentlap.shape
            contentlap.info()
            print(f'lapdata_{year}.csv exists')
            break
        except FileNotFoundError as fnfe:
            starttijdlap = perf_counter()
            print(f'\x1b[32mGetting Lap Data... {eventlap}')
            lapdata = alllapdata(eventlap, year, mif.loadsession(year, eventlap, sessiontype))
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdlap) * 1000:.0f}ms")
            if lapdata.empty:
                pass
            else:
                combinedlap.append(lapdata)
            eventiter += 1
            # print(f'\x1b[0m{lapdata}')
            pass
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")
    """
    TODO: Ik krijg hier dubbele data terug doordat ik 'lapdata' toevoeg aan een lijst (2023).
    Hoe zorg ik ervoor dat ik dit niet krijg zonder dat lapdata 'None' wordt door
    de laatste races?
    """
    try:
        if combinedlap != []:
            return pd.concat(combinedlap)
        elif lapdata.empty:
            return None
        else:
            return lapdata
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
        return None


def writeseasonlapdata(year, sprinttype):
    """
    Extension to function above which should be called if lapdata has to be written.
    """
    try:
        fw.writecsv(f'lapdata_{year}', seasonlapdata(year, sprinttype).drop_duplicates())
        print(f"Season {year} Lap Data written!")
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")



def allweatherdata(name, year, session, combinedweatherdata=[]):
    try:
        for driver in session.drivers:
            lap = 1
            while lap <= session.total_laps:
                try:
                    lstdriver, lstyear, lstlap, lstname, x = [], [], [], [], 1
                    df = session.laps.pick_driver(driver).pick_lap(int(lap)).get_weather_data()
                    # TODO: Krijg af en toe lege dataframes terug?
                    while x <= df.AirTemp.size:
                        lstdriver.append(driver)
                        lstyear.append(year)
                        lstlap.append(lap)
                        lstname.append(name)
                        x += 1
                    df["driverID"] = lstdriver
                    df['year'] = lstyear
                    df['lap'] = lstlap
                    df['gp'] = lstname
                    combinedweatherdata.append(df)
                except KeyError as ke:
                    print(f"\x1b[31m{ke}\x1b[0m")
                except ValueError as ve:
                    print(f"\x1b[31m{ve}\x1b[0m")
                lap += 1
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    return pd.concat(combinedweatherdata)


def seasonweatherdata(year, sessiontype, eventiter=0):
    schedule = mif.loadschedule(year)
    for eventweather in schedule.OfficialEventName:
        print(f'\n\n{eventiter}')
        try:
            contentweather = pd.read_csv(f'weatherdata_{year}.csv')
            contentweather.shape
            contentweather.info()
            print(f'weatherdata_{year}.csv exists')
            break
        except FileNotFoundError as fnfe:
            starttijdweather = perf_counter()
            print(f'\x1b[32mGetting Weather Data... {eventweather}')
            weatherdata = allweatherdata(eventweather, year, mif.loadsession(year, eventweather, sessiontype))
            # TODO VRAAG: Data voegt zichzelf toe zonder append?
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdweather) * 1000:.0f}ms")
            eventiter += 1
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except FileExistsError as fee:
            print(f"\x1b[31m{fee}\x1b[0m")
    try:
        return weatherdata
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
        return None


def writeseasonweatherdata(year, sprinttype):
    """
    Extension to function above which should be called if lapdata has to be written.
    """
    try:
        fw.writecsv(f'weatherdata_{year}', seasonweatherdata(year, sprinttype).drop_duplicates())
        print(f"Season {year} Weather Data written!")
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")