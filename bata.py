import requests
import json
import csv
import os
import re
import uuid
import json

header = ["url", "id", "name", "product_code", "price", "size_type", "summary", "type", "variant",
              "upperDescription", "articleNo", "CategoryCode", "group_id", "images", 
              "Color_0", "Size_0", "availability_0", "images_0", "product_link_0",
              "Color_1", "Size_1", "availability_1", "images_1", "product_link_1",
              "Color_2", "Size_2", "availability_2", "images_2", "product_link_2",
              "Color_3", "Size_3", "availability_3", "images_3",  "product_link_3",
              "Color_4", "Size_4", "availability_4", "images_4",  "product_link_4",
              "Color_5", "Size_5", "availability_5", "images_5",  "product_link_5",
              "Color_6", "Size_6", "availability_6", "images_6",  "product_link_6",
              "Color_7", "Size_7", "availability_7", "images_7",  "product_link_7",
              "Color_8", "Size_8", "availability_8", "images_8",  "product_link_8",
              "Color_9", "Size_9", "availability_9", "images_9", "product_link_9",
              "Color_10", "Size_10", "availability_10", "images_10", "product_link_10",
              "Color_11", "Size_11", "availability_11", "images_11", "product_link_11",
              "Color_12", "Size_12", "availability_12", "images_12", "product_link_12",
              "Color_13", "Size_13", "availability_13", "images_13", "product_link_13",
              "Color_14", "Size_14", "availability_14", "images_14", "product_link_14",
              "Color_15", "Size_15", "availability_15", "images_15", "product_link_15",
              "Color_16", "Size_16", "availability_16", "images_16", "product_link_16",
              "Color_17", "Size_17", "availability_17", "images_17", "product_link_17",
              "Color_18", "Size_18", "availability_18", "images_18", "product_link_18",
              "Color_19", "Size_19", "availability_19", "images_19", "product_link_19",
              "Color_20", "Size_20", "availability_20", "images_20", "product_link_20",
              "Color_21", "Size_21", "availability_21", "images_21", "product_link_21",
              "Color_22", "Size_22", "availability_22", "images_22", "product_link_22",
              "Color_23", "Size_23", "availability_23", "images_23", "product_link_23",
              "Color_24", "Size_24", "availability_24", "images_24", "product_link_24",
              "Color_25", "Size_25", "availability_25", "images_25", "product_link_25",
              "Color_26", "Size_26", "availability_26", "images_26", "product_link_26",
              "Color_27", "Size_27", "availability_27", "images_27", "product_link_27",
              "Color_28", "Size_28", "availability_28", "images_28", "product_link_28",
              "Color_29", "Size_29", "availability_29", "images_29", "product_link_29",
              "Color_30", "Size_30", "availability_30", "images_30", "product_link_30",
              "Color_31", "Size_31", "availability_31", "images_31", "product_link_31",
              "Color_32", "Size_32", "availability_32", "images_32", "product_link_32",
              "Color_33", "Size_33", "availability_33", "images_33", "product_link_33",
              "Color_34", "Size_34", "availability_34", "images_34", "product_link_34",
              "Color_35", "Size_35", "availability_35", "images_35", "product_link_35",
              "Color_36", "Size_36", "availability_36", "images_36", "product_link_36",
              "Color_37", "Size_37", "availability_37", "images_37", "product_link_37",
              "Color_38", "Size_38", "availability_38", "images_38", "product_link_38",
              "Color_39", "Size_39", "availability_39", "images_39", "product_link_39",
              "Color_40", "Size_40", "availability_40", "images_40", "product_link_40",
              "Color_41", "Size_41", "availability_41", "images_41", "product_link_41",
              "Color_42", "Size_42", "availability_42", "images_42", "product_link_42",
              "Color_43", "Size_43", "availability_43", "images_43", "product_link_43",
              "Color_44", "Size_44", "availability_44", "images_44", "product_link_44",
              "Color_45", "Size_45", "availability_45", "images_45", "product_link_45",
              "Color_46", "Size_46", "availability_46", "images_46", "product_link_46",
              "Color_47", "Size_47", "availability_47", "images_47", "product_link_47",
              "Color_48", "Size_48", "availability_48", "images_48", "product_link_48",
              "Color_49", "Size_49", "availability_49", "images_49", "product_link_49",
              "Color_50", "Size_50", "availability_50", "images_50", "product_link_50",
              "Color_51", "Size_51", "availability_51", "images_51", "product_link_51",
              "Color_52", "Size_52", "availability_52", "images_52", "product_link_52",
              "Color_53", "Size_53", "availability_53", "images_53", "product_link_53",
              "Color_54", "Size_54", "availability_54", "images_54", "product_link_54",
              "Color_55", "Size_55", "availability_55", "images_55", "product_link_55",
              "Color_56", "Size_56", "availability_56", "images_56", "product_link_56",
              "Color_57", "Size_57", "availability_57", "images_57", "product_link_57",
              "Color_58", "Size_58", "availability_58", "images_58", "product_link_58",
              "Color_59", "Size_59", "availability_59", "images_59", "product_link_59",
              "Color_60", "Size_60", "availability_60", "images_60", "product_link_60"]

all_products = []

def write_serial_csv(fields):
    # Get the list of existing files in the /data directory
    existing_files = os.listdir('./julziscraper/data')

    # Filter out non-CSV files and extract serial numbers
    existing_serials = [int(f[:-4]) for f in existing_files if f.endswith('.csv')]

    # Determine the serial number for the new file
    if existing_serials:
        new_serial = max(existing_serials) + 1
    else:
        new_serial = 0

    # Determine the previous file (if any)
    if new_serial > 0:
        previous_file = f'./julziscraper/data/{new_serial - 1}.csv'
    else:
        previous_file = None

    # Check the status
    status = read_load_data_status()

    # If status is True, do not create a new file, only return the last indexed file
    if status:
        with open(previous_file, 'a', newline="", encoding='utf-8-sig') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fields)
        
        return previous_file, None

    # Create the new file
    new_file = f'./julziscraper/data/{new_serial}.csv'
    with open(new_file, 'w', newline="", encoding='utf-8-sig') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fields)
        csv_writer.writeheader()

    return new_file, previous_file


def read_load_data_status():
    with open("./julziscraper/loading_status.json", 'r') as file:
        data = json.load(file)
        return data.get('failed_to_load_data', True)

def write_load_data_status(status):
    with open("./julziscraper/loading_status.json", 'w') as file:
        json.dump({'failed_to_load_data': status}, file)



csv_file_path, _ = write_serial_csv(header)

# data failed to load last time, meaning we haven't completed the loading of all data, read data into all_products and set it to true, will be set to false again when the data fails to load
if read_load_data_status():
    with open(csv_file_path, 'r', newline="", encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=header)
        for row in csv_reader:
            all_products.append(row)
        write_load_data_status(False)


# if os.path.isfile('./bata.csv'):
#     with open('./bata.csv', 'r', newline="", encoding='utf-8-sig') as file:
#         csv_reader = csv.DictReader(file, fieldnames=header)
#         for row in csv_reader:
#             all_products.append(row)
#     # try:
#     #     with open("assigned_group_ids.json", "r") as file:
#     #         restored_assigned_group_ids = json.load(file)
#     # except:
#     # restored_assigned_group_ids = {}
#     file = open('bata.csv', 'a', newline="", encoding='utf-8-sig')
#     csv_writer = csv.DictWriter(file, fieldnames=header)
#     # csv_writer.writeheader()
# else:
#     file = open('bata.csv', 'w', newline="", encoding='utf-8-sig')
#     csv_writer = csv.DictWriter(file, fieldnames=header)
#     csv_writer.writeheader()

done_file = open("./julziscraper/done_ids.txt", "a+")
done_file.seek(0)
done_data = [v.strip() for v in done_file.readlines()]

auth_token = "eyJraWQiOiJKZzBUN1p0Y0xmbzhkSUpKME91aFJ3MkU0Um1FODJra2ltRWFaMzNWS1JBPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkMjQ2MzJkYi04NDBjLTRhODQtODM0Ni0yMzE4NGVkOWM4YTciLCJjb2duaXRvOmdyb3VwcyI6WyJhcC1zb3V0aC0xX3Q4ZEhXZTNnWV9BQUQtSURQIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoLTFfdDhkSFdlM2dZIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiN2p0bnFsc2JhZzFlbTUyNG4wdGZucXVoaWEiLCJvcmlnaW5fanRpIjoiODY4MjA4ZTMtNmRlMi00MTViLTkwZDUtZDk0NTVmNGE1Mjc4IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiBvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF1dGhfdGltZSI6MTY5MTAyMTg4OSwiZXhwIjoxNjkyNzIxODEyLCJpYXQiOjE2OTI3MTgyMTIsImp0aSI6ImViM2Q0ZjM4LWEzOTMtNDQ3ZC1iYTJmLWQ3Y2U0Njc2NTM4MiIsInVzZXJuYW1lIjoiYWFkLWlkcF81MjEuNTIxNjNAYmF0YS5jb20ifQ.CChAxykgWqDNLI_zfkwcNs9nB5cg5TuW3p_FE1XM4hcf65DN8OVHy2_jRufUE6NqPb_lADo0499MJKcCuthiDOH5mnAB1OoySgA9GNFslXKiiUKyceY_tVm6ME0XGhSSsxMJSZekSc-FpF90M1KfDbPB5iCCJZ9FHyrtC-PegwDXRdiTA6AAd1zzPIVMhs5eT_YgW77-kb7rMT0zygE5pkVOiZ1sKnZ_pXaYh0sTmF8CsgaSxUU5q0rLkJIiddQeyBAX2BNne20dap_cSjHbAi1t0f7oLjhdKQ6gknw87NDJYcNTkghwo1zfugpoEhgCJ0eW6V9Coheq9XwCZka5RgQ"

headers = {
    "authority": "bata-my-api.instoreapp.io",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "auth": auth_token,
    "origin": "https://bata-my.instoreapp.io",
    "referer": "https://bata-my.instoreapp.io/",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-api-key": "Rzjyz4oPcbaKxRjh37o9H807yPCpdFDK5uZgrQv9"
}


assigned_group_ids = {}


def get_images(key):
    res = requests.get(f"https://bata-my-api.instoreapp.io/sfcc/ocapi/products/productVariations/{key}", headers=headers)
    if res.status_code == 200:
        page_resp = json.loads(res.text)
        for data in page_resp["data"]:
            images = []
            for img_group in data["image_groups"]:
                if img_group["view_type"] == "large":
                    for img in img_group["images"]:
                        images.append(img["url"])
            try:
                return ','.join(images)
            except:
                return []

def get_product_id(key):
    split_string = key.rsplit('_', 1)
    return split_string[0]

def is_partial_match(product_id, done_data):
    for done_id in done_data:
        if done_id.startswith(product_id):
            return True
    return False

def get_results(category, max_count=200, offset=0, all_results=None):
    if all_results is None:
        all_results = []

    url = f"https://bata-my-api.instoreapp.io/sfcc/ocapi/productSearch?category={category}&count={max_count}&offset={offset}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if 'hits' in data:
            all_results.extend(data['hits'])

        if 'next' in data:
            return get_results(category, max_count, offset + max_count, all_results)
        else:
            return all_results
    else:
        print(f"Error: {response.status_code}")
        print(f"Error details: {response.text}")
        
        # auth_token = input("Enter new auth token:\n")
        # return get_results(category, max_count, offset, all_results)
        # print(f"Error: {response.status_code}")
        return all_results

def extract_product_id(url):
    # return url.split("/")[-1]
    pattern = r'(\d+)_1\.jpg'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def split_article_no(id):
    return id.split("_")[-1]

def load_product_data(code):
    res = requests.get(f"https://bata-my-api.instoreapp.io/sfcc/ocapi/products/productVariations/{code}", headers=headers)
    if res.status_code == 200:
        page_resp = json.loads(res.text)
        for data in page_resp["data"]:
            return data
    else:
        print('-- response 401 for id : ' + code)
        return None

def get_product(entity, data):

    item = dict()
    try: 
        item["id"] = data["id"]
    except:
        item["id"] = ""
    try:
        item["name"] = data["name"]
    except:
        item["name"] = ""
    try:
        item["product_code"] = data["c_articleNo"]
    except:
        item["product_code"] = ""
    try:
        item["type"] = data["type"]["_type"]
    except:
        item["type"] = ""
    try:
        item["variant"] = data["type"]["variant"]
    except:
        item["variant"] = ""
    try:
        item["articleNo"] = data["c_articleNo"]
    except:
        item["articleNo"] = ""
    try:
        item["CategoryCode"] = data["c_bataCategoryCode"]
    except:
        item["CategoryCode"] = ""
    try:
        item["price"] = entity["price"]
    except:
        item["price"] = ""
    try:
        item["upperDescription"] = data['c_upperDescription']
    except:
        item["upperDescription"] = ""
    try:
        item["size_type"] = data['c_sizeType']
    except:
        item["size_type"] = ""

    for index, variant in enumerate(data["variants"]):
        item[f'images_{index}'] = ''
        try:
            item[f"Color_{index}"] = variant['variation_values']["color"]
        except:
            item[f"Color_{index}"] = ""
        try:
            if 'size_shoes' in variant['variation_values']:
                item[f"Size_{index}"] = variant['variation_values']["size_shoes"]
            elif 'size_nonshoes_shoecare' in variant['variation_values']:
                item[f'Size_{index}'] = variant['variation_values']['size_nonshoes_shoecare']
            elif 'size_nonshoes_unique' in variant['variation_values']:
                item[f'Size_{index}'] = variant['variation_values']['size_nonshoes_unique']  
        except:
            item[f"Size_{index}"] = ""
        try:
            avail = variant["orderable"]
            if avail == True:
                item[f"availability_{index}"] = "Available"
            else:
                item[f"availability_{index}"] = "Not Available"
        except:
            item[f"availability_{index}"] = ""
        try:
            item[f"product_link_{index}"] = variant["link"]
        except:
            item[f"product_link_{index}"]
    return item, data["variation_groups"]


def assign_group_id(product, assigned_group_ids):
    product_id = product['product_id']
    variation_groups = product.get('variation_groups', [])

    # Check if any product in the variation_group has already been assigned a group_id
    group_id = None
    for variation in variation_groups:
        variation_id = variation['product_id']
        if variation_id in assigned_group_ids:
            group_id = assigned_group_ids[variation_id]
            break

    # If no group_id is found, generate a new group_id (UUID)
    if group_id is None:
        group_id = str(uuid.uuid4())

    # Assign the group_id to the current product and all variations in the group
    assigned_group_ids[product_id] = group_id
    for variation in variation_groups:
        assigned_group_ids[variation['product_id']] = group_id

    product['group_id'] = group_id

    return product


def assign_group_id(product, variation_groups):
    product_id = product['product_code']

    # Check if any product in the variation_group has already been assigned a group_id
    group_id = None
    for variation in variation_groups:
        variation_id = split_article_no(variation['product_id'])
        if variation_id in assigned_group_ids:
            group_id = assigned_group_ids[variation_id]
            break

    # If no group_id is found, generate a new group_id (UUID)
    if group_id is None:
        group_id = str(uuid.uuid4())

    # Assign the group_id to the current product and all variations in the group
    assigned_group_ids[product_id] = group_id
    for variation in variation_groups:
        assigned_group_ids[split_article_no(variation['product_id'])] = group_id

    product['group_id'] = group_id

    return product

def complete():
    with open("./julziscraper/assigned_group_ids.json", "w") as file:
        json.dump(assigned_group_ids, file)
    done_file.close()
    file.close()


# for each product id that you receive from bata, check the variant_groups, get the id, and load the product information from there
all_data = []
all_data.append(get_results("MY_Men"))
all_data.append(get_results("MY_Women"))
all_data.append(get_results("MY_Kids"))

print("--- all data length is --- ", sum(len(sub_list) for sub_list in all_data))

# failed_to_load_data = False


# bata_products = ['8426842','8421842','4614989', '4616989', '6319005', '6317005', '6316005']
all_colors = []

for index, data in enumerate(all_data):
    if read_load_data_status():
        break

    for index, hit in enumerate(data):
        if hit["orderable"] == False:
            continue

        id = hit["id"]
        product_id = get_product_id(id)
        # if not any(bata_id in id for bata_id in bata_products):
        #     continue
        if is_partial_match(product_id, done_data):
            continue
        print('trying to load: ', id)
        data = load_product_data(id)
        if data is None:
            write_load_data_status(True)
            # failed_to_load_data = True
            # complete()
            break

        # for this product, add all the possible colors into the color array 
        for variation in data['variation_groups']:
            all_colors.append(variation['variation_values']['color']) 
        

        color = ''
        for variation in data['variation_groups']:
            if data['c_articleNo'] in variation['product_id']:
                color = variation['variation_values']['color']
                break

        data['variants'] = sorted(data['variants'], key=lambda item: item['variation_values']['color'] != color)

        product, variation_groups = get_product(hit, data)
        # if result is not None:
        #      = result
        #     # auth_token = auth_token + "eh"
        # else:
            # auth_token = input("Enter new auth token:\n ")
            # result = get_product(hit, data)
            # if result is not None:
            #     product, variation_groups = result
            # else:
            
        # go through the variation_group, load both sets of images per variation_values
        # then loop over 53 keys, and assign image where variation_group.variation_values.color = Color_{i}
        loaded_variations = []
        ordered_variations = []

        for variation in variation_groups:
            if product['product_code'] in variation['product_id']:
                ordered_variations.insert(0, variation)
            else:
                ordered_variations.append(variation)

        for variation in ordered_variations:
            # variation_ids = {}
            for i in range(60):
                try:
                    if f'Color_{i}' not in product:
                        break
                    else:
                        color = product[f'Color_{i}']
                        #check if the variation for this color are already loaded
                        if color in loaded_variations:
                            continue
                        if color == variation["variation_values"]["color"]:
                            #load variation images 
                            product[f'images_{i}'] = get_images(variation["product_id"])
                            loaded_variations.append(color)
                            # variation_ids.append(i)
                except:
                    continue
        product = assign_group_id(product, variation_groups)

        all_products.append(product)

import re

def remove_colors_from_title(colors, title):
    # Convert the colors list to a set to remove duplicates, then convert it back to a list
    colors = list(set(colors))

    for color in colors:
        # Use regular expressions to replace color with an empty string, case-insensitively
        title = re.sub(re.compile(color, re.IGNORECASE), '', title)
    
    return title.strip()

def finalise_products(file_path):

    with open(csv_file_path, 'a', newline="", encoding='utf-8-sig') as file:
        csv_writer = csv.DictWriter(file, fieldnames=header)
        for product in all_products: 
            id = product["id"]
            product['name'] = remove_colors_from_title(all_colors, product['name'])
            csv_writer.writerow(product)
            done_data.append(id)
            done_file.write(id + '\n')
            done_file.flush()

finalise_products(csv_file_path)

complete()

print("---  script COMPLETE ---")
