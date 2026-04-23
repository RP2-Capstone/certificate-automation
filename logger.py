import csv
import os
from datetime import datetime

LOG_FILE = "delivery_logs.csv"

def log_email(name, email, cert_paths, status, error_msg=""):
    file_exists = os.path.isfile(LOG_FILE)

    #Remove None values
    cert_paths = [str(path) for path in cert_paths if path]

    #Handle empty case
    cert_paths_str = "; ".join(cert_paths) if cert_paths else "No Certificates"

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name",
                "Email",
                "Certificate Path",
                "Status",
                "Timestamp",
                "Error Message"
            ])

        writer.writerow([
            name,
            email,
            cert_paths_str,
            status,
            datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
            error_msg
        ])