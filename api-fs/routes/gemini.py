import google.generativeai as genai
import os
import json

GOOGLE_API_KEY = 'AIzaSyByEHWnU4grVOfuRUgdXB0gk93v-yWKfAs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# def gemini_parsed_order(order_desc):
#     schema = """{"Products":["put the list of products"],"Weight":["put the list of weight"],"Quantity":["put the list of quantity"]}"""
#     pre_prompt = f"Given the following order(s) {order_desc} FILTER and SORT INTELLIGENTLY and return the products ordered and their weight and quantities. If the order has multiple products then each of them should be sorted with their weights and requested quantities. Return in the following example :{schema}"
#     response = model.generate_content(pre_prompt)

#     if response.parts:
#         return response.text
#     else:
#         return "No valid content generated."

# order_desc = "2 bags of 100kg CRUFertilizer, 150 pounds of Animal feed and 50kg of Carrot seeds"

# order = gemini_parsed_order(order_desc)

# # Directly attempt to load the 'order' string as JSON, assuming it's in the correct format.
# try:
#     order_items_dict = json.loads(order)
# except json.JSONDecodeError:
#     print("Failed to decode order into JSON. Please check the format.")
#     order_items_dict = {}

# # If 'order_items_dict' is properly formatted, this should work without error.
# final_order = [list(order_items_dict.keys()), list(order_items_dict.values())]

# print(final_order)

def nicely_formatted_order_gemini(order_desc):
    pre_prompt = f"Given the following order(s) {order_desc} FILTER and SORT INTELLIGENTLY and return the products ordered and their respective weight and quantities. If the order has multiple products, then each of them should be sorted according to their weights and requested quantities. Return the final result in a simple bulleted format without any headings or categories."
    response = model.generate_content(pre_prompt)

    if response.parts:
        return response.text
    else:
        return "No valid content generated."

order_desc = "2 boxes of chocolate, 2 bags of 1kg of potatoes, 2kg watermelon, 1000kg of Fertilizer, A box of Chicks, 100 grams of Butter, 2000 pounds of Manure, 500 lbs of Carrots, A shovel and a machete; Actually can i also have some DairyFresh Milk 2% fat - 2kg. Last but not least, two eggs"

formatted_order = nicely_formatted_order_gemini(order_desc)

print(formatted_order)