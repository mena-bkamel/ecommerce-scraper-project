import csv
import json
import sqlite3


class SaveData:
    def __init__(self):
        ...

    def save_to_csv(self, file_name: str, header: list, records: list[tuple], mode="w"):
        platform = records[0][-1].lower()
        file_name = file_name.replace(" ", "_").lower()

        with open(f"{file_name}.csv", mode, newline='', encoding='utf-8') as f:
            if mode == "w":
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(records)

    def create_db(self, db_name: str = "file.db", table_name="Product".lower(), columns: dict = None):
        """
           Create a database and a table with specified columns.

           Parameters:
           - db_name: Name of the database file (default: "file.db").
           - table_name: Name of the table to create (default: "Product").
           - columns: A dictionary where keys are column names and values are their SQL data types.
                      Example: {"product_name": "TEXT NOT NULL", "price": "REAL", "num_reviews": "TEXT"}
           """
        db_name = db_name.lower()

        if not db_name.endswith("db"):
            db_name += ".db"

        if not columns:
            print("Error: The 'columns' parameter is required to define the table structure. "
                  "It should be a dictionary like this example:")
            print({
                "product_name": "TEXT NOT NULL",
                "price": "REAL",
                "num_reviews": "TEXT",
                "url": "TEXT",
                "date": "TEXT"
            })
            return

        column_definitions = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        column_definitions = f"id INTEGER PRIMARY KEY AUTOINCREMENT, {column_definitions}"
        if not db_name.endswith(".db"):
            db_name = db_name.replace(" ", "_") + ".db"

        table_name = table_name.replace(' ', '_').lower()
        try:
            with sqlite3.connect(db_name) as conn:

                cursor = conn.cursor()
                cursor.execute(f'''CREATE TABLE IF NOT EXISTS 
                        "{table_name}" (
                            {column_definitions}
                            )''')
                conn.commit()
                print(f"Database '{db_name}' and table '{table_name}' created successfully.")

                return db_name, table_name, [col_name for col_name in columns]

        except sqlite3.Error as err:
            print(f"Error creating database or table: {err}")


    def insert_records(self, db_name, table_name, columns_names: list, records: list[tuple]):
        """
        Insert a list of tuples into the specified database table.

        Parameters:
        - db_name: Name of the database file.
        - table_name: Name of the table where records will be inserted.
        - records: A list of tuples, where each tuple represents a row of data.
        """
        if not db_name.endswith(".db"):
            db_name = db_name.replace(" ", "_") + ".db"

        table_name = table_name.replace(' ', '_').lower()

        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                col_names = ", ".join(columns_names)
                placeholders = ", ".join(["?" for value in columns_names])
                query = f"INSERT INTO '{table_name}' ({col_names}) VALUES ({placeholders})"
                cursor.executemany(query, records)
                conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def save_to_json(self, file_name: str, header: list, records):
        data = {}
        result = [dict(zip(header, record)) for record in records]
        data[file_name] = result
        platform = records[0][-1]

        output_file = file_name.replace(" ", "_")

        with open(f"{output_file.lower()}.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Data saved to data.json")
