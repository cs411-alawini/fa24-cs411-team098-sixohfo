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

# CREATE: Add a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['Username']
    password = data['Password']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO User (Username, Password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

# READ: Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM User")
        users = cursor.fetchall()
        return jsonify(users), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

# READ: Get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

# UPDATE: Update a user's information
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    username = data.get('Username')
    password = data.get('Password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE User SET Username = %s, Password = %s WHERE UserID = %s",
            (username, password, user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "User updated successfully!"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

# DELETE: Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "User deleted successfully!"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

    
@app.route('/most_mentioned_entities_by_podcast', methods=['GET'])
def get_most_mentioned_entities_by_podcast():
    """Retrieve the most mentioned entities by podcast."""
    connection = get_db_connection()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('CALL GetMostMentionedEntitiesByPodcast')
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing stored procedure: {err}")
            return jsonify({'error': 'Failed to retrieve most mentioned entities by podcast.'}), 500
    else:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

@app.route('/most_mentioned_companies_with_revenue', methods=['GET'])
def get_most_mentioned_companies_with_revenue():
    """Retrieve the most mentioned companies with revenue."""
    connection = get_db_connection()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('CALL GetMostMentionedCompaniesWithRevenue')
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing stored procedure: {err}")
            return jsonify({'error': 'Failed to retrieve most mentioned companies with revenue.'}), 500
    else:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

@app.route('/most_mentioned_books', methods=['GET'])
def get_most_mentioned_books():
    """Retrieve the most mentioned books."""
    connection = get_db_connection()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("CALL GetMostMentionedBooks()")
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error executing stored procedure: {err}")
            return jsonify({'error': 'Failed to retrieve most mentioned books.'}), 500
    else:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
