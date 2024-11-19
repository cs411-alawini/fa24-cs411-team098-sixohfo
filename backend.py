# from flask import Flask, jsonify
# import mysql.connector

# app = Flask(__name__)

# # MySQL Configuration
# db_config = {
#     'user': 'root',
#     'password': 'Password',
#     'host': '34.118.207.21',  # Public IP of your GCP MySQL instance
#     'database': 'seeken',
#     'port': 3306  # Default MySQL port
# }

# # Establish connection
# def get_db_connection():
#     try:
#         print("trying db connection")
#         connection = mysql.connector.connect(**db_config)
#         print("got ittttt")
#         return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

# @app.route("/")
# def test_connection():
#     conn = get_db_connection()
#     if conn:
#         return jsonify({"message": "Successfully connected to the database!"})
#     else:
#         return jsonify({"error": "Failed to connect to the database."})

# if __name__ == "__main__":
#     app.run(debug=True)


import mysql.connector

db_config = {
    'user': 'root',
    'password': 'Password',
    'host': '34.118.207.21',
    'database': 'seeken',
    'port': 3306,
    'connection_timeout': 10  # Optional
}

try:
    print("Connecting...")
    conn = mysql.connector.connect(**db_config)
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")