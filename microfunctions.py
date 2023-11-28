import fastf1
import fastf1.plotting


def loadcardata(session, driver, lap):
    """
    #TODO BESCHRIJVING

    Args:
    - session
    - driver
    - lap

    Returns:
    - Telemetry (DataFrame): information regarding the car within a given lap.
    """
    return session.laps.pick_driver(str(driver)).pick_lap(int(lap)).get_car_data()

def loadposdata(session, driver, lap):
    return session.laps.pick_driver(str(driver)).pick_lap(int(lap)).get_pos_data()


def loadlap(session, lap):
    """
    #TODO BESCHRIJVING

    Args:
    - session
    - lap

    Returns:
    - Lapinformation (DataFrame): 
    """
    try:
        return session.laps.pick_lap(lap)
    except:
        return None


def loadremaining():
    """
    Loads the remaining sessions given the latest year that's available.

    Returns:
    - remaining (DataFrame): which contains the remaining sessions within the latest season.
    """
    return fastf1.get_events_remaining()


def loadschedule(year):
    """
    Loads the schedule for a given year.
    
    Args:
    - year (int): the year of which the schedule is loaded for.

    Returns:
    - schedule (DataFrame): the schedule of the given year.
    """
    return fastf1.get_event_schedule(int(year))


def loadsession(year, circuit, sessiontype):
    """
    Loads a given session defined by:
    
    Args:
    - year (int): the year the race was held.
    - circuit (name: str | id: int): the circuit which was raced on in the given year.
    - sessiontype (str): which type of session it is (Qualifying, Race, etc.).

    Returns:
    - session (DataFrame): which contains a variety of information regarding the requested session.
    """
    try:
        session = fastf1.get_session(year, circuit, sessiontype)
    except ValueError:
        return None
    try:
        session.load(laps=True, weather=True, telemetry=True, messages=True)
        return session
    except:
        print(f'\x1b[31mFailed to load: {year}, {circuit}, "{sessiontype}"\x1b[0m')
