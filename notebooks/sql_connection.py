import pyodbc
import pandas as pd

try:
    # Connect to SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=KAAVIYA;"
        "DATABASE=CustomerChurnDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    print("✅ Connected to SQL Server Successfully!")

    # SQL Query
    query = "SELECT * FROM CustomerChurn"

    # Read data into Pandas DataFrame
    df = pd.read_sql(query, conn)

    print("\n✅ Data Loaded Successfully!")
    print("Shape of Dataset:", df.shape)

    print("\nFirst 5 Records:")
    print(df.head())

    # Close connection
    conn.close()
    print("\n✅ SQL Connection Closed.")

except Exception as e:
    print("\n❌ Error:")
    print(e)