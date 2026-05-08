from flask import Flask, render_template, request, redirect, url_for
import os

from database import create_table, insert_record, view_records, delete_record

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------------
# Data
# -----------------------------
MICROSCOPE_TYPES = {
    "Light Microscope": 40,
    "Electron Microscope": 1000,
    "SEM": 5000,
    "TEM": 10000
}

UNIT_TO_METERS = {
    "nm": 1e-9,
    "um": 1e-6,
    "mm": 1e-3,
    "cm": 1e-2,
    "m": 1
}

# -----------------------------
# Home Page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        username = request.form.get("username")
        measured = request.form.get("measured")
        microscope = request.form.get("microscope")
        unit = request.form.get("unit")
        image = request.files.get("image")

        if not username:
            return "Username required"

        try:
            measured = float(measured)
            if measured <= 0:
                return "Invalid measured size"
        except:
            return "Invalid input"

        magnification = MICROSCOPE_TYPES[microscope]

        real_size = measured / magnification
        final_value = real_size / UNIT_TO_METERS[unit]

        # Save image
        if image and image.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filepath)

        # Save to DB
        insert_record(username, measured, real_size)

        result = f"{final_value:.6f} {unit}"

    return render_template(
        "index.html",
        microscopes=MICROSCOPE_TYPES.keys(),
        units=UNIT_TO_METERS.keys(),
        result=result
    )

# -----------------------------
# View Records
# -----------------------------
@app.route("/records")
def records():
    data = view_records()
    return render_template("records.html", records=data)

# -----------------------------
# Delete Record
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):
    delete_record(id)
    return redirect(url_for("records"))


# Create database table
create_table()

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)