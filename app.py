from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "ak_0cplurm6gxeovhk8q32qavz3"
EMAIL = "23f3000717@ds.study.iitm.ac.in"  

@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "X-API-Key, Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return resp

@app.route("/analytics", methods=["POST", "OPTIONS"])
def analytics():
    if request.method == "OPTIONS":
        return "", 204

    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    events = data.get("events", [])

    total_events = len(events)
    users = set()
    revenue = 0.0
    user_totals = {}

    for e in events:
        user = e.get("user")
        amount = e.get("amount", 0) or 0
        if user is not None:
            users.add(user)
        if amount > 0:
            revenue += amount
            user_totals[user] = user_totals.get(user, 0.0) + amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return jsonify({
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": round(revenue, 2),
        "top_user": top_user
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)