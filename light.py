import csv
import re
import os
import glob

def read_files_serially():
    # Get the list of existing files in the /batadb directory
    existing_files = os.listdir('./batadb')

    # Filter out non-CSV files and extract serial numbers
    existing_serials = [int(f[:-4]) for f in existing_files if f.endswith('.csv')]
    latest_serial = 0
    # Determine the serial number for the new file
    if existing_serials:
        latest_serial = max(existing_serials)
    latest_file = f'./batadb/{latest_serial}.csv'
    # Determine the previous file (if any)
    if latest_serial > 0:
        previous_file = f'./batadb/{latest_serial - 1}.csv'
    else:
        previous_file = None
    
    return latest_file, previous_file

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
    with open('./batadb/output.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['Handle', 'Title', 'Collection', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value',  'Variant Inventory Policy', 'Variant Inventory Qty', 'Variant Inventory Tracker', 'Variant Price', 'Image Src', 'Image Alt Text', 'Variant SKU']) #, 'Image Position' , 'Variant Inventory Tracker','Variant Image',
        writer.writeheader()
        writer.writerows(data)

# def combine_images(images):
#     comma_separated = 
# latest_file, previous_file = read_files_serially()


def transform_data(file_path):
    # Open the input CSV file
    with open(latest_file, 'r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        # Create a list to hold the new rows
        new_rows = []
        written_handles = []
        # Loop through each row in the input file
        for idx, row in enumerate(rows):
            if row['id'] == 'id':
                continue # skip rows that has header in it

            if row['product_code'] in written_handles:
                continue
            # Loop through the variant columns and create a new row for each variant
            name = row['name']
            price = row['price']
            category = row['CategoryCode']
            size_type = row['size_type']
            

            # first extract all the images and map them by product code 
            product_images = {}
            for i in range(53):
                if len(row[f'images_{i}']) != 0:
                    color = row[f'Color_{i}']
                    product_images[color] = row[f'images_{i}']

            previous_images = ""
            previous_color = ""
            for i in range(53):
                new_row = {
                    'Handle': row['product_code'],
                    'Title': name,
                    'Collection': category,
                    'Option1 Name': 'Size type',
                    'Option1 Value': size_type
                    # 'Option2 Name': 'Material',
                    # 'Option2 Value': row['upperDescription']
                }
                has_size = False
                has_color = False
                # first assign the images so that previous_images has value before skipping items
                imagesString = previous_images
                if len(row[f'images_{i}']) != 0:
                    imagesString = row[f'images_{i}']
                    previous_images = imagesString
                    # split the images into an array, save the record in the end, and write it 
                # new_row['Image Src'] = imagesString
                images = imagesString.split(',')
                # new_row['Image Src'] = product_images
                # first check if available, and if not available, skip the loop item (don't add to output rows)
                # if row[f'availability_{i}'] != 'Available':
                #     continue
                if row[f'Size_{i}'] and row[f'Size_{i}'] != '':
                    new_row['Option2 Name'] = 'Size'
                    try:
                        new_row['Option2 Value'] = int(row[f'Size_{i}']) / 10
                    except:
                        new_row['Option2 Value'] = row[f'Size_{i}']
                    has_size = True
                if row[f'Color_{i}'] and row[f'Color_{i}'] != '':
                    new_row['Option3 Name'] = 'Color'
                    new_row['Option3 Value'] = row[f'Color_{i}']
                    # new_row['Image Src'] = product_images[row[f'Color_{i}']]
                    # new_row['Image Alt Text'] = row[f'Color_{i}']
                    if previous_color == new_row['Option3 Value']:
                        previous_color = new_row['Option3 Value']
                        
                    # else:
                    #     new_row['Image Src'] = imagesString
                    has_color = True
                # add 10 quantity where the product is available
                # new_row['Varient Inventory Qty'] = 1
                new_row['Variant Inventory Qty'] = 99999 if row[f'availability_{i}'] == 'Available' else 0
                new_row['Variant Inventory Tracker'] = 'shopify'
                new_row['Variant Inventory Policy'] = "continue" if row[f'availability_{i}'] == 'Available' else "deny"
                new_row['Variant Price'] = price
                new_row['Variant SKU'] = extract_product_id(images[0])
                # if row["product_code"] == "8426842":
                #     print("yay")
                if has_size or has_color:

                    for idx, image in enumerate(images):
                        new_row['Image Src'] = image
                        # new_row['Variant SKU'] = extract_product_id(images[0])
                        new_row['Image Alt Text'] = row[f'Color_{i}']
                        # new_row['Image Position'] = idx + 1
                        if idx > 0:
                            #clear all rows except handle and variant image
                            copy_row = {key: '' for key in new_row}
                            copy_row['Handle'] = row['product_code']
                            copy_row['Image Src'] = image
                            copy_row['Image Alt Text'] = row[f'Color_{i}']
                            new_rows.append(copy_row.copy())
                        else:
                            new_rows.append(new_row.copy())
            written_handles.append(new_row['Handle'])
        return new_rows



latest_file, previous_file = read_files_serially()
latest_data = transform_data(latest_file)
if previous_file is not None:
    previous_data = transform_data(previous_file)

# Get all handles in latest_data
latest_handles = [row['Handle'] for row in latest_data]

# Iterate over previous_data
for row in previous_data:
    # If the handle doesn't exist in latest_data
    if row['Handle'] not in latest_handles:
        # Create a copy of the row
        new_row = row.copy()
        # Set 'Variant Inventory Qty' to 0
        new_row['Variant Inventory Qty'] = 0
        new_row['Variant Inventory Policy'] = 'deny' if new_row['Variant Inventory Policy'] == 'continue' else new_row['Variant Inventory Policy']
        print('id deleted from new data: ', row['Handle'])
        # Append the new row to latest_data
        latest_data.append(new_row)

write_file(latest_data)
