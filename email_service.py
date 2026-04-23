import smtplib
from email.message import EmailMessage
import os

def send_email(name, email, file_paths):
      msg = EmailMessage()
      msg['Subject'] = "Certificates Approved"
      msg['From'] = "adhiltest99@gmail.com"
      msg['To'] = email

      msg.set_content(f"Hello {name},\n\nYour certificates has been approved.")
      
      #Attach multiple File
      for file_path in file_paths:
            with open(file_path, 'rb') as f:
                  file_name = os.path.basename(file_path)
                  msg.add_attachment(
                        f.read(), 
                        maintype='application',
                        subtype='pdf',  
                        filename=file_name
                        )

      #Connect to Gmail Server
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("adhiltest99@gmail.com", "rnai ovjx mebm tjgr")
            smtp.send_message(msg)


