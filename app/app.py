from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/buildings/suggest", methods=["GET"])
def suggest_buildings():
    """Return a list of building names that match the user's query (for autocomplete)."""
    query = request.args.get("query", "")
    conn = get_db()
    rows = conn.execute("""
        SELECT DISTINCT building
        FROM database
        WHERE building LIKE ?
        ORDER BY building
        LIMIT 10
    """, (f"%{query}%",)).fetchall()
    conn.close()

    suggestions = [row["building"] for row in rows]
    return jsonify(suggestions)

@app.route("/free_rooms", methods=["GET"])
def get_free_rooms():
    day = request.args.get("day")
    time = request.args.get("time")
    building_filter = request.args.get("building")

    conn = get_db()
    query_busy = """
        SELECT DISTINCT building, room_number
        FROM database
        WHERE days LIKE '%' || ? || '%'
            AND start_time <= ?
            AND end_time >= ?
    """ 
    params_busy = [day, time, time]

    if building_filter and building_filter.strip():
        query_busy += " AND building = ?"
        params_busy.append(building_filter.strip())

    busy_rooms = conn.execute(query_busy, params_busy).fetchall()
    busy_rooms_set = {(row["building"], row["room_number"]) for row in busy_rooms}
    
    query_all = """
        SELECT DISTINCT building, room_number
        FROM database
    """
    params_all = []

    if building_filter and building_filter.strip():
        query_all += " WHERE building = ?"
        params_all.append(building_filter.strip())

    all_rooms = conn.execute(query_all, params_all).fetchall()
    conn.close()

    all_rooms_set = {(row["building"], row["room_number"]) for row in all_rooms}

    free_rooms_set = all_rooms_set - busy_rooms_set

    free_rooms = []
    for (bldg, rm) in free_rooms_set:
        free_rooms.append({"building": bldg, "room_number": rm})

    return jsonify(free_rooms)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)