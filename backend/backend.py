from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
# MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'Password',
    'host': '34.118.207.21',  
    'database': 'seeken',
    'port': 3306 
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

@app.route("/add_user", methods=['POST'])
def add_new_user():
    data = request.json
    try:
        conn = get_db_connection()
        
        cur = conn.cursor()
        
        user_id = data.get('user_id')
        username = data.get('username')
        password = data.get('password')
        
        if not all([user_id, username, password]):
            return jsonify({"error": "All fields are required to add a new user"}), 400
        
        query = "INSERT INTO User (UserID, Username, Password) VALUES (%s, %s, %s)"
        params = (user_id, username, password)
        
        cur.execute(query, params)
        conn.commit()
        
        return jsonify({"message": f"New user '{username}' added successfully"}), 201
    
    except mysql.connector.Error as e:
        error_message = f"Database connection failed: {e}"
        if conn.is_connected():
            cur.close()
        conn.close()
        return jsonify({"error": error_message}), 500
    
    finally:
        pass

## DELETE USER
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        username = request.args.get('username')
        password = request.args.get('password')

        conn.start_transaction(isolation_level='SERIALIZABLE')

        cursor.execute("SELECT UserID FROM User WHERE Username = %s AND Password = %s", (username, password))
        result = cursor.fetchone()
        if not result:
            return jsonify({"message": "User not found or incorrect credentials"}), 404

        user_id = result[0]

        cursor.execute(
            "DELETE FROM BookReference WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = %s)", (user_id,)
        )
        cursor.execute(
            "DELETE FROM PeopleReference WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = %s)", (user_id,)
        )
        cursor.execute(
            "DELETE FROM CompanyReference WHERE PodcastID IN (SELECT PodcastID FROM Podcast WHERE UserID = %s)", (user_id,)
        )

        cursor.execute("DELETE FROM Podcast WHERE UserID = %s", (user_id,))

        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))

        conn.commit()
        return jsonify({"message": "User and associated data deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

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
    

@app.route("/valid_user", methods=['POST'])
def valid_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        conn = get_db_connection()
        
        cur = conn.cursor()
        
        query = "SELECT * FROM User WHERE username=%s AND password=%s"
        params = (username, password)
        
        cur.execute(query, params)
        result = cur.fetchone()
        
        if result:
            return jsonify({
                "success": True,  
                "message": f"Welcome back, {username}!",
                "id": result[0],
                "role": result[1]
            }), 200
        else:
            return jsonify({
                "success": False,  
                "error": "Invalid username or password"
            }), 401

        
    except mysql.connector.Error as e:
        error_message = f"Database connection failed: {e}"
        if conn.is_connected():
            cur.close()
        conn.close()
        return jsonify({"error": error_message}), 500
    
    finally:
        pass


"""Enter your Gemini API Key."""
genai.configure(api_key="")
def get_youtube_id(url):
    video_id = url.split("v=")[1]
    ampersand_pos = video_id.find("&")
    if ampersand_pos != -1:
        video_id = video_id[:ampersand_pos]
    return video_id

def get_transcript(video_id):
    try:
        print(f"Fetching transcript for video: {video_id}")  
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


def analyze_transcript(transcript):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following transcript and extract the names of all books, companies, and people mentioned. 
    
    Format the output in this EXACT manner:
    
    Books: [book1, book2, book3]
    Companies: [company1, company2, company3]
    People: [person1, person2, person3]

    Transcript: {transcript}
    """
    response = model.generate_content(prompt)
    return response.text

def parse_results(results):
    books, companies, people = [], [], []
    for line in results.split('\n'):
        if line.startswith("Books:"):
            books = extract_items(line)
        elif line.startswith("Companies:"):
            companies = extract_items(line)
        elif line.startswith("People:"):
            people = extract_items(line)
    return books, companies, people

def extract_items(line):
    items = line.split(":")[1].strip()[1:-1].split(', ')
    return [item.strip("'") for item in items if item]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    youtube_url = data.get('url')
    video_id = get_youtube_id(youtube_url)
    transcript = get_transcript(video_id)
    if transcript:
        results = analyze_transcript(transcript)
        books, companies, people = parse_results(results)
        return jsonify({'books': books, 'companies': companies, 'people': people})
    else:
        return jsonify({'error': 'Unable to process the podcast.'}), 400
    
@app.route('/check_db_for_string', methods=['POST'])
def check_db():
    data = request.json
    string = data.get('entity')
    ty = data.get('type')
    conn = get_db_connection()
    cursor = conn.cursor()

    if not string:
        return jsonify({"error": "Input string cannot be empty"}), 400
    
    if ty == 'companies':
        query = """
            SELECT *  
            FROM Companies
            WHERE CompanyName = """ + "\"" + string + "\"" 
    elif ty == 'people':
        query = """
            SELECT *
            FROM People
            WHERE PersonName = """ + "\"" + string + "\""
    else:
        query = """
            SELECT *
            FROM Books
            WHERE BookName = """ + "\"" + string + "\""
        
    if ty == "people":
        cursor.execute(query)
        result = cursor.fetchmany()

        if result:
            # result = list(result)
            # result[2] = str(result[2]) + " State"
            # result[3] = str(result[3]) + " Million Networth"
            result = list(result[0][1:])
            result[1] = str(result[1]) + "  Million Networth"
            
            return jsonify({"message": "found", "result": result}), 200
        else:
            return jsonify({"message": "not found"}), 404

    cursor.execute(query)
    result = cursor.fetchone()

    if conn.is_connected():
        cursor.close()
    conn.close()


    if result:
        if ty == 'companies':
            result = list(result)
            result[2] = str(result[2]) + " State"
            result[3] = str(result[3]) + " Million Networth"
            
            return jsonify({"message": "found", "result": result[1:]}), 200
        elif ty == 'people':
            return jsonify({"message": "found", "result": result[1:]}), 200
        else:
            result = list(result)
            result[3] = str(result[3]) + " Rating"
            return jsonify({"message": "found", "result": result[1:]}), 200
    else:
        return jsonify({"message": "not found"}), 404



if __name__ == '__main__':
    app.run(port=8000, debug=True)
