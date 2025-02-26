from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import streamlit as st

def generate_gst_bill(filename, business_name='', seller_address='', seller_state='', contact_info='', gst_number='', invoice_no='', invoice_date='', due_date='', buyer_name='', buyer_state='', bill_to='', ship_to='', items=[], bank_details=''):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Header Section
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, business_name if business_name else "Business Name")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, seller_address if seller_address else "Address")
    c.drawString(50, height - 95, contact_info if contact_info else "Website, Email Address, Contact Number")
    c.drawString(50, height - 110, f"GSTIN: {gst_number if gst_number else '________________'}")
    
    # Invoice Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, height - 80, "Invoice Details:")
    c.setFont("Helvetica", 10)
    c.drawString(400, height - 100, f"Invoice No.: {invoice_no if invoice_no else '__________'}")
    c.drawString(400, height - 115, f"Invoice Date: {invoice_date if invoice_date else '__________'}")
    c.drawString(400, height - 130, f"Due Date: {due_date if due_date else '__________'}")
    
    # Buyer Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "Buyer Name:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 175, buyer_name if buyer_name else "Person Name")
    c.drawString(50, height - 190, f"State: {buyer_state if buyer_state else '__________'}")
    
    # Billing and Shipping Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 210, "BILL TO:")
    c.drawString(300, height - 210, "SHIP TO:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 230, bill_to if bill_to else "Person Name\nBusiness Name\nAddress")
    c.drawString(300, height - 230, ship_to if ship_to else "Person Name\nBusiness Name\nAddress")
    
    # Table Headers
    c.setFillColor(colors.lightgrey)
    c.rect(50, height - 280, width - 100, 20, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(55, height - 275, "DESCRIPTION")
    c.drawString(250, height - 275, "QTY")
    c.drawString(300, height - 275, "UNIT PRICE")
    c.drawString(400, height - 275, "GST %")
    c.drawString(450, height - 275, "TOTAL")
    
    # Table Rows
    y_position = height - 300
    total_amount = 0
    c.setFont("Helvetica", 10)
    for index, item in enumerate(items):
        if index % 2 == 0:
            c.setFillColor(colors.whitesmoke)
            c.rect(50, y_position - 5, width - 100, 20, fill=True, stroke=False)
        c.setFillColor(colors.black)
        gst_rate = item.get("gst_percent", 0)
        price = item.get("qty", 0) * item.get("unit_price", 0)
        gst_amount = (gst_rate / 100) * price
        total = price + gst_amount
        
        # Apply CGST+SGST or IGST based on state comparison
        if seller_state == buyer_state:
            gst_text = f"CGST {gst_rate/2}% + SGST {gst_rate/2}%"
        else:
            gst_text = f"IGST {gst_rate}%"
        
        c.drawString(55, y_position, item.get("description", ""))
        c.drawString(250, y_position, str(item.get("qty", "")))
        c.drawString(300, y_position, str(item.get("unit_price", "")))
        c.drawString(400, y_position, gst_text)
        c.drawString(450, y_position, str(round(total, 2)))
        total_amount += total
        y_position -= 20
    
    # Total Amount
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, y_position - 20, f"Grand Total: ₹{round(total_amount, 2)}")
    
    # Bank Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 120, "Bank Details:")
    c.setFont("Helvetica", 10)
    c.drawString(50, 100, bank_details if bank_details else "Account Name:\nBank Name:\nAccount Number:\nIFSC Code:")
    
    # Footer and Signature
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "This is a system-generated invoice.")
    c.drawString(400, 50, "Signature: _____________")
    
    c.save()

# Streamlit UI
st.title("GST Invoice Generator")

business_name = st.text_input("Business Name")
seller_address = st.text_area("Seller Address")
seller_state = st.text_input("Seller State")
contact_info = st.text_area("Contact Information")
gst_number = st.text_input("GST Number")
invoice_no = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date")
due_date = st.date_input("Due Date")
buyer_name = st.text_input("Buyer Name")
buyer_state = st.text_input("Buyer State")
bill_to = st.text_area("Bill To")
ship_to = st.text_area("Ship To")
bank_details = st.text_area("Bank Details")

items = []
num_items = st.number_input("Number of Items", min_value=1, step=1)
for i in range(num_items):
    st.write(f"### Item {i+1}")
    description = st.text_input(f"Description {i+1}")
    qty = st.number_input(f"Quantity {i+1}", min_value=1, step=1)
    unit_price = st.number_input(f"Unit Price {i+1}", min_value=0.0, step=0.01)
    gst_percent = st.number_input(f"GST % {i+1}", min_value=0, max_value=50, step=1)
    items.append({"description": description, "qty": qty, "unit_price": unit_price, "gst_percent": gst_percent})

if st.button("Generate Invoice"):
    filename = "gst_invoice.pdf"
    generate_gst_bill(filename, business_name, seller_address, seller_state, contact_info, gst_number, invoice_no, invoice_date, due_date, buyer_name, buyer_state, bill_to, ship_to, items, bank_details)
    with open(filename, "rb") as f:
        st.download_button("Download Invoice", f, file_name=filename, mime="application/pdf")
