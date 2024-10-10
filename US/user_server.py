from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if all required parameters are provided
    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return "Bad Request - Missing parameters", 400

    try:
        # Query the Authoritative Server (AS) to get the IP address of the Fibonacci Server
        as_url = f'http://{as_ip}:{as_port}/resolve?hostname={hostname}'
        response = requests.get(as_url)
        if response.status_code != 200:
            return "Failed to resolve hostname", 500

        fs_ip = response.json().get('ip')
        if not fs_ip:
            return "Fibonacci server IP not found", 500

        # Now query the Fibonacci Server for the Fibonacci number
        fs_url = f'http://{fs_ip}:{fs_port}/fibonacci?number={number}'
        fibonacci_response = requests.get(fs_url)
        if fibonacci_response.status_code != 200:
            return "Fibonacci server error", 500

        return jsonify(fibonacci_response.json()), 200

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
