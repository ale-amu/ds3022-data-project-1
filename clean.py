import duckdb
import logging

#INSERT INTO yellow_trips
#SELECT * FROM duckdb.read_parquet('yellow_tripdata_2020-01.csv');

#writes timestamped messages to clean.log instaed of putting erros in terminal

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)
logger = logging.getLogger(__name__)

def clean_tables():
    """remove any duplicates as well as invalid trips"""

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")

#were cleaning both yellow and green so if we use a loop iwe wont have to do everything twice
        for table in ['yellow_trips', 'green_trips']:
            print(f"Cleaning {table}...")

            #1. remove duplicates - we cant craete a tabel for yellow trips if it already exists os we drop the original rename and make a enw one and rename after

            con.execute(f"""
            DROP TABLE IF EXISTS {table}_clean;
            CREATE TABLE {table}_clean AS
            SELECT DISTINCT * FROM {table};
            DROP TABLE {table};
            ALTER TABLE {table}_clean RENAME TO {table};
            """)
            print(con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) #recheck this line

            #step 2: 0-passenger trip
            before = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE passenger_count = 0
            """).fetchone()[0]
            print(f"Before delete: {before}")
            logger.info(f"Before delete: {before}") 

            con.execute(f"""
            DELETE FROM {table}
            WHERE passenger_count = 0
            """)

            after = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE passenger_count = 0
            """).fetchone()[0]
            print(f"After delete: {after}")
            logger.info(f"After delete: {after}")


           #step 3: Remove any trips 0 miles in length.

            before = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE trip_distance = 0
            """).fetchone()[0]
            print(f"Before delete: {before}") #COUNT HOW MANY COLUMNS HAVE 0 TRIPS LOGEGD
            logger.info(f"Before delete: {before}") 

            con.execute(f"""
            DELETE FROM {table}
            WHERE trip_distance = 0
            """)

            after = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE trip_distance = 0
            """).fetchone()[0]
            print(f"After delete: {after}") #this should always be zeero after DELETE
            logger.info(f"After delete: {after}")

            #step 4: trips over 100 miles

            before = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE trip_distance > 100
            """).fetchone()[0]
            print(f"Before delete: {before}")
            logger.info(f"Before delete: {before}") 

            con.execute(f"""
            DELETE FROM {table}
            WHERE trip_distance > 100
            """)

            after = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE trip_distance > 100
            """).fetchone()[0]
            print(f"After delete(verify): {after}")
            logger.info(f"After delete(verify): {after}")


            #step 5: trips over 1 day
            before = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
            """).fetchone()[0]
            print(f"Before delete: {before}")
            logger.info(f"Before delete: {before}") 


            #second is the unit of time we are using to measure the difference between pickup and dropoff time
            con.execute(f"""
            DELETE FROM {table}
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400 
            """)

            # 86400 seconds in a day
            after = con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
            """).fetchone()[0]
            print(f"After delete(verify): {after}")
            logger.info(f"After delete(verify): {after}")

            #before delete : 1
            #after delete verify : 0
 
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_tables()