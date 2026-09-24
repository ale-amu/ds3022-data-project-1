# put raw nyc data in a database

import duckdb
import os
import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"   
YEAR = 2024

def load_parquet_files():
    """load Yellow/Green taxi trips & vehicle emissions lookup"""

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")

        # vehicle_emissions.csv
        con.execute(f"""
            DROP TABLE IF EXISTS vehicle_emissions;
            CREATE TABLE vehicle_emissions AS
            SELECT * FROM read_csv_auto(
            'data/vehicle_emissions.csv');
            """)
        
        logger.info("Dropped table if exists")

        n = con.execute(
            "SELECT COUNT(*) FROM vehicle_emissions"
            ).fetchone()[0]

        logger.info(f"vehicle_emissions: {n} rows loaded")
        print(f"vehicle_emissions: {n} rows loaded")

        # load yellow & green taxi trip data 
        for color, prefix in (("yellow", "tpep"), ("green", "lpep")):
            table = f"{color}_trips"

            con.execute(f"""
                DROP TABLE IF EXISTS {table};
                CREATE TABLE {table} (
                    VendorID INTEGER,
                    pickup_time TIMESTAMP,
                    dropoff_time TIMESTAMP,
                    passenger_count BIGINT,
                    trip_distance DOUBLE
                )
            """)

            for month in range(1, 13):
                url = (f"{BASE_URL}{color}_tripdata_{YEAR}-{month:02d}.parquet")

                con.execute(
                    f"INSERT INTO {table} "
                    f"SELECT VendorID, "
                    f"{prefix}_pickup_datetime AS pickup_time, "
                    f"{prefix}_dropoff_datetime AS dropoff_time, "
                    f"passenger_count, trip_distance "
                    f"FROM read_parquet('{url}')" 
                )
                logger.info(f"Loaded {color} taxi trip data for month {month:02d} into {table}")  


            # raw count after 12 mojths
            n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            logger.info(f"{table}: {n:,} rows loaded after 12 months")
            print(f"{table}: {n:,} rows loaded after 12 months")

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    load_parquet_files()


#did all 24 months load (12y +12g)
 #and did load.py print raw counts for all 3 tables
 #and osmthing alias