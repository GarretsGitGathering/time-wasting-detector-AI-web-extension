from flask import Flask, request, jsonify  # Import Flask and other necessary modules
import threading  # Import threading module for concurrent execution
import json
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO

from askGPTBehaviorLearning import identify_bad_habits

app = Flask(__name__)  # Initialize Flask app
CORS(app)

def start_flask_server():
    """Function to start Flask server"""
    print("Starting Flask server...")  # Print message indicating Flask server is starting
    app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=55575)  # Start Flask app

@app.route('/', methods=['POST'])  # Define route for handling POST requests
def handle_request():
    """Function to handle POST requests"""
    data = request.get_data(as_text=True)  # Get request data
    print("RECEIVED DATA")
    data = data.replace('\\\\\\"', '')
    print("data:" + data)

    print("-------------------------------")

    print("PROCESSING DATA")
    context_status = identify_bad_habits(data)  # Process request data      YOU NEED TO PARSE THE RECEIVED STRING
    print("historical prediction: "+context_status)

    print("-------------------------------")

    print("SENDING STATUS BACK TO CLIENT")
    json_prediction = jsonify({'context prediction': context_status})
    return json_prediction  # Return processed data as JSON response

if __name__ == '__main__':
    flask_server_thread = threading.Thread(target=start_flask_server)  # Create thread for Flask server
    flask_server_thread.start()  # Start Flask server thread
