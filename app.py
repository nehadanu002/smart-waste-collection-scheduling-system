
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart-waste-demo-key"

DB_PATH = Path(__file__).with_name("waste_management.db")

# Demo campus coordinates (x, y)
COORDS = {
    "Library Gate": (1, 2),
    "Hostel Block A": (4, 1),
    "Cafeteria": (3, 4),
    "Academic Block": (2, 5),
    "Sports Ground": (6, 4),
    "Main Entrance": (0, 0),
}


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS bins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bin_code TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL,
            fill_level INTEGER NOT NULL,
            capacity_liters INTEGER NOT NULL DEFAULT 240,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bin_id INTEGER NOT NULL,
            scheduled_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            route_order INTEGER,
            FOREIGN KEY(bin_id) REFERENCES bins(id)
        );
        """)

        count = db.execute(
            "SELECT COUNT(*) FROM bins"
        ).fetchone()[0]

        if count == 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            sample_bins = [
                ("BIN-101", "Library Gate", 92, 240, now),
                ("BIN-102", "Hostel Block A", 68, 240, now),
                ("BIN-103", "Cafeteria", 97, 360, now),
                ("BIN-104", "Academic Block", 35, 240, now),
                ("BIN-105", "Sports Ground", 76, 360, now),
                ("BIN-106", "Main Entrance", 18, 240, now),
            ]

            db.executemany("""
                INSERT INTO bins
                (bin_code, location, fill_level,
                 capacity_liters, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, sample_bins)


def get_bins():
    with connect_db() as db:
        rows = db.execute(
            "SELECT * FROM bins ORDER BY fill_level DESC"
        ).fetchall()

    bins = []
    for row in rows:
        item = dict(row)
        fill = item["fill_level"]

        if fill >= 85:
            priority = "Critical"
        elif fill >= 60:
            priority = "High"
        elif fill >= 35:
            priority = "Medium"
        else:
            priority = "Low"

        item["priority"] = priority
        bins.append(item)

    return bins


def schedule_collections():
    # GREEDY ALGORITHM:
    # Prioritize bins with the highest fill level.
    bins = [
        b for b in get_bins()
        if b["fill_level"] >= 35
    ]

    bins.sort(
        key=lambda b: (-b["fill_level"], b["id"])
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with connect_db() as db:
        # Regenerate pending records but retain completed history.
        db.execute(
            "DELETE FROM collections WHERE status = 'Pending'"
        )

        for order, bin_data in enumerate(bins, start=1):
            db.execute("""
                INSERT INTO collections
                (bin_id, scheduled_at, status, route_order)
                VALUES (?, ?, 'Pending', ?)
            """, (bin_data["id"], now, order))

    return bins


def manhattan_distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])


def optimize_route(bins):
    # GREEDY NEAREST-NEIGHBOUR HEURISTIC
    remaining = []

    for b in bins:
        x, y = COORDS.get(b["location"], (0, 0))
        remaining.append({**b, "x": x, "y": y})

    current = {"x": 0, "y": 0}
    route = []
    total_distance = 0

    while remaining:
        next_bin = min(
            remaining,
            key=lambda b: (
                manhattan_distance(current, b),
                -b["fill_level"]
            )
        )

        total_distance += manhattan_distance(current, next_bin)
        route.append(next_bin)
        current = next_bin
        remaining.remove(next_bin)

    return route, total_distance


@app.route("/")
def dashboard():
    bins = get_bins()

    with connect_db() as db:
        pending = db.execute("""
            SELECT COUNT(*) FROM collections
            WHERE status = 'Pending'
        """).fetchone()[0]

        completed = db.execute("""
            SELECT COUNT(*) FROM collections
            WHERE status = 'Completed'
        """).fetchone()[0]

    return render_template(
        "index.html",
        bins=bins,
        total=len(bins),
        critical=sum(b["fill_level"] >= 85 for b in bins),
        pending=pending,
        completed=completed
    )


@app.route("/bins/add", methods=["POST"])
def add_bin():
    code = request.form.get("bin_code", "").strip().upper()
    location = request.form.get("location", "").strip()

    try:
        fill = int(request.form.get("fill_level", "0"))
        capacity = int(request.form.get("capacity_liters", "240"))

        if not code or not location:
            raise ValueError

        if not 0 <= fill <= 100 or capacity <= 0:
            raise ValueError

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        with connect_db() as db:
            db.execute("""
                INSERT INTO bins
                (bin_code, location, fill_level,
                 capacity_liters, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (code, location, fill, capacity, now))

        flash("Bin added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("Bin code already exists.", "error")
    except ValueError:
        flash("Enter valid bin details.", "error")

    return redirect(url_for("dashboard"))


@app.route("/bins/<int:bin_id>/update", methods=["POST"])
def update_bin(bin_id):
    try:
        fill = int(request.form.get("fill_level", "-1"))

        if not 0 <= fill <= 100:
            raise ValueError

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        with connect_db() as db:
            db.execute("""
                UPDATE bins
                SET fill_level = ?, updated_at = ?
                WHERE id = ?
            """, (fill, now, bin_id))

        flash("Fill level updated.", "success")

    except ValueError:
        flash("Fill level must be between 0 and 100.", "error")

    return redirect(url_for("dashboard"))


@app.route("/schedule", methods=["GET", "POST"])
def schedule_page():
    if request.method == "POST":
        scheduled = schedule_collections()
        flash(
            f"Schedule generated for {len(scheduled)} bins.",
            "success"
        )
        return redirect(url_for("schedule_page"))

    with connect_db() as db:
        collections = db.execute("""
            SELECT c.id AS collection_id,
                   c.scheduled_at, c.status, c.route_order,
                   b.bin_code, b.location, b.fill_level
            FROM collections c
            JOIN bins b ON b.id = c.bin_id
            ORDER BY
                CASE c.status WHEN 'Pending' THEN 0 ELSE 1 END,
                c.route_order
        """).fetchall()

    return render_template(
        "schedule.html", collections=collections
    )


@app.route("/route")
def route_page():
    bins = [
        b for b in get_bins()
        if b["fill_level"] >= 35
    ]

    route, total_distance = optimize_route(bins)

    return render_template(
        "route.html",
        route=route,
        total_distance=total_distance
    )


@app.route("/collections/<int:collection_id>/complete",
           methods=["POST"])
def complete_collection(collection_id):
    with connect_db() as db:
        record = db.execute("""
            SELECT bin_id, status FROM collections
            WHERE id = ?
        """, (collection_id,)).fetchone()

        if record is None:
            flash("Collection record not found.", "error")

        elif record["status"] == "Completed":
            flash("This collection is already complete.", "error")

        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            db.execute("""
                UPDATE collections
                SET status = 'Completed'
                WHERE id = ?
            """, (collection_id,))

            db.execute("""
                UPDATE bins SET fill_level = 0, updated_at = ?
                WHERE id = ?
            """, (now, record["bin_id"]))

            flash("Collection completed!", "success")

    return redirect(url_for("schedule_page"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
