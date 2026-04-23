import pandas as pd
from sheets import connect_sheet,update_end_dates


def get_sheet_data():
    """
    Fetch data from Google Sheets and ensure End Dates are updated.
    """
    try:
        sheet = connect_sheet()

        print("Updating missing end dates...")
        data = update_end_dates(sheet)

        return pd.DataFrame(data)
    

    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Using mock data instead.")

        return pd.DataFrame([
            {
                "Name": "john doe",
                "Email": "jannathparveen343@gmail.com",
                "Emp ID": "EMP001",
                "Course Name": "python automation",
                "Start Date": "01/01/2023",
                "Duration(months)": 2,
                "End Date": "01/03/2023"
            }
        ])



def process_data(df):
    """
    Cleans and formats data for certificate generation.
    """
    if df.empty:
        return df

    # Clean column names
    df.columns = df.columns.str.strip()

    # Standardize column names
    rename_map = {
    "Course": "Course Name",
    "Course name": "Course Name", 
    "EmpID": "Emp ID",
    "Employee ID": "Emp ID",
    "email": "Email"
    }
    
    df.rename(columns=rename_map, inplace=True)
    print("Column names standardized.")

    # Ensure required columns exist
    required_cols = ["Name", "Course Name", "Start Date", "End Date", "Duration(months)"]
    for col in required_cols:
        if col not in df.columns:
            print(f"Column '{col}' is missing. Filling with 'Unknown'.")
            df[col] = "Unknown"

    # Optional column
    if "Emp ID" not in df.columns:
        df["Emp ID"] = "N/A"

    # Format text
    df["Name"] = df["Name"].astype(str).str.title()
    df["Course Name"] = df["Course Name"].astype(str).str.title()
    print("Text formatted successfully.")

    # Format dates 
    for col in ["Start Date", "End Date"]:
        df[col] = pd.to_datetime(
            df[col],
            format="%d/%m/%Y",
            errors="coerce"
        ).dt.strftime("%d-%b-%Y")  
        df[col] = df[col].fillna("Unknown Date")


    print("Data processed successfully.")    

    return df




def fetch_and_process():
    df = get_sheet_data()
    return process_data(df)
