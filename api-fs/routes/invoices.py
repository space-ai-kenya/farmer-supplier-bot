from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
    pre_prompt = f"""
    Given the following order(s): {order_desc}

    Intelligently filter and sort the order details with no mistakes, recheck the order to make sure you havent forgotten anything and return the following information:

    - The products ordered (only the names of the products should appear in the products category/list, do not put the weights/quantity of the Products there.)
    - The weight of each product (if available, otherwise set to 'N/A')
    - The requested quantity of each product (if the quantity is not defined then by default assume its '1', if its defined assign the correct quantity.)

    If the order has multiple products, make sure to present each product with its corresponding weight and quantity in a sorted manner.
    Finally return the correct information in the following format:{schema}"""

    response = model.generate_content(pre_prompt)

    if response.parts:
        order_details = json.loads(response.text)  # Assuming the response.text is a JSON string
        # Convert the order details into a format suitable for Table creation in ReportLab
        table_data = [["Products", "Weight", "Quantity"]]  # Header row
        for product, weight, quantity in zip(order_details["Products"], order_details["Weight"], order_details["Quantity"]):
            table_data.append([product, weight, quantity])
        return table_data
    else:
        return [["Products", "Weight", "Quantity"]]  # Return only the header row if no valid content is generated




### Returns the order inputted by the farmer in well clear manner for validation, then if approved is then used by 2nd gemini prompt.
def nicely_formatted_order_gemini(order_desc):
    pre_prompt = f"Given the following order(s) {order_desc} FILTER and SORT INTELLIGENTLY and return the products ordered and their respective weight and quantities. If the order has multiple products, then each of them should be sorted according to their weights and requested quantities. Return the final result in a simple bulleted format without any headings or categories."
    response = model.generate_content(pre_prompt)

    if response.parts:
        return response.text
    else:
        return "No valid content generated."




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
    
    # Invoice logo
    logo = file_path("../images/spacelogo.png")
    logo_img = Image(logo, width=2*inch, height=1*inch)
    flowables.append(logo_img)
    
    # Invoice header
    heading_style = styles['Heading1']
    heading_style.alignment = TA_CENTER
    header = Paragraph("SpaceAI Marketplace - Farmer's Order", heading_style)
    flowables.append(header)

     # Spacer-- adds space between
    flowables.append(Spacer(1, 12))

    # Formatting order and farmer details for better UI/UX
    details_style = ParagraphStyle('DetailsStyle', parent=styles['Normal'], alignment=TA_LEFT, spaceAfter=10, leftIndent=10)
    
    order_date_str = order_details.Order.orderDate.strftime("%Y-%m-%d %I:%M %p")
    order_info_content = [
        ["Order Number:", order_details.Order.o_uuid],
        ["Date:", order_date_str],
        ["Farmer's Name:", order_details.Farmer.name],
        ["Farmer's Phone:", order_details.Farmer.phone],
        ["County:", order_details.Farmer.county],
        ["Village:", order_details.Farmer.village],
        ["Address/Location:", order_details.Farmer.location]
    ]

    for item in order_info_content:
        flowables.append(Paragraph(f'<b>{item[0]}</b> {item[1]}', details_style))

    # Spacer for aesthetics
    flowables.append(Spacer(1, 12))

    # Assuming final_order is returned from gemini_parsed_order and properly formatted
    final_order = gemini_parsed_order(order_details.Order.order_desc)
    
    # Table for order items
    table = Table(final_order, colWidths=[4*inch, 3*inch, 2*inch], hAlign='CENTER')
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightseagreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    flowables.append(table)

    doc.build(flowables)