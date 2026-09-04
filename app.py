from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "smart-parking-secret"

# Demo parking slots
slots = [
    {"id": 1, "name": "A1", "status": "Available"},
    {"id": 2, "name": "A2", "status": "Available"},
    {"id": 3, "name": "A3", "status": "Available"},
    {"id": 4, "name": "A4", "status": "Available"},
    {"id": 5, "name": "B1", "status": "Available"},
    {"id": 6, "name": "B2", "status": "Available"},
    {"id": 7, "name": "B3", "status": "Available"},
    {"id": 8, "name": "B4", "status": "Available"}
]

bookings = []


@app.route("/")
def index():
    return render_template("index.html", slots=slots)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        session["user"] = name
        session["email"] = email

        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        session["user"] = name

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user=session["user"],
        slots=slots,
        bookings=bookings
    )


@app.route("/parking-slots")
def parking_slots():
    return render_template("parking-slots.html", slots=slots)


@app.route("/booking/<int:slot_id>", methods=["GET", "POST"])
def booking(slot_id):
    slot = next((s for s in slots if s["id"] == slot_id), None)

    if slot is None:
        return "Parking slot not found"

    if request.method == "POST":
        if slot["status"] == "Occupied":
            return "Slot is already occupied"

        vehicle = request.form["vehicle"]
        date = request.form["date"]
        time = request.form["time"]

        slot["status"] = "Occupied"

        bookings.append({
            "slot": slot["name"],
            "vehicle": vehicle,
            "date": date,
            "time": time,
            "user": session.get("user", "Guest")
        })

        return redirect(url_for("dashboard"))

    return render_template("booking.html", slot=slot)


@app.route("/cancel/<slot_name>")
def cancel_booking(slot_name):
    for slot in slots:
        if slot["name"] == slot_name:
            slot["status"] = "Available"

    global bookings
    bookings = [b for b in bookings if b["slot"] != slot_name]

    return redirect(url_for("dashboard"))


@app.route("/admin")
def admin():
    return render_template("admin.html", slots=slots, bookings=bookings)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)