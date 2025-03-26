import psycopg2
import csv

# הגדרות חיבור למסד הנתונים - עדכן לפי הפרטים שלך
DB_NAME = "my_dbdata"
DB_USER = "omer"
DB_PASSWORD = "gerbil"
DB_HOST = "localhost"
DB_PORT = "5432"

# חיבור למסד הנתונים
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# קריאת הנתונים מה-CSV והכנסתם למסד הנתונים
with open("workout_real_dates.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # דילוג על כותרות
    for row in reader:
        cursor.execute(
            "INSERT INTO Workout (workout_id, workout_name, day_number, date_scheduled, last_completed) VALUES (%s, %s, %s, %s, %s)",
            row,
        )

# שמירת השינויים וסגירת החיבור
conn.commit()
cursor.close()
conn.close()

print("✅ הנתונים הוזנו בהצלחה!")
