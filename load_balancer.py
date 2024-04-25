from flask import Flask, request, jsonify
from consistent_hash import ConsistentHash
import docker

app = Flask(__name__)
client = docker.from_env()

# Initialize the consistent hash
consistent_hash = ConsistentHash()

# List of server containers
server_containers = []

# Endpoint to get the status of replicas
@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = [container.name for container in server_containers]
    return jsonify({"replicas": len(replicas), "hostnames": replicas})

# Endpoint to add new server instances
@app.route('/add', methods=['POST'])
def add_servers():
    payload = request.get_json()
    num_servers = payload.get('num_servers')
    hostnames = payload.get('hostnames', [])

    for _ in range(num_servers):
        hostname = hostnames.pop() if hostnames else None
        container = client.containers.run("server-image", hostname=hostname, detach=True)
        server_containers.append(container)

    return jsonify({"message": f"{num_servers} server instances added"})

# Endpoint to remove server instances
@app.route('/rm', methods=['DELETE'])
def remove_servers():
    payload = request.get_json()
    num_servers = payload.get('num_servers')
    hostnames = payload.get('hostnames', [])

    for _ in range(num_servers):
        if hostnames:
            hostname = hostnames.pop()
            container = next((c for c in server_containers if c.name == hostname), None)
        else:
            container = server_containers.pop()

        if container:
            container.stop()
            container.remove()

    return jsonify({"message": f"{num_servers} server instances removed"})

# Endpoint to route requests to server replicas
@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    request_id = hash(path)
    server_id = consistent_hash.get_server(request_id)
    server_container = server_containers[server_id]
    response = server_container.containers.get(f"http://{server_container.name}:5000/{path}")
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)