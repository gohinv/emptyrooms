from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/free_rooms", methods=["GET"])
def get_free_rooms():
    day = request.args.get("day")
    time = request.args.get("time")

    conn = get_db()
    busy_rooms = conn.execute('''
        SELECT DISTINCT building, room_number
        FROM database
        WHERE days LIKE '%' || ? || '%'
            AND start_time <= ?
            AND end_time >= ?
    ''', (day, time, time)).fetchall()
    
    all_rooms = conn.execute("""
        SELECT DISTINCT building, room_number
        FROM database
    """).fetchall()
    
    conn.close()

    busy_rooms_set =  {(row['building'], row['room_number']) for row in busy_rooms}
    all_rooms_set = {(row['building'], row['room_number']) for row in all_rooms}

    free_rooms_set = all_rooms_set - busy_rooms_set
    free_rooms = [{"building": b, "room_number": r} for (b, r) in free_rooms_set]

    return jsonify(free_rooms)


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)