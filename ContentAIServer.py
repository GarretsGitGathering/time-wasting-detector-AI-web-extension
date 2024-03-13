from flask import Flask, request, jsonify  # Import Flask and other necessary modules
import socket  # Import socket module for TCP communication
import threading  # Import threading module for concurrent execution
import json
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO

from askGPTContent import determine_timewasting_percentage, image_classification

app = Flask(__name__)  # Initialize Flask app
CORS(app)

def process_prediction(data):
    """Function to process prediction data"""

    #seperate data into seperate parts, data = {"title": "cool_title", "parsed_data": "some_data", "url": "https://youtube.com/8719879"}
    try:
        data_dict = json.loads(data)
        title = data_dict.get("title")
        parsed_data = data_dict.get("parsed_data")
        url = data_dict.get("url")
        base64_screenshot = data_dict.get("screenshot")
    except json.JSONDecodeError:
        return "Invalid JSON format"

    context_status = determine_timewasting_percentage(title, parsed_data, url)

    data_type, encoded_screenshot = base64_screenshot.split(',', 1)

    decoded_screenshot = base64.b64decode(encoded_screenshot)
    screenshot_status = image_classification(Image.open(BytesIO(decoded_screenshot)))

    return context_status, screenshot_status  # Placeholder function, replace with actual implementation

def start_flask_server():
    """Function to start Flask server"""
    print("Starting Flask server...")  # Print message indicating Flask server is starting
    app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=55570)  # Start Flask app

@app.route('/', methods=['POST'])  # Define route for handling POST requests
def handle_request():
    """Function to handle POST requests"""
    data = request.get_data(as_text=True)  # Get request data
    print("RECEIVED DATA")
    #print("data:" + data)

    print("-------------------------------")

    print("PROCESSING DATA")
    context_status, screenshot_status = process_prediction(data)  # Process request data
    print("context prediction: "+context_status)
    print("screenshot prediction: "+screenshot_status)

    print("-------------------------------")

    print("SENDING STATUS BACK TO CLIENT")
    json_prediction = jsonify({'context prediction': context_status, 'screenshot prediction': screenshot_status})
    return json_prediction  # Return processed data as JSON response

if __name__ == '__main__':
    flask_server_thread = threading.Thread(target=start_flask_server)  # Create thread for Flask server
    flask_server_thread.start()  # Start Flask server thread
