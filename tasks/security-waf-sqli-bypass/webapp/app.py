from flask import Flask, request, jsonify
import sqlite3
import sys

app = Flask(__name__)

# Hardcoded flag - stored only in database, not accessible in source
FLAG = "FLAG{W4F_Ev4s10n_M4st3ry_Ach13v3d}"


def db_init():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    c.execute("INSERT INTO users VALUES (1, 'alice'), (2, 'bob')")
    c.execute("DROP TABLE IF EXISTS secrets")
    c.execute("CREATE TABLE secrets (key TEXT, value TEXT)")
    c.execute("INSERT INTO secrets VALUES ('flag', ?)", (FLAG,))
    conn.commit()
    conn.close()


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "1")
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    try:
        # VULNERABILITY: Direct string interpolation in SQL query (blind SQLi)
        query = f"SELECT name FROM users WHERE id = {user_id}"

        # Log all SQL queries for anti-cheat verification
        with open("/logs/webapp_queries.log", "a") as log:
            log.write(f"{query}\n")

        c.execute(query)
        result = c.fetchone()
        return jsonify({"name": result[0] if result else "not found"})
    except Exception as e:
        with open("/logs/webapp_queries.log", "a") as log:
            log.write(f"ERROR: {str(e)}\n")
        return jsonify({"name": "not found"}), 200


if __name__ == "__main__":
    db_init()
    print("INFO: Database initialized", file=sys.stderr, flush=True)
    app.run(host="0.0.0.0", port=8080)
