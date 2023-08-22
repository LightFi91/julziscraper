import csv
import re

def extract_product_id(url):
    # return url.split("/")[-1]
    pattern = r'(\d+)_1\.jpg'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
    
def write_file(data):
    # Write the new rows to a new CSV file
    with open('names.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['Handle', 'Title', 'Collection']) #, 'Image Position' , 'Variant Inventory Tracker','Variant Image',
        writer.writeheader()
        writer.writerows(data)

# def combine_images(images):
#     comma_separated = 

# Open the input CSV file
# import os

# # Get the current working directory
# cwd = os.getcwd()
# print("Current working directory: {0}".format(cwd))

# # Check if the file exists
# file_path = os.path.join(cwd, 'data/1.csv')
# if not os.path.isfile(file_path):
#     print("File does not exist: {0}".format(file_path))
# else:
#     print("File exists: {0}".format(file_path))

with open('./julziscraper/data/1.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)
    # Create a list to hold the new rows
    new_rows = []
    written_handles = []
    # Loop through each row in the input file
    for idx, row in enumerate(rows):
        # if idx == 0:
        #     continue # skip the header

        if row['id'] == 'id':
            continue # skip rows that has header in it

        if row['product_code'] in written_handles:
            continue
        # Loop through the variant columns and create a new row for each variant
        name = row['name']
        price = row['price']
        category = row['CategoryCode']

        new_row = {
          'Handle': row['product_code'],
          'Title': name,
          'Collection': category,
          # 'Option2 Name': 'Material',
          # 'Option2 Value': row['upperDescription']
        }
        new_rows.append(new_row.copy())
        
        written_handles.append(new_row['Handle'])

write_file(new_rows)               
