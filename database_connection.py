import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="GYMDBOmerNoamStage3",
            user="NoamHadad1",
            password="Noam.123"
        )
        print("✅ Connected to the database successfully!")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

