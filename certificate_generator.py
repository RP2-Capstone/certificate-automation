import os
import io
from pydoc import text
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, grey
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
from config import CERTIFICATES_DIR, TEMPLATE_PDF


def generate_certificate(name, course_name, start_date, end_date, filepath):

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    LEFT_X = 60   
    y = 500

    can.setFont("Helvetica", 14)
    can.setFillColor(grey)
    can.drawString(LEFT_X, y, "This is to certify that")

    y -= 30
    can.setFont("Helvetica-Bold", 24)
    can.setFillColor(black)
    can.drawString(LEFT_X, y, name)

    y -= 25
    can.setFont("Helvetica", 14)
    can.setFillColor(grey)
    can.drawString(LEFT_X, y, "has successfully completed the")

    y -= 25
    can.drawString(LEFT_X, y, "Rounded Professional Program on")

    y -= 25
    can.setFont("Helvetica-Bold", 16)
    can.setFillColor(black)
    can.drawString(LEFT_X, y, f"{course_name},")

    y -= 25
    can.setFont("Helvetica", 14)
    can.setFillColor(grey)
    can.drawString(LEFT_X, y, f"conducted from {start_date} to {end_date}.")

    can.save()
    packet.seek(0)

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(TEMPLATE_PDF)
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # ✅ SAVE TO GIVEN PATH
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "wb") as outputStream:
        output.write(outputStream)

    print("Saving certificate to:", filepath)    

    return filepath