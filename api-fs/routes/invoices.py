from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import google.generativeai as genai
import json

## --------- Local imports ---------------
#from routes import parse_order_description
from common.getfilepath import file_path

## This function helps to filter the orders using GEMINI

GOOGLE_API_KEY ='AIzaSyByEHWnU4grVOfuRUgdXB0gk93v-yWKfAs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def gemini_parsed_order(order_desc):
    schema = """{"Products":["put the list of products"],"Weight":["put the list of weight"],"Quantity":["put the list of quantity"]}"""
    pre_prompt = f"Given the following order(s) {order_desc} FILTER and SORT INTELLIGENTLY and return the products ordered and their weight and quantities. If the order has multiple products then each of them should be sorted with their weights and requested quantities. Return in the following example :{schema}"
    response = model.generate_content(pre_prompt)

    if response.parts:
        order_details = json.loads(response.text)  # Assuming the response.text is a JSON string
        # Convert the order details into a format suitable for Table creation in ReportLab
        table_data = [["Product", "Weight", "Quantity"]]  # Header row
        for product, weight, quantity in zip(order_details["Products"], order_details["Weight"], order_details["Quantity"]):
            table_data.append([product, weight, quantity])
        return table_data
    else:
        return [["Product", "Weight", "Quantity"]]  # Return only the header row if no valid content is generated




## for adding a watermark to the invoice 
# def add_watermark(canvas, doc):
#     # Use x=0, y=0 for full-page background, adjust as needed
#     canvas.saveState()
#     canvas.drawImage("", 0, 0, width=doc.width, height=doc.height, mask='auto')
#     canvas.restoreState()


####### My invoice generation script -------------------------------------------------------------------------------------

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
    header = Paragraph('SpaceAI Marketplace - Farmer Order', heading_style)
    flowables.append(header)
    
    #order Date
    order_date_str = order_details.Order.orderDate.strftime("%Y-%m-%d %I:%M %p")

    # Order and Farmer details
    order_info = Paragraph(f'''
    <br/>
    <b>Order Number:</b> {order_details.Order.o_uuid}<br/>
    <b>Date:</b> {order_date_str}<br/>
    <b>Farmer's Name:</b> {order_details.Farmer.name}<br/>
    <b>Farmer's Phone:</b> {order_details.Farmer.phone}<br/>
    <b>County:</b> {order_details.Farmer.county}<br/>
    <b>Vilage:</b> {order_details.Farmer.village}<br/>
    <b>Address/Location:</b> {order_details.Farmer.location}<br/>
    ''', styles['Normal'])
    flowables.append(order_info)

    flowables.append(Spacer(1, 12))  # Add some space before listing items

    # Use the adjusted parse_order_description function here
    final_order = gemini_parsed_order(order_details.Order.order_desc)

# Create table for order items, using the parsed items
    table = Table(final_order, colWidths=[4*inch, 3*inch,2*inch], hAlign='CENTER')
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightseagreen),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 10), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightsteelblue),
    ]))
    flowables.append(table)

    doc.build(flowables)

