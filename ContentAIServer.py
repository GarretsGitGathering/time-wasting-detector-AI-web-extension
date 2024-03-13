from flask import Flask, request, jsonify  # Import Flask and other necessary modules
import socket  # Import socket module for TCP communication
import threading  # Import threading module for concurrent execution
import json

from askGPTContent import determine_timewasting_percentage

app = Flask(__name__)  # Initialize Flask app

def process_prediction(data):
    """Function to process prediction data"""

    #seperate data into seperate parts, data = {"title": "cool_title", "parsed_data": "some_data", "url": "https://youtube.com/8719879"}
    try:
        data_dict = json.loads(data)
        title = data_dict.get("title")
        parsed_data = data_dict.get("parsed_data")
        url = data_dict.get("url")
    except json.JSONDecodeError:
        return "Invalid JSON format"

    status = determine_timewasting_percentage(title, parsed_data, url)

    return status  # Placeholder function, replace with actual implementation

def start_flask_server():
    """Function to start Flask server"""
    print("Starting Flask server...")  # Print message indicating Flask server is starting
    app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=55570)  # Start Flask app

@app.route('/', methods=['POST'])  # Define route for handling POST requests
def handle_request():
    """Function to handle POST requests"""
    data = request.get_data(as_text=True)  # Get request data
    print("data: "+data)

    print("-------------------------------")

    print("PROCESSING DATA")
    processed_status = process_prediction(data)  # Process request data
    print("prediction: "+processed_status)

    print("-------------------------------")

    print("SENDING STATUS BACK TO CLIENT")
    json_prediction = jsonify({'result': processed_status})
    return json_prediction  # Return processed data as JSON response

if __name__ == '__main__':
    flask_server_thread = threading.Thread(target=start_flask_server)  # Create thread for Flask server
    flask_server_thread.start()  # Start Flask server thread
