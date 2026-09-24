import duckdb, logging
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="analysis.log")
logger = logging.getLogger(__name__)

DB_PATH = "emissions.duckdb"
TABLES  = {"YELLOW": "yellow_trips", "GREEN": "green_trips"}

def report(message):
    print(message)        
    logger.info(message)  

#1. What was the single largest carbon producing trip of the year for YELLOW and GREEN trips? (One result for each type)

def main():
    """run CO2 analyses and make a monthly comparison plot"""
    
    con = duckdb.connect(database=DB_PATH, read_only=True)

    yellow_largest = con.execute("""
        SELECT trip_co2_kgs, trip_distance, pickup_time
        FROM yellow_trips
        ORDER BY trip_co2_kgs DESC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Largest carbon-producing trip: {yellow_largest[0]:.3f} kg CO2, {yellow_largest[1]:.2f} miles, picked up at {yellow_largest[2]}")

    green_largest = con.execute("""
        SELECT trip_co2_kgs, trip_distance, pickup_time
        FROM green_trips
        ORDER BY trip_co2_kgs DESC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Largest carbon-producing trip: {green_largest[0]:.3f} kg CO2, {green_largest[1]:.2f} miles, picked up at {green_largest[2]}")


#Complete the analysis.py script to report the following calculations using DuckDB/SQL. You should give one answer for each cab type, YELLOW and GREEN:


#2. Across the entire year, what on average are the most carbon heavy and carbon light hours of the day for YELLOW and for GREEN trips? (1-24)

    yellow_heaviest_hour = con.execute("""
        SELECT hour_of_day + 1, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY hour_of_day ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Heavy Hour of Day: {yellow_heaviest_hour[0]} ({yellow_heaviest_hour[1]:.3f} kg avg/trip)")

    yellow_lightest_hour = con.execute("""
        SELECT hour_of_day + 1, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY hour_of_day ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Light Hour of Day: {yellow_lightest_hour[0]} ({yellow_lightest_hour[1]:.3f} kg avg/trip)")

    green_heaviest_hour = con.execute("""
        SELECT hour_of_day + 1, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY hour_of_day ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Heavy Hour of Day: {green_heaviest_hour[0]} ({green_heaviest_hour[1]:.3f} kg avg/trip)")

    green_lightest_hour = con.execute("""
        SELECT hour_of_day + 1, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY hour_of_day ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Light Hour of Day: {green_lightest_hour[0]} ({green_lightest_hour[1]:.3f} kg avg/trip)")


#3. Across the entire year, what on average are the most carbon heavy and carbon light days of the week for YELLOW and for GREEN trips? (Sun-Sat)

    day_names = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

    yellow_heaviest_day = con.execute("""
        SELECT day_of_week, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY day_of_week ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Heavy Day of Week: {day_names[int(yellow_heaviest_day[0])]} ({yellow_heaviest_day[1]:.3f} kg avg/trip)")

    yellow_lightest_day = con.execute("""
        SELECT day_of_week, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY day_of_week ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Light Day of Week: {day_names[int(yellow_lightest_day[0])]} ({yellow_lightest_day[1]:.3f} kg avg/trip)")

    green_heaviest_day = con.execute("""
        SELECT day_of_week, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY day_of_week ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Heavy Day of Week: {day_names[int(green_heaviest_day[0])]} ({green_heaviest_day[1]:.3f} kg avg/trip)")

    green_lightest_day = con.execute("""
        SELECT day_of_week, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY day_of_week ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Light Day of Week: {day_names[int(green_lightest_day[0])]} ({green_lightest_day[1]:.3f} kg avg/trip)")


#4. Across the entire year, what on average are the most carbon heavy and carbon light weeks of the year for YELLOW and for GREEN trips? (1-52)

    yellow_heaviest_week = con.execute("""
        SELECT week_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY week_of_year ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Heavy Week of Year: {yellow_heaviest_week[0]} ({yellow_heaviest_week[1]:.3f} kg avg/trip)")

    yellow_lightest_week = con.execute("""
        SELECT week_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY week_of_year ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Light Week of Year: {yellow_lightest_week[0]} ({yellow_lightest_week[1]:.3f} kg avg/trip)")

    green_heaviest_week = con.execute("""
        SELECT week_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY week_of_year ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Heavy Week of Year: {green_heaviest_week[0]} ({green_heaviest_week[1]:.3f} kg avg/trip)")

    green_lightest_week = con.execute("""
        SELECT week_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY week_of_year ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Light Week of Year: {green_lightest_week[0]} ({green_lightest_week[1]:.3f} kg avg/trip)")


#5. Across the entire year, what on average are the most carbon heavy and carbon light months of the year for YELLOW and for GREEN trips? (Jan-Dec)

    month_names = [None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    yellow_heaviest_month = con.execute("""
        SELECT month_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY month_of_year ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Heavy Month of Year: {month_names[int(yellow_heaviest_month[0])]} ({yellow_heaviest_month[1]:.3f} kg avg/trip)")

    yellow_lightest_month = con.execute("""
        SELECT month_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM yellow_trips
        GROUP BY month_of_year ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(YELLOW) Most Carbon Light Month of Year: {month_names[int(yellow_lightest_month[0])]} ({yellow_lightest_month[1]:.3f} kg avg/trip)")

    green_heaviest_month = con.execute("""
        SELECT month_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY month_of_year ORDER BY avg_co2 DESC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Heavy Month of Year: {month_names[int(green_heaviest_month[0])]} ({green_heaviest_month[1]:.3f} kg avg/trip)")

    green_lightest_month = con.execute("""
        SELECT month_of_year, AVG(trip_co2_kgs) AS avg_co2
        FROM green_trips
        GROUP BY month_of_year ORDER BY avg_co2 ASC LIMIT 1
    """).fetchone()
    report(f"(GREEN) Most Carbon Light Month of Year: {month_names[int(green_lightest_month[0])]} ({green_lightest_month[1]:.3f} kg avg/trip)")


#6. Use a plotting library to generate a time-series plot with MONTH on the X-axis and CO2 totals on the Y-axis, one line/series for YELLOW and one for GREEN

    yellow_monthly = con.execute("""
        SELECT month_of_year, SUM(trip_co2_kgs) AS total_co2
        FROM yellow_trips
        GROUP BY month_of_year ORDER BY month_of_year
    """).fetchall()

    green_monthly = con.execute("""
        SELECT month_of_year, SUM(trip_co2_kgs) AS total_co2
        FROM green_trips
        GROUP BY month_of_year ORDER BY month_of_year
    """).fetchall()

    months = [row[0] for row in yellow_monthly]
    yellow_totals = [row[1] / 1000.0 for row in yellow_monthly]  # kg -> tonnes
    green_totals = [row[1] / 1000.0 for row in green_monthly]    # kg -> tonnes

    fig, ax1 = plt.subplots(figsize=(10, 6))

    yellow_line, = ax1.plot(months, yellow_totals, marker="o", color="gold", label="Yellow Taxi")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Yellow Taxi CO2 (tonnes)", color="gold")
    ax1.tick_params(axis="y", labelcolor="gold")

    ax2 = ax1.twinx()
    green_line, = ax2.plot(months, green_totals, marker="o", color="green", label="Green Taxi")
    ax2.set_ylabel("Green Taxi CO2 (tonnes)", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    ax1.set_title("Total CO2 Output by Month")
    ax1.legend([yellow_line, green_line], ["Yellow Taxi", "Green Taxi"], loc="upper left")

    fig.tight_layout()
    fig.savefig("co2_by_month_2024.png", dpi=150)
    report("Plot written to co2_by_month_2024.png")

    con.close()

if __name__ == "__main__":
    main()