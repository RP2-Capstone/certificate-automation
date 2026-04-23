# import os
# import io
# from pydoc import text
# from reportlab.pdfgen import canvas
# from reportlab.lib.colors import black
# from reportlab.lib.pagesizes import A4
# from pypdf import PdfReader, PdfWriter
# from config import EXP_CERTIFICATES_DIR, EXP_TEMPLATE


# def experience_certificate(current_date, emp_id,name, course_name, start_date, end_date,filepath):
#       """
#       Overlays the text on the existing template.pdf and saves as
#       a new PDF. Returns the path of the saved PDF.
#         """
      
#       #create an in-memory PDF with the overlaid text
#       packet = io.BytesIO()
#       can = canvas.Canvas(packet, pagesize=A4)
#       width, height = A4

#       #Adding the text to the certificate
#       LEFT_X = 72   
#       y = 515  # Starting y position

#       # Line 1
#       can.setFont("Helvetica", 11.5)
#       can.setFillColor(black)
#       can.drawString(LEFT_X, y, f"This is to certify that Ms./Mr.{name} (Emp ID: {emp_id}) worked with")
      
#       y -= 19
#       can.drawString(LEFT_X, y, f"RP2 India Pvt. Ltd. as an Intern in {course_name}") 

#       y -= 19
#       can.drawString(LEFT_X, y, f"from {start_date} to {end_date}.")               

#       # Move down
#       y -= 30

#       can.setFont("Helvetica", 11.5)
#       can.setFillColor(black)
#       can.drawString(LEFT_X, y, "During the internship tenure at RP2, the performance was good, and the assigned")

#       y -= 19
#       can.drawString(LEFT_X, y, "roles and responsibilities were carried out diligently and professionally.")
      
#       y -= 30
#       can.setFont("Helvetica", 11.5)
#       can.setFillColor(black)
#       can.drawString(LEFT_X, y, "Best wishes are extended for future opportunities.")


#       can.setFont("Helvetica",11.5)
#       can.setFillColor(black)
#       can.drawString(105,697, current_date)


#       # Save the in-memory PDF
#       can.save()
#       #Move to the begninning of the memory file
#       packet.seek(0)
#       #Read the overlay PDF
#       new_exp_pdf = PdfReader(packet)

#       #Load the template PDF
#       existing_exp_pdf = PdfReader(EXP_TEMPLATE)
#       output_exp = PdfWriter()#where we will write the final PDF

#       #Merge the overlay PDF with the template PDF
#       page = existing_exp_pdf.pages[0]
#       page.merge_page(new_exp_pdf.pages[0])
#       output_exp.add_page(page)

      # #Ensure the certificates directory exists
      # os.makedirs(EXP_CERTIFICATES_DIR, exist_ok=True)

      # #Create safe filename
      # safe_name = "".join([c for c in name if c.isalnum() or c == " "]).rstrip().replace(" ","_")
      # output_file_name = f"Experience_Crtfct_{safe_name}.pdf"
      # output_path = os.path.join(EXP_CERTIFICATES_DIR, output_file_name)

      # #Handle duplicate filenames by appending a number
      # counter = 1
      # while os.path.exists(output_path):
      #       output_file_name = f"Experience_Crtfct_{safe_name}_{counter}.pdf"
      #       output_path = os.path.join(EXP_CERTIFICATES_DIR, output_file_name)
      #       counter += 1

      # #Write the final PDF to disk
      # with open(output_path,"wb") as outputStream:
      #       output_exp.write(outputStream)  

      # return output_path          


def experience_certificate(current_date, emp_id, name, course_name, start_date, end_date, filepath):

    import os
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import black
    from reportlab.lib.pagesizes import A4
    from pypdf import PdfReader, PdfWriter
    from config import TEMPLATE_PDF

    # Create in-memory PDF
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4

    LEFT_X = 72   
    y = 515

    can.setFont("Helvetica", 11.5)
    can.setFillColor(black)
    can.drawString(LEFT_X, y, f"This is to certify that Ms./Mr. {name} (Emp ID: {emp_id}) worked with")

    y -= 19
    can.drawString(LEFT_X, y, f"RP2 India Pvt. Ltd. as an Intern in {course_name}") 

    y -= 19
    can.drawString(LEFT_X, y, f"from {start_date} to {end_date}.")               

    y -= 30
    can.drawString(LEFT_X, y, "During the internship tenure at RP2, the performance was good, and the assigned")

    y -= 19
    can.drawString(LEFT_X, y, "roles and responsibilities were carried out diligently and professionally.")
      
    y -= 30
    can.drawString(LEFT_X, y, "Best wishes are extended for future opportunities.")

    # Add date (optional)
    y -= 40
    can.drawString(LEFT_X, y, f"Date: {current_date}")

    can.save()
    packet.seek(0)

    # Merge with template
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(TEMPLATE_PDF)
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # ✅ SAVE TO GIVEN PATH (IMPORTANT FIX)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "wb") as outputStream:
        output.write(outputStream)

    print("Saving certificate to:", filepath)    

    return filepath
