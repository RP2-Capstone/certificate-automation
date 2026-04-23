import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

#function to get data from the google sheet

def connect_sheet():
    #defining the scope of the application
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    #Loading the credentials from the JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    #Authorizing the client
    client = gspread.authorize(creds)

    sheet = client.open("Student Data").sheet1
    return sheet

#Adding End date to the google sheet

def update_end_dates(sheet):
      data = sheet.get_all_records()

      for i, row in enumerate(data, start=2):
            start_date = row["Start Date"]
            duration = row["Duration(months)"]
            end_date = row["End Date"]

            if not end_date:
                  try:      
                        start = datetime.strptime(start_date, "%d/%m/%Y")
                        duration_months = int(duration)
                        end = start + timedelta(days = duration_months * 30)

                        sheet.update_cell(i,7, end.strftime("%d/%m/%Y"))


                  except Exception as e:
                        print(f"Error in row{i}:{e}")      
      print("End dates updated successfully.")
      return sheet.get_all_records()  # Return updated data 


def update_status(emp_id, new_status):
    sheet = connect_sheet()
    data = sheet.get_all_records()

    for i, row in enumerate(data, start=2):  # row 2 = first data row
        if str(row.get("Emp ID")) == str(emp_id):
            status_col = list(row.keys()).index("Status") + 1
            sheet.update_cell(i, status_col, new_status)
            print(f"Updated status for {emp_id} → {new_status}")
            break