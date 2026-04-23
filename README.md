# 🎓 Automatic Certificate Generation System

A Flask-based web application that automates the process of generating, verifying, and emailing certificates (Completion & Experience) using data from Google Sheets.



## Features

*  Generate **Completion Certificates**
*  Generate **Experience Certificates**
*  Fetch and process data from **Google Sheets**
*  Send certificates via email
*  Verification system before sending
*  Store certificates locally
*  Maintain delivery logs (CSV)
*  Simple dashboard interface



## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML
* **Data Source:** Google Sheets API
* **PDF Generation:** ReportLab
* **Email Service:** SMTP



## Workflow

1. Fetch data from Google Sheets
2. Process user records
3. Generate certificates (PDF)
4. Display in dashboard
5. Verify certificate
6. Send via email
7. Log status in CSV



## 📌 Notes

* Certificates are stored in the `certificates/` folder (not uploaded to GitHub)
* Logs are stored in `delivery_logs.csv`
* Ensure Google Sheets API credentials are properly configured
