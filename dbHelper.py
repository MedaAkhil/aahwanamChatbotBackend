import dotenv
import mysql.connector
from mysql.connector import Error



dotenv.load_dotenv()
import os
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")
port = os.getenv("PORT")







def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        if connection.is_connected():
            print("✅ Connected to the database.")
            return connection
    except Error as e:
        print("❌ Connection error:", e)
        return None

def run_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return column_names, results
    except Error as e:
        print(f"❌ Query error: {e}")
        return None, None
    finally:
        cursor.close()




def print_joined_service_categories(connection):
    print("\n🔍 Service and Categories:")
    print("=" * 50)

    # query = """
    # SELECT 
    #     s.service_name,
    #     s.description AS service_description,
    #     sc.category_name,
    #     sc.description AS category_description
    # FROM 
    #     services s
    # LEFT JOIN 
    #     services_categories sc ON s.service_id = sc.service_id
    # ORDER BY 
    #     s.service_name, sc.category_name;
    # """


    query = """
SELECT 
    s.service_name,
    s.description AS service_description,
    GROUP_CONCAT(sc.category_name ORDER BY sc.category_name SEPARATOR ', ') AS category_names,
    GROUP_CONCAT(sc.description ORDER BY sc.category_name SEPARATOR ', ') AS category_descriptions
FROM 
    services s
LEFT JOIN 
    services_categories sc ON s.service_id = sc.service_id
GROUP BY 
    s.service_id, s.service_name, s.description
ORDER BY 
    s.service_name;

"""

    columns, data = run_query(connection, query)

    if columns and data:
        print(" | ".join(columns))
        print("-" * 50)
        for row in data:
            print(" | ".join(str(item) if item is not None else "NULL" for item in row))
    else:
        print("⚠️ No data found for joined query.")




def getservicesbylocation(conn, cityorstatename):
    query = f"""
SELECT 
    vsl.city,
    vsl.state,
    GROUP_CONCAT(DISTINCT vs.service_name ORDER BY vs.service_name SEPARATOR ', ') AS listofservice,
    GROUP_CONCAT(DISTINCT vs.description ORDER BY vs.service_name SEPARATOR ' | ') AS description
FROM 
    vendor_service_locations vsl
JOIN 
    vendors_services vs ON vsl.vendor_id = vs.vendor_id
WHERE 
    vsl.city = '{cityorstatename}'
    AND vsl.status = 1
    AND vs.status = 1
GROUP BY 
    vsl.city, vsl.state;

"""
    print(query)
    columns, data = run_query(conn, query)

    if columns and data:
        print(" | ".join(columns))
        print("-" * 50)
        for row in data:
            print(" | ".join(str(item) if item is not None else "NULL" for item in row))
    else:
        print("⚠️ No data found for joined query.")




def getServicePackages(Query):
    query = """
    SELECT 
        package_name, 
        base_price, 
        description
    FROM 
        services_packages;
    """

    columns, data = run_query(conn, query)

    if columns and data:
        print(" | ".join(columns))
        print("-" * 50)
        for row in data:
            print(" | ".join(str(item) if item is not None else "NULL" for item in row))
    else:
        print("⚠️ No data found for service packages.")