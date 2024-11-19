from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'Password',
    'host': '34.118.207.21',  # Public IP of your GCP MySQL instance
    'database': 'seeken',
    'port': 3306  # Default MySQL port
}

# Establish connection
def get_db_connection():
    try:
        print("trying db connection")
        connection = mysql.connector.connect(**db_config)
        print("got ittttt")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Test connection
@app.route("/")
def test_connection():
    conn = get_db_connection()
    if conn:
        return jsonify({"message": "Successfully connected to the database!"})
    else:
        return jsonify({"error": "Failed to connect to the database."})

# CREATE - Add a new record
@app.route("/create", methods=["POST"])
def create_record():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            return jsonify({"message": "Record created successfully!"}), 201
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to create record."}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed."}), 500

# READ - Get all records
@app.route("/read", methods=["GET"])
def read_records():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            return jsonify(results), 200
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to fetch records."}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed."}), 500

# UPDATE - Update a record by ID
@app.route("/update/<int:id>", methods=["PUT"])
def update_record(id):
    data = request.json
    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "No record found with the given ID."}), 404
            return jsonify({"message": "Record updated successfully!"}), 200
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to update record."}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed."}), 500

# DELETE - Delete a record by ID
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_record(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "No record found with the given ID."}), 404
            return jsonify({"message": "Record deleted successfully!"}), 200
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to delete record."}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed."}), 500

if __name__ == "__main__":
    app.run(debug=True)