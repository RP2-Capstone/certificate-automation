from flask import Flask, render_template, redirect, send_from_directory
from email_service import send_email
from certificate_generator import generate_certificate
from experience_certificate import experience_certificate
from data_processor import fetch_and_process
from sheets import update_status
from logger import log_email 
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(BASE_DIR, "certificates")

os.makedirs(CERT_DIR, exist_ok=True)

current_date = datetime.now().strftime("%d-%b-%Y")

#Data
def load_records():
    df = fetch_and_process()

    records = []

    for _, row in df.iterrows():
        record = {
            "Emp ID": row.get("Emp ID"),
            "Name": row.get("Name"),
            "Email": row.get("Email") or row.get("email"),
            "Course Name": row.get("Course Name"),
            "Start Date": row.get("Start Date"),
            "End Date": row.get("End Date"),
            "Duration": row.get("Duration(months)"),
            "Status": str(row.get("Status", "PENDING")).strip().upper()
        }

        records.append(record)

    return records

# Dashboard
@app.route('/')
def dashboard():
    records = load_records()
    return render_template('dashboard.html', records=records)


# View PDF Files
@app.route('/view/<id>/<type>')
def view_pdf(id, type):
    records = load_records()

    for record in records:
        if str(record["Emp ID"]) == str(id):

            if type == "completion":
                filepath = os.path.join(CERT_DIR, f"completion_{id}.pdf")
                if not os.path.exists(filepath):
                    generate_certificate(
                        record["Name"],
                        record["Course Name"],
                        record["Start Date"],
                        record["End Date"],
                        filepath
                    )

            elif type == "experience":
                filepath = os.path.join(CERT_DIR, f"experience_{id}.pdf")

                if not os.path.exists(filepath):
                    experience_certificate(
                        current_date,
                        record["Emp ID"],
                        record["Name"],
                        record["Course Name"],
                        record["Start Date"],
                        record["End Date"],
                        filepath
                    )

            return send_from_directory(CERT_DIR, os.path.basename(filepath))

    return "File not found"

# VERIFY
@app.route('/verify/<id>')
def verify(id):
    records = load_records()

    for record in records:
        if str(record["Emp ID"]) == str(id):

            if record["Status"] in ["PENDING", "VERIFIED"]:

                completion_path = os.path.join(CERT_DIR, f"completion_{id}.pdf")
                experience_path = os.path.join(CERT_DIR, f"experience_{id}.pdf")

                # Ensure files exist
                if not os.path.exists(completion_path):
                    generate_certificate(
                        record["Name"],
                        record["Course Name"],
                        record["Start Date"],
                        record["End Date"],
                        completion_path
                    )

                if not os.path.exists(experience_path):
                    experience_certificate(
                        current_date,
                        record["Emp ID"],
                        record["Name"],
                        record["Course Name"],
                        record["Start Date"],
                        record["End Date"],
                        experience_path
                    )

                try:
                    send_email(
                        record["Name"],
                        record["Email"],
                        [completion_path, experience_path]
                    )

                    log_email(
                        record["Name"],
                        record["Email"],
                        [completion_path, experience_path],
                        "SENT"
                    )

                    update_status(record["Emp ID"], "SENT")

                except Exception as e:
                    print("Email failed:", e)

                    log_email(
                        record["Name"],
                        record["Email"],
                        [completion_path, experience_path],
                        "FAILED",
                        str(e)
                    )

            break

    return redirect('/')


# REJECT
@app.route('/reject/<id>')
def reject(id):
    records = load_records()

    for record in records:
        if str(record["Emp ID"]) == str(id):
            if record["Status"] != "SENT":

                update_status(record["Emp ID"], "REJECTED")

                log_email(
                    record["Name"],
                    record["Email"],
                    [],
                    "REJECTED"
                )

            break

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)