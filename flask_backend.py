import sqlite3

from flask import Flask, jsonify

app = Flask(__name__)

DB_PATH = "products.db"
TABLE = "Products"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE}")
        products = cursor.fetchall()
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        return jsonify({"error": "An error occurred while retrieving jobs."}), 500

    return jsonify([dict(row) for row in products])


if __name__ == "__main__":
    app.run(debug=True)
