from flask import Flask, jsonify, request
import requests
import sqlite3

app = Flask(__name__)

DATABASE = 'phishing_sites.db'
WHOIS_API_KEY = 'at_c4NP0WsdiHmO0KM2I9NTD8TF17btw' 
WHOIS_API_ENDPOINT = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_c4NP0WsdiHmO0KM2I9NTD8TF17btw&domainName=google.com"

def query_db(query, args=(), one=False):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        if one:
            return rows[0]
        return rows

def add_to_db(query, args=()):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(query, args)
        con.commit()

@app.route('/getblacklist.json', methods=['GET'])
def get_blacklist():
    rows = query_db("SELECT url FROM phishing_sites")
    urls = [row[0] for row in rows]
    return jsonify(urls)

@app.route('/add_to_blacklist', methods=['POST'])
def add_to_blacklist():
    new_url = request.form.get('url')
    if new_url:
        add_to_db("INSERT INTO phishing_sites (url) VALUES (?)", (new_url,))
        # Ideally, you should also update the version in the metadata table here.
        return jsonify({"message": "URL added successfully!"}), 200
    return jsonify({"error": "No URL provided!"}), 400

@app.route('/getDomainAge', methods=['POST'])
def get_domain_age():
    domain = request.form.get('domain')
    if not domain:
        return jsonify({"error": "No domain provided!"}), 400

    params = {
        "apiKey": WHOIS_API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    try:
        response = requests.get(WHOIS_API_ENDPOINT, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors

        data = response.json()
        
        if data and data.get("WhoisRecord") and data["WhoisRecord"].get("createdDate"):
            createdDate = data["WhoisRecord"]["createdDate"]
            age = (int(createdDate.split('-')[0]) - 1970)  # Simplistic calculation, you can enhance this
            return jsonify({"domainAge": age}), 200

        return jsonify({"error": "Unable to retrieve domain age."}), 500

    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # This will print the detailed HTTP error
        return jsonify({"error": str(http_err)}), 500
    except Exception as e:
        print(f'Error occurred: {e}')  # This will print the generic error
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return "This is only for testing the Flask server is Activated."

if __name__ == '__main__':
    app.run(debug=True)
