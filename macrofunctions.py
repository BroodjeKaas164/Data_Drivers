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


def allcardata(track, year, session, combinedcardata=[], _cardata=None):
    """
    # TODO: Beschrijving
    """
    try:
        for driver in session.drivers:
            lap = 1
            try:
                while lap <= session.total_laps:
                    lstdriver, lstyear, lsttrack, lstlap, x = [], [], [], [], 1
                    cardata = session.laps.pick_driver(driver).pick_lap(int(lap)).get_car_data()
                    while x <= cardata.Brake.size:
                        lstdriver.append(driver)
                        lstyear.append(year)
                        lsttrack.append(session.event.RoundNumber)
                        lstlap.append(lap)
                        x += 1
                    cardata["driverID"] = lstdriver
                    cardata['year'] = lstyear
                    cardata['roundnumber'] = lsttrack
                    cardata['lap'] = lstlap
                    combinedcardata.append(cardata)
                    lap += 1
            except KeyError as ke:
                print(f"\x1b[31m{ke}\x1b[0m")
            except ValueError as ve:
                print(f"\x1b[31m{ve}\x1b[0m")
            except:
                print('\n\tUNKOWN ERROR!')
        _cardata = pd.concat(combinedcardata)
        print(_cardata)
        return _cardata
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    except ValueError as ve:
        print(f"\x1b[31m{ve}\x1b[0m")


def seasoncardata(track, session, year, sessiontype, eventiter=0):
    """
    TODO: BESCHRIJVING
    """
    try:
        contentcar = pd.read_csv(f'cardata_{year}.csv')
        contentcar.isnull().sum()
        contentcar.shape
        contentcar.info()
        print(f'cardata_{year}.csv exists')
    except FileNotFoundError as fnfe:
        starttijdcar = perf_counter()
        print(f'\x1b[32mGetting Car Telemetry Data... {track}')
        cardata = allcardata(track, year, session)
        # TODO VRAAG: Data voegt zichzelf toe zonder append?
        print(f"Tijd: \x1b[31m{(perf_counter() - starttijdcar) * 1000:.0f}ms")
        eventiter += 1
        pass
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    try:
        return cardata
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
        return None


def writeseasoncardata(track, session, year, sprinttype):
    """
    Extension to function above which should be called if cardata has to be written.
    """
    try:
        return seasoncardata(track, session, year, sprinttype)
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")


def alllapdata(name, year, session, lap=1, combinedlapdata=[], _lapdata=None):
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
                    lstname.append(session.event.RoundNumber)
                    x += 1
                lapinfo['year'] = lstyear
                lapinfo['roundnumber'] = lstname
            except KeyError as ke:
                print(f"\x1b[31m{ke}\x1b[0m")
            except ValueError as ve:
                print(f"\x1b[31m{ve}\x1b[0m")
            combinedlapdata.append(lapinfo)
            # print(lapinfo)
            lap += 1
        _lapdata = pd.concat(combinedlapdata)
        print(_lapdata)
        return _lapdata
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    except:
        print('\t\tSOMETHING WENT WRONG')


def seasonlapdata(track, session, year, sessiontype, eventiter=0, combinedlap=[]):
    try:
        contentlap = pd.read_csv(f'lapdata_{year}.csv')
        contentlap.isnull().sum()
        contentlap.shape
        contentlap.info()
        print(f'lapdata_{year}.csv exists')
    except FileNotFoundError as fnfe:
        starttijdlap = perf_counter()
        print(f'\x1b[32mGetting Lap Data... {track}')
        lapdata = alllapdata(track, year, session)
        print(f"Tijd: \x1b[31m{(perf_counter() - starttijdlap) * 1000:.0f}ms")
        if lapdata.empty:
            pass
        else:
            combinedlap.append(lapdata)
        eventiter += 1
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
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


def writeseasonlapdata(track, session, year, sprinttype):
    """
    Extension to function above which should be called if lapdata has to be written.
    """
    try:
        return seasonlapdata(track, session, year, sprinttype)
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")



def allweatherdata(name, year, session, combinedweatherdata=[], lap=1, _weatherdata=None):
    # TODO: Verander dit naar weerdata van de sessie zelf {name, session, year} extra values {lap}
    # DRIVER IS HIER NIET NODIG AANGEZIEN DE DATA HIER HETZELFDE IS.
    try:
        try:
            lstyear, lstlap, lstname, x = [], [], [], 1
            weerdata = session.weather_data
            # TODO: Krijg af en toe lege dataframes terug?
            while x <= weerdata.AirTemp.size:
                lstyear.append(year)
                lstlap.append(lap)
                lstname.append(session.event.RoundNumber)
                x += 1
            weerdata['year'] = lstyear
            weerdata['lap'] = lstlap
            weerdata['roundnumber'] = lstname
            combinedweatherdata.append(weerdata)
        except KeyError as ke:
            print(f"\x1b[31m{ke}\x1b[0m")
        except ValueError as ve:
            print(f"\x1b[31m{ve}\x1b[0m")
        lap += 1
        _weatherdata = pd.concat(combinedweatherdata)
        print(_weatherdata)
        return _weatherdata
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")


def seasonweatherdata(track, session, year, sessiontype):
    try:
        contentweather = pd.read_csv(f'weatherdata_{year}.csv')
        contentweather.isnull().sum()
        contentweather.shape
        contentweather.info()
        print(f'weatherdata_{year}.csv exists')
    except FileNotFoundError as fnfe:
        starttijdweather = perf_counter()
        print(f'\x1b[32mGetting Weather Data... {track}')
        weatherdata = allweatherdata(track, year, session)
        # TODO VRAAG: Data voegt zichzelf toe zonder append?
        print(f"Tijd: \x1b[31m{(perf_counter() - starttijdweather) * 1000:.0f}ms")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    try:
        return weatherdata
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
        return None


def writeseasonweatherdata(track, session, year, sprinttype):
    """
    Extension to function above which should be called if lapdata has to be written.
    """
    try:
        return seasonweatherdata(track, session, year, sprinttype)
    except UnboundLocalError as ule:
        print(f"\x1b[31m{ule}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")