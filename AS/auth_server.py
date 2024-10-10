import socket
import json

DNS_RECORD_FILE = "dns_records.json"

# Helper function to store DNS records in a file
def store_dns_record(hostname, ip_address, ttl):
    try:
        with open(DNS_RECORD_FILE, 'r') as f:
            dns_records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dns_records = {}
    
    dns_records[hostname] = {"ip": ip_address, "ttl": ttl}
    
    with open(DNS_RECORD_FILE, 'w') as f:
        json.dump(dns_records, f)

# Helper function to look up DNS records
def lookup_dns_record(hostname):
    try:
        with open(DNS_RECORD_FILE, 'r') as f:
            dns_records = json.load(f)
        return dns_records.get(hostname)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# UDP server to handle DNS registration and query requests
def run_authoritative_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53533))
    
    print("Authoritative DNS server listening on port 53533")
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        lines = message.strip().split("\n")
        
        # Parse message to differentiate between registration and query
        msg_type = lines[0].split("=")[1]
        hostname = lines[1].split("=")[1]
        
        if msg_type == "A" and "VALUE" in lines[2]:
            # Registration request
            ip_address = lines[2].split("=")[1]
            ttl = lines[3].split("=")[1]
            store_dns_record(hostname, ip_address, ttl)
            print(f"Registered: {hostname} -> {ip_address} with TTL {ttl}")
        
        elif msg_type == "A":
            # DNS query request
            record = lookup_dns_record(hostname)
            if record:
                response = f"TYPE=A\nNAME={hostname}\nVALUE={record['ip']}\nTTL={record['ttl']}\n"
                sock.sendto(response.encode(), addr)
            else:
                response = "DNS record not found"
                sock.sendto(response.encode(), addr)

if __name__ == '__main__':
    run_authoritative_server()
