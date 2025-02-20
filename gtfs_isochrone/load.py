import os
from collections import namedtuple
from pathlib import Path

import pandas as pd
import numpy as np

Data = namedtuple("Data", ["stops", "durations", "trips_dates", "stoptimes"])

EXTENSION = ".parq"

def load_prepared_data(gtfs_folder):
    paths = {field: os.path.join(gtfs_folder, field + EXTENSION) for field in Data._fields}
    dataframes = {field: pd.read_parquet(path) for field, path in paths.items()}
    data = Data(**dataframes)
    return data


def _store(df, folder, name):
    path = Path(folder) / name
    df.to_parquet(path)


def store_durations(durations, gtfs_folder):
    _store(durations, gtfs_folder, "durations"+EXTENSION)


def store_stops(stops, gtfs_folder):
    _store(stops, gtfs_folder, "stops"+EXTENSION)


def store_trips_dates(trips_dates, gtfs_folder):
    _store(trips_dates, gtfs_folder, "trips_dates"+EXTENSION)


def store_stoptimes(stoptimes, gtfs_folder):
    _store(stoptimes, gtfs_folder, "stoptimes"+EXTENSION)


def load_raw_stops(gtfs_folder):
    stops_path = Path(gtfs_folder)/ "stops.txt"

    return pd.read_csv(
        stops_path,
        usecols=["stop_id", "stop_lat", "stop_lon"],
        dtype={"stop_id": "object", "stop_lat": np.float64, "stop_lon": np.float64},
    )


def load_raw_routes(gtfs_folder):
    routes_path = Path(gtfs_folder) /"routes.txt"

    return pd.read_csv(
        routes_path,
        usecols=["route_id", "route_type"],
        dtype={"route_id": "object", "route_type": np.int16},
    ).drop_duplicates()


def load_raw_calendar_dates(gtfs_folder):
    path_calendar_dates = Path(gtfs_folder) /"calendar_dates.txt"
    return pd.read_csv(
        path_calendar_dates,
        usecols=["service_id", "date"],
        dtype={"service_id": "object", "date": "object"},
        parse_dates=["date"],
    )


def load_raw_trips(gtfs_folder):
    path_trips = os.path.join(gtfs_folder, "trips.txt")
    return pd.read_csv(
        path_trips, usecols=["route_id", "service_id", "trip_id"], dtype="object"
    )


def load_raw_stoptimes(gtfs_folder):
    path_stoptimes = os.path.join(gtfs_folder, "stop_times.txt")
    stoptimes = pd.read_csv(
        path_stoptimes, usecols=["trip_id", "stop_id", "arrival_time"], dtype="object",
    )
    stoptimes["arrival_time"] = pd.TimedeltaIndex(stoptimes["arrival_time"]).round("S")
    stoptimes = stoptimes.loc[:, ["trip_id", "stop_id", "arrival_time"]]
    return stoptimes
