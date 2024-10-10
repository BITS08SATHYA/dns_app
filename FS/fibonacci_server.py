import json
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fibonacci calculation function
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Registration to Authoritative Server (UDP on port 53533)
def register_to_authoritative_server(hostname, fs_ip, as_ip, as_port):
    # DNS registration message format
    registration_message = f"TYPE=A\nNAME={hostname}\nVALUE={fs_ip}\nTTL=10\n"
    
    # Send the message via UDP to the Authoritative Server
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(registration_message.encode(), (as_ip, int(as_port)))

@app.route('/register', methods=['PUT'])
def register():
    # Parse request body for hostname and IP addresses
    try:
        data = request.json
        hostname = data['hostname']
        fs_ip = data['ip']
        as_ip = data['as_ip']
        as_port = data['as_port']
    except KeyError:
        return "Bad Request - Missing parameters", 400

    # Register the hostname with the Authoritative Server via UDP
    register_to_authoritative_server(hostname, fs_ip, as_ip, as_port)
    
    return "Registered successfully", 201

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    if not number:
        return "Bad Request - Missing number", 400

    try:
        n = int(number)
        if n < 0:
            return "Bad Request - Fibonacci number must be non-negative", 400
        result = fibonacci(n)
        return jsonify({"fibonacci": result}), 200
    except ValueError:
        return "Bad Request - Invalid number format", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)  # Running Fibonacci Server on port 9090