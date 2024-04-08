import google.generativeai as genai
import os
import json

GOOGLE_API_KEY = 'AIzaSyByEHWnU4grVOfuRUgdXB0gk93v-yWKfAs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def gemini_parsed_order(order_desc):
    schema = """{"Products":["put the list of products"],"Weight":["put the list of weight"],"Quantity":["put the list of quantity"]}"""
    pre_prompt = f"Given the following order(s) {order_desc} FILTER and SORT INTELLIGENTLY and return the products ordered and their weight and quantities. If the order has multiple products then each of them should be sorted with their weights and requested quantities. Return in the following example :{schema}"
    response = model.generate_content(pre_prompt)

    if response.parts:
        return response.text
    else:
        return "No valid content generated."

order_desc = "2 bags of 100kg CRUFertilizer, 150 pounds of Animal feed and 50kg of Carrot seeds"

order = gemini_parsed_order(order_desc)

# Directly attempt to load the 'order' string as JSON, assuming it's in the correct format.
try:
    order_items_dict = json.loads(order)
except json.JSONDecodeError:
    print("Failed to decode order into JSON. Please check the format.")
    order_items_dict = {}

# If 'order_items_dict' is properly formatted, this should work without error.
final_order = [list(order_items_dict.keys()), list(order_items_dict.values())]

print(final_order)
