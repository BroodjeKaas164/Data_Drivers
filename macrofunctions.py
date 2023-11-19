from time import perf_counter

import pandas as pd

import filewriters as fw
import microfunctions as mif


def cacheall(year, sprinttype):
    """
    Caches all sessions for offline use for the requested year and sprinttype:

    args:
    - year (int/str): the year for which the sessions should be loaded
    - sprinttype (str): the sprinttype for which the sessions should be loaded
    """
    schedule = mif.loadschedule(year)
    for name in schedule.OfficialEventName:
        print("\x1b[32m")
        mif.loadsession(year, name, sprinttype)
        print("\x1b[0m")


def allcardata(track, year, session, sessiontype, cardata=None):
    """
    # TODO: BESCHRIJVING
    """
    try:
        combinedcardata = []
        starttijdcar = perf_counter()
        print(f'\x1b[32mGetting Car Telemetry Data... {track}')
        for driver in session.drivers:
            lap = 1
            try:
                while lap <= session.total_laps:
                    lstdriver, lstyear, lsttrack, lstlap, lsttype, x = [], [], [], [], [], 1
                    cardata = session.laps.pick_driver(driver).pick_lap(int(lap)).get_car_data()
                    while x <= cardata.Brake.size:
                        lstdriver.append(driver)
                        lstyear.append(year)
                        lsttrack.append(track)
                        lstlap.append(lap)
                        lsttype.append(sessiontype)
                        x += 1
                    cardata["driverID"] = lstdriver
                    cardata['year'] = lstyear
                    cardata['gp'] = lsttrack
                    cardata['lap'] = lstlap
                    cardata['sessiontype'] = lsttype
                    combinedcardata.append(cardata)
                    lap += 1
            except KeyError as ke:
                print(f"\x1b[31m{ke}\x1b[0m")
            except ValueError as ve:
                print(f"\x1b[31m{ve}\x1b[0m")
            except:
                print('Data not loaded')
        try:
            _cardata = pd.concat(combinedcardata)
            print(f"Tijd: \x1b[31m{(perf_counter() - starttijdcar) * 1000:.0f}ms")
            return _cardata
        except UnboundLocalError as ule:
            print(f"\x1b[31m{ule}\x1b[0m")
        except AttributeError as ae:
            print(f"\x1b[31m{ae}\x1b[0m")
        except TypeError as te:
            print(f"\x1b[31m{te}\x1b[0m")
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    except ValueError as ve:
        print(f"\x1b[31m{ve}\x1b[0m")


def alllapdata(name, year, session, sessiontype, lap=1, lapinfo=None):
    """
    # TODO: BESCHRIJVING
    """
    try:
        combinedlapdata = []
        starttijdlap = perf_counter()
        print(f'\x1b[32mGetting Lap Data... {name}')
        while lap <= session.total_laps:
            try:
                lstyear, lstname, lsttype, x = [], [], [], 1
                lapinfo = mif.loadlap(session, lap)
                while x <= lapinfo.DriverNumber.size:
                    lstyear.append(year)
                    lstname.append(name)
                    lsttype.append(sessiontype)
                    x += 1
                lapinfo['year'] = lstyear
                lapinfo['gp'] = lstname
                lapinfo['sessiontype'] = lsttype
            except KeyError as ke:
                print(f"\x1b[31m{ke}\x1b[0m")
            except ValueError as ve:
                print(f"\x1b[31m{ve}\x1b[0m")
            combinedlapdata.append(lapinfo)
            # print(lapinfo)
            lap += 1
        _lapdata = pd.concat(combinedlapdata)
        print(f"Tijd: \x1b[31m{(perf_counter() - starttijdlap) * 1000:.0f}ms")
        return _lapdata
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    except TypeError as te:
            print(f"\x1b[31m{te}\x1b[0m")
    except:
        print('\t\tData not loaded')


def allweatherdata(name, year, session, sessiontype, lap=1, weerdata=None):
    """
    TODO: Verander dit naar weerdata van de sessie zelf {name, session, year} extra values {lap}
    """
    try:
        combinedweatherdata = []
        starttijdweather = perf_counter()
        print(f'\x1b[32mGetting Weather Data... {name}')
        try:
            lstyear, lstlap, lstname, lsttype, x = [], [], [], [], 1
            weerdata = session.weather_data
            # TODO: Krijg af en toe lege dataframes terug?
            while x <= weerdata.AirTemp.size:
                lstyear.append(year)
                lstlap.append(lap)
                lstname.append(name)
                lsttype.append(sessiontype)
                x += 1
            weerdata['year'] = lstyear
            weerdata['lap'] = lstlap
            weerdata['gp'] = lstname
            weerdata['sessiontype'] = lsttype
            combinedweatherdata.append(weerdata)
        except KeyError as ke:
            print(f"\x1b[31m{ke}\x1b[0m")
        except ValueError as ve:
            print(f"\x1b[31m{ve}\x1b[0m")
        except:
            print("Data Not Loaded")
        lap += 1
        _weatherdata = pd.concat(combinedweatherdata)
        print(f"Tijd: \x1b[31m{(perf_counter() - starttijdweather) * 1000:.0f}ms")
        return _weatherdata
    except AttributeError as ae:
        print(f"\x1b[31m{ae}\x1b[0m")
    except TypeError as te:
        print(f"\x1b[31m{te}\x1b[0m")
