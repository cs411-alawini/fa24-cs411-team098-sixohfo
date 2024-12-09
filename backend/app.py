# app.py
import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes (allow requests from any origin)
CORS(app, origins=["http://localhost:3000"])

# # Set up Gemini API
# genai.configure(api_key="AIzaSyDMe6QJjtX4L4_IH8FRmrMqsHrwc5FCNbY")
# def get_youtube_id(url):
#     video_id = url.split("v=")[1]
#     ampersand_pos = video_id.find("&")
#     if ampersand_pos != -1:
#         video_id = video_id[:ampersand_pos]
#     return video_id

# def get_transcript(video_id):
#     try:
#         print(f"Fetching transcript for video: {video_id}")  # Debugging line
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         return " ".join([entry['text'] for entry in transcript])
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None


# def analyze_transcript(transcript):
#     model = genai.GenerativeModel('gemini-pro')
#     prompt = f"""
#     Analyze the following transcript and extract the names of all books, companies, and people mentioned. 
    
#     Format the output in this EXACT manner:
    
#     Books: [book1, book2, book3]
#     Companies: [company1, company2, company3]
#     People: [person1, person2, person3]

#     Transcript: {transcript}
#     """
#     response = model.generate_content(prompt)
#     return response.text

# def parse_results(results):
#     books, companies, people = [], [], []
#     for line in results.split('\n'):
#         if line.startswith("Books:"):
#             books = extract_items(line)
#         elif line.startswith("Companies:"):
#             companies = extract_items(line)
#         elif line.startswith("People:"):
#             people = extract_items(line)
#     return books, companies, people

# def extract_items(line):
#     items = line.split(":")[1].strip()[1:-1].split(', ')
#     return [item.strip("'") for item in items if item]

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     print("hello")
#     data = request.get_json()
#     youtube_url = data.get('url')
#     video_id = get_youtube_id(youtube_url)
#     transcript = get_transcript(video_id)
#     if transcript:
#         results = analyze_transcript(transcript)
#         books, companies, people = parse_results(results)
#         return jsonify({'books': books, 'companies': companies, 'people': people})
#     else:
#         return jsonify({'error': 'Unable to process the podcast.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
