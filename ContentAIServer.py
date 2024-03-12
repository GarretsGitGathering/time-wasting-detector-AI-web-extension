from flask import Flask, request, jsonify  # Import Flask and other necessary modules
import socket  # Import socket module for TCP communication
import threading  # Import threading module for concurrent execution

app = Flask(__name__)  # Initialize Flask app

def process_prediction(data):
    """Function to process prediction data"""
    return data  # Placeholder function, replace with actual implementation

def tcp_listener():
    """Function to start TCP listener"""
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 55565  # TCP port to listen on

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
    tcp_server.bind((host, port))  # Bind socket to host and port
    tcp_server.listen(5)  # Listen for incoming connections with backlog of 5

    print(f"TCP server listening on {host}:{port}")  # Print message indicating server is listening

    while True:
        client_socket, client_address = tcp_server.accept()  # Accept incoming connection
        print(f"Connection from {client_address}")  # Print message indicating new connection

        data = client_socket.recv(1024).decode("utf-8")  # Receive data from client
        print(f"Received data: {data}")  # Print received data

        processed_data = process_prediction(data)  # Process received data

        client_socket.send(processed_data.encode("utf-8"))  # Send processed data back to client

        client_socket.close()  # Close client socket after communication is complete

def start_flask_server():
    """Function to start Flask server"""
    print("Starting Flask server...")  # Print message indicating Flask server is starting
    app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=5000)  # Start Flask app

@app.route('/', methods=['POST'])  # Define route for handling POST requests
def handle_request():
    """Function to handle POST requests"""
    data = request.get_data(as_text=True)  # Get request data
    processed_data = process_prediction(data)  # Process request data
    return jsonify({'result': processed_data})  # Return processed data as JSON response

if __name__ == '__main__':
    flask_server_thread = threading.Thread(target=start_flask_server)  # Create thread for Flask server
    flask_server_thread.start()  # Start Flask server thread

    tcp_thread = threading.Thread(target=tcp_listener)  # Create thread for TCP listener
    tcp_thread.start()  # Start TCP listener thread
