from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_data(query):
    conn = sqlite3.connect("spotify_data.db")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/api/top-tracks")
def top_tracks():
    query = "SELECT name, artist, popularity FROM tracks DESC LIMIT 50"
    data = get_data(query=query)
    return jsonify([{"name": t[0], "artist": t[1], "popularity": t[2]} for t in data])

@app.route("/")
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)