import duckdb
import logging


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='transform.log'
)
logger = logging.getLogger(__name__)


def transform_tables():
    """add trip_co2_kgs, avg_mph, and time-based columns"""

    con = None # this is a placeholder for the connection object

    try:
        #connect to local DuckDB instance
        con = duckdb.connect(database= "emissions.duckdb", read_only=False)
        logger.info("Connected to DuckDB instance") 

#After cleaning you should have 1 or 2 cleaned trip tables representing YELLOW and GREEN trips for all of 2024. Perform the following transformations to the data:

        print("Transforming yellow_trips...")
        logger.info("Transforming yellow_trips...")

#1. Calculate total CO2 output per trip by multiplying the trip_distance by the co2_grams_per_mile value in the vehicle_emissions lookup table,
# then dividing by 1000 (to calculate Kg). Insert that value as a new column named trip_co2_kgs. This calculation should be based upon a 
# real-time lookup from the vehicle_emissions table and not hard-coded as a numeric figure

        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS trip_co2_kgs DOUBLE;
            UPDATE yellow_trips
            SET trip_co2_kgs = trip_distance * (SELECT co2_grams_per_mile FROM vehicle_emissions WHERE vehicle_type = 'yellow_taxi') / 1000;
            """)

#2. Calculate average miles per hour based on distance divided by the duration of the trip, and insert that value as a new column avg_mph.

        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS avg_mph DOUBLE;
            UPDATE yellow_trips
            SET avg_mph = trip_distance / (date_diff('second', pickup_time, dropoff_time) / 3600.0);
            """)    

#3. Extract the HOUR of the day from the pickup_time and insert it as a new column hour_of_day.

        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS hour_of_day INTEGER;
            UPDATE yellow_trips
            SET hour_of_day = HOUR(pickup_time);
            """)    

#4. Extract the DAY OF WEEK from the pickup time and insert it as a new column day_of_week.
        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
            UPDATE yellow_trips
            SET day_of_week = DAYOFWEEK(pickup_time);
            """)    

#5. Extract the WEEK NUMBER from the pickup time and insert it as a new column week_of_year.

        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS week_of_year INTEGER;
            UPDATE yellow_trips
            SET week_of_year = WEEK(pickup_time);
            """)    

#6. Extract the MONTH from the pickup time and insert it as a new column month_of_year.

        con.execute(f"""
            ALTER TABLE yellow_trips ADD COLUMN IF NOT EXISTS month_of_year INTEGER;
            UPDATE yellow_trips
            SET month_of_year = MONTH(pickup_time);
            """)


        print("Transforming green_trips...")
        logger.info("Transforming green_trips...") 

#GREEN — 1. Calculate total CO2 output per trip by multiplying the trip_distance by the co2_grams_per_mile value in the vehicle_emissions lookup table,
# then dividing by 1000 (to calculate Kg). Insert that value as a new column named trip_co2_kgs. This calculation should be based upon a 
# real-time lookup from the vehicle_emissions table and not hard-coded as a numeric figure

        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS trip_co2_kgs DOUBLE;
            UPDATE green_trips
            SET trip_co2_kgs = trip_distance * (SELECT co2_grams_per_mile FROM vehicle_emissions WHERE vehicle_type = 'green_taxi') / 1000;
            """)

#GREEN — 2. Calculate average miles per hour based on distance divided by the duration of the trip, and insert that value as a new column avg_mph.

        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS avg_mph DOUBLE;
            UPDATE green_trips
            SET avg_mph = trip_distance / (date_diff('second', pickup_time, dropoff_time) / 3600.0);
            """)    

#GREEN — 3. Extract the HOUR of the day from the pickup_time and insert it as a new column hour_of_day.

        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS hour_of_day INTEGER;
            UPDATE green_trips
            SET hour_of_day = HOUR(pickup_time);
            """)    

#GREEN — 4. Extract the DAY OF WEEK from the pickup time and insert it as a new column day_of_week.
        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
            UPDATE green_trips
            SET day_of_week = DAYOFWEEK(pickup_time);
            """)    

#GREEN — 5. Extract the WEEK NUMBER from the pickup time and insert it as a new column week_of_year.

        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS week_of_year INTEGER;
            UPDATE green_trips
            SET week_of_year = WEEK(pickup_time);
            """)    

#GREEN — 6. Extract the MONTH from the pickup time and insert it as a new column month_of_year.

        con.execute(f"""
            ALTER TABLE green_trips ADD COLUMN IF NOT EXISTS month_of_year INTEGER;
            UPDATE green_trips
            SET month_of_year = MONTH(pickup_time);
            """)

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    transform_tables()


