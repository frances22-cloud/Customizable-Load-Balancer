from flask import Flask

app = Flask(__name__)

# Server ID (to be set as an environment variable)
server_id = None

@app.route('/home', methods=['GET'])
def home():
    return f"Hello from Server: {server_id}"

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "", 200

if __name__ == '__main__':
    # Get the server ID from the environment variable
    server_id = os.environ.get('SERVER_ID')
    if not server_id:
        print("SERVER_ID environment variable not set")
        exit(1)

    app.run(host='0.0.0.0', port=5000)