from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import re

## --------- Local imports ---------------
#from routes import parse_order_description
from common.getfilepath import file_path

## This function helps to filter the orders and checks for regular expressions regarding weight/quantities. Very Primitive way of doing NLP. WIP
def parse_order_description(order_desc):
    # Updated pattern to include more units and optionally match the word 'of' following the units
    pattern = re.compile(r'(\d+\s?(kg|kgs|bag(s?)|box(es?)|lb|lbs|pound(s?)|gram(s?)|gm)\s?of)')
    
    items = order_desc.split(',')
    parsed_items = [["Item", "Quantity/Weight"]]
    for item in items:
        match = pattern.search(item)
        if match:
            quantity = match.group(1).rstrip(' of')  # Remove ' of' from the end of the quantity string
            # Remove the matched quantity (including 'of' if present) from the item description
            name = pattern.sub('', item).strip()
            parsed_items.append([name.capitalize(), quantity])
        else:
            # If no match, assume the entire string is the item name
            parsed_items.append([item.strip().capitalize(), ''])
    
    return parsed_items



## for adding a watermark to the invoice 
def add_watermark(canvas, doc):
    # Use x=0, y=0 for full-page background, adjust as needed
    canvas.saveState()
    canvas.drawImage("", 0, 0, width=doc.width, height=doc.height, mask='auto')
    canvas.restoreState()


## My invoice generation script ----
def generate_invoice(order_details, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []
    
    ## Invoice
    logo = file_path(r"../images/spacelogo.png")
    logo_img = Image(logo, width=2*inch, height=1*inch)  # Adjust width and height as needed
    flowables.insert(0, logo_img) 

    # Invoice header
    heading_style = styles['Heading1']
    heading_style.alignment = TA_CENTER
    header = Paragraph('SpaceAI Marketplace - Farmer Invoice', heading_style)
    flowables.append(header)

    # Order and Farmer details
    order_info = Paragraph(f'''
    <b>Order ID:</b> {order_details.Order.orderID}<br/>
    <b>Date:</b> {order_details.Order.orderDate.strftime("%Y-%m-%d")}<br/>
    <b>Farmer Name:</b> {order_details.Farmer.name}<br/>
    <b>Farmer Phone:</b> {order_details.Farmer.phone}<br/>
    <b>Farmer Location:</b> {order_details.Farmer.location}<br/>
    ''', styles['Normal'])
    flowables.append(order_info)

    flowables.append(Spacer(1, 12))  # Add some space before listing items

    # Use the adjusted parse_order_description function here
    order_items = parse_order_description(order_details.Order.order_desc)

    # Create table for order items, using the parsed items
    table = Table(order_items, colWidths=[4*inch, 3*inch], hAlign='CENTER')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightslategray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
    ]))
    flowables.append(table)

    doc.build(flowables)