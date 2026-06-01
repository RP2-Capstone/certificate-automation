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
