from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import streamlit as st

def generate_gst_bill(filename, business_name='', seller_address='', contact_info='', gst_number='', invoice_no='', invoice_date='', due_date='', bill_to='', ship_to='', items=[]):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title with color
    c.setFillColor(colors.blue)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Invoice")
    c.setFillColor(colors.black)
    
    # Draw lines for sections
    c.line(50, height - 60, width - 50, height - 60)
    c.line(50, height - 140, width - 50, height - 140)
    c.line(50, height - 200, width - 50, height - 200)
    c.line(50, height - 230, width - 50, height - 230)
    
    # Business Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, business_name if business_name else "Business Name")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 100, seller_address if seller_address else "Address")
    c.drawString(50, height - 115, contact_info if contact_info else "Website, Email Address, Contact Number")
    c.drawString(50, height - 130, f"GSTIN: {gst_number if gst_number else '________________'}")
    
    # Invoice Details
    c.drawString(400, height - 100, f"Invoice No.: {invoice_no if invoice_no else '__________'}")
    c.drawString(400, height - 115, f"Invoice Date: {invoice_date if invoice_date else '__________'}")
    c.drawString(400, height - 130, f"Due Date: {due_date if due_date else '__________'}")
    
    # Billing and Shipping Details with section headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "BILL TO")
    c.drawString(300, height - 160, "SHIP TO")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 180, bill_to if bill_to else "Person Name\nBusiness Name\nAddress")
    c.drawString(300, height - 180, ship_to if ship_to else "Person Name\nBusiness Name\nAddress")
    
    # Table Headers with color
    c.setFillColor(colors.lightgrey)
    c.rect(50, height - 250, width - 100, 20, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(55, height - 245, "DESCRIPTION")
    c.drawString(300, height - 245, "QTY")
    c.drawString(370, height - 245, "UNIT PRICE")
    c.drawString(450, height - 245, "TOTAL")
    
    # Table Rows with alternate shading
    y_position = height - 270
    c.setFont("Helvetica", 10)
    for index, item in enumerate(items):
        if index % 2 == 0:
            c.setFillColor(colors.whitesmoke)
            c.rect(50, y_position - 5, width - 100, 20, fill=True, stroke=False)
        c.setFillColor(colors.black)
        c.drawString(55, y_position, item.get("description", ""))
        c.drawString(300, y_position, str(item.get("qty", "")))
        c.drawString(370, y_position, str(item.get("unit_price", "")))
        c.drawString(450, y_position, str(item.get("total", "")))
        y_position -= 20
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "This is a system-generated invoice.")
    
    c.save()
    print(f"GST bill saved as {filename}")

# Streamlit UI
st.title("GST Invoice Generator")

business_name = st.text_input("Business Name")
seller_address = st.text_area("Seller Address")
contact_info = st.text_area("Contact Information")
gst_number = st.text_input("GST Number")
invoice_no = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date")
due_date = st.date_input("Due Date")
bill_to = st.text_area("Bill To")
ship_to = st.text_area("Ship To")

items = []
num_items = st.number_input("Number of Items", min_value=1, step=1)
for i in range(num_items):
    st.write(f"### Item {i+1}")
    description = st.text_input(f"Description {i+1}")
    qty = st.number_input(f"Quantity {i+1}", min_value=1, step=1)
    unit_price = st.number_input(f"Unit Price {i+1}", min_value=0.0, step=0.01)
    total = qty * unit_price
    items.append({"description": description, "qty": qty, "unit_price": unit_price, "total": total})

if st.button("Generate Invoice"):
    filename = "gst_invoice.pdf"
    generate_gst_bill(filename, business_name, seller_address, contact_info, gst_number, invoice_no, invoice_date, due_date, bill_to, ship_to, items)
    with open(filename, "rb") as f:
        st.download_button("Download Invoice", f, file_name=filename, mime="application/pdf")
