import os
import numpy as np
import boto3
import configparser

from datetime import datetime
from dateutil.relativedelta import relativedelta

from data_generator import (
    generate_customers,
    generate_products,
    generate_transactions,
)
print("reading config data")
config = configparser.ConfigParser()
config.read('infra/config.ini')

# read AWS credentials from config file instead of hardcoding in the code. Config file is placed in the infra folder of the project directory

aws_access_key = config['aws_secrets']['aws_access_key']
aws_secret_access_key = config['aws_secrets']['aws_secret_access_key']
aw_region = config['aws_secrets']['aws_region']
bucket_name = config['directory_config']['bucket_name']
local_root_dir = config['directory_config']['local_root_dir']
customers_dir = config['directory_config']['customers_dir']
products_dir = config['directory_config']['products_dir']
transactions_dir = config['directory_config']['transactions_dir']

# The function is designed to load the files to respective S3 folders automatically instead of manual loading

def uplloadGeneratedFilesToS3():
    s3 = boto3.resource(
    service_name='s3',
    region_name= aw_region,
    aws_access_key_id = aws_access_key, 
    aws_secret_access_key= aws_secret_access_key
    )
    print("Connected to s3")
    try:
        root_path = f"{local_root_dir}"

        bucket = s3.Bucket(bucket_name)

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\", "/")
            directory_name = path.replace(root_path, "").strip("/")
            print(directory_name + '/')
            for file in files:
                bucket.upload_file(os.path.join(path, file), directory_name + '/' + file)
                print("Uploaded the File:"+file)

    except Exception as err:
        print(err)


if __name__ == "__main__":
    np.random.seed(seed=42)

    products_data = {
        "house": [
            "detergent",
            "kitchen roll",
            "bin liners",
            "shower gel",
            "scented candles",
            "fabric softener",
            "cling film",
            "aluminium foil",
            "toilet paper",
            "kitchen knife",
            "dishwasher tablets",
            "ice pack",
        ],
        "clothes": [
            "men's dark green trousers",
            "women's shoes",
            "jumper",
            "men's belt",
            "women's black socks",
            "men's striped socks",
            "men's trainers",
            "women's blouse",
            "women's red dress",
        ],
        "fruit_veg": [
            "avocado",
            "cherries",
            "scotch bonnets",
            "peppers",
            "broccoli",
            "potatoes",
            "grapes",
            "easy peeler",
            "mango",
            "lemon grass",
            "onions",
            "apples",
            "raspberries",
        ],
        "sweets": [
            "carrot cake",
            "salted caramel dark chocolate",
            "gummy bears",
            "kombucha",
            "ice cream",
            "irn bru",
        ],
        "food": [
            "steak",
            "chicken",
            "mince beef",
            "milk",
            "hummus",
            "activated charcoal croissant",
            "whole chicken",
            "tuna",
            "smoked salmon",
            "camembert",
            "pizza",
            "oats",
            "peanut butter",
            "almond milk",
            "lentil soup",
            "greek yoghurt",
            "parmesan",
            "coconut water",
            "chicken stock",
            "water",
        ],
        "bws": [
            "beer",
            "vodka",
            "rum",
            "soda water",
            "scotch",
            "whiskey",
        ],
    }
    products_cats_frequency = (
        ["house"] * 15
        + ["clothes"] * 5
        + ["fruit_veg"] * 25
        + ["sweets"] * 20
        + ["food"] * 25
        + ["bws"] * 10
    )
    
    # gen_id = "convex-insurance-test-data"
    output_location = f".{local_root_dir}"
    print(output_location)
    output_loc_customers = f"{output_location}/{customers_dir}"
    os.makedirs(output_loc_customers, exist_ok=True)
    print(output_loc_customers)
    os.makedirs(output_loc_customers,exist_ok=True)
    gen_customers = generate_customers(output_loc_customers, 137)
    output_loc_products = f"{output_location}/{products_dir}"
    os.makedirs(output_loc_products, exist_ok=True)
    print(output_loc_products)
    product_id_lookup = generate_products(output_loc_products, products_data)
    
    output_loc_transactions = f"{output_location}/{transactions_dir}"
    os.makedirs(output_loc_transactions, exist_ok=True)
    print(output_loc_transactions)
    
    end_date = datetime.today()
    delta = relativedelta(months=2)
    start_date = end_date - delta

    generate_transactions(
        output_loc_transactions,
        gen_customers,
        products_data,
        product_id_lookup,
        products_cats_frequency,
        start_date,
        end_date,
    )
    # call function to load data to S3 folders
    uplloadGeneratedFilesToS3()
