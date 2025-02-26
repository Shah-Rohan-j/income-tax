from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

def generate_gst_bill(filename, seller_name='', seller_address='', pan_number='', gst_number='', bank_details=''):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "GST Standard Bill")
    
    # Seller Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Seller Details:")
    
    c.drawString(50, height - 130, f"Name: {seller_name if seller_name else '________________'}")
    c.drawString(50, height - 150, f"Address: {seller_address if seller_address else '________________'}")
    c.drawString(50, height - 170, f"PAN Number: {pan_number if pan_number else '________________'}")
    c.drawString(50, height - 190, f"GST Number: {gst_number if gst_number else '________________'}")
    c.drawString(50, height - 210, f"Bank Details: {bank_details if bank_details else '________________'}")
    
    # Placeholder for Bill Items Table (can be extended as needed)
    c.drawString(50, height - 250, "Bill Items:")
    c.rect(50, height - 500, width - 100, 200, stroke=1, fill=0)
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "This is a system-generated invoice.")
    
    c.save()
    print(f"GST bill saved as {filename}")

# Streamlit UI
st.title("GST Bill Generator")

seller_name = st.text_input("Seller Name")
seller_address = st.text_area("Seller Address")
pan_number = st.text_input("PAN Number")
gst_number = st.text_input("GST Number")
bank_details = st.text_area("Bank Details")

if st.button("Generate Bill"):
    filename = "gst_bill.pdf"
    generate_gst_bill(filename, seller_name, seller_address, pan_number, gst_number, bank_details)
    with open(filename, "rb") as f:
        st.download_button("Download Bill", f, file_name=filename, mime="application/pdf")
