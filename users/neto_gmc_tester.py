from neto_gmc import *
from google_merchant_center import *
from neto_func import *

#testing product


product={'Brand': None,
 'MPN': None,
 'Condition': 'new',
 'Availability': 'Out of Stock',
 'Identifier_exists': 'no',
 'Quantity': 0,
 'Sale_Price': '24.00 AUD',
 'Price': '35.00 AUD',
 'ID': 'SPD-6INCH-HATCH-LID',
 'Link': 'https://www.kayaks2fish.com/6-inches-round-twist-hatch-lid-cover',
 'Title': 'K2F 6 Inches Round Twist Hatch Lid/Cover - Kayaks2Fish - Afterpay & Zippay Available',
 'Image_Link': 'https://www.kayaks2fish.com/assets/full/SPD-6INCH-HATCH-LID.jpg',
 'Description': 'K2F 6 Inches Round Twist Hatch Lid/Cover 6 Inches Round Twist Hatch Lid/Cover Kayaks2Fish Introducing the 6inch Hatch Lid Water Resistant and Versatile! This hatch lid is specially designed to fit on an 8inch round flat surface such as a deck or kayak cockpit (avoiding low spots and cargo wells). Found on Pro Puffin NextGen 10 Mk2 NextGen 1+1 NextGen 11 Package includes 1x 6 inch hatch 8x Screws &ampnbsp ',
 'Product_Type': 'Accessories-Kayaks2Fish',
 'Google_Product_Category': 'Sporting Goods > Outdoor Recreation > Boating & Water Sports > Boating & Rafting > Kayak Accessories',
 'Shipping_Label': 'postagepaid',
 'Shipping_Weight': '0.3000 kg',
 'GTIN': None,
 'Promotion_ID': '10off500order'}

#Check if product is on GMC
gmc_products=fetch_products()

print(gmc_products)


if gmc_products:
    #Get all SKUs in gmc
    offer_ids=[i["offerId"] for i in gmc_products]
    if product["ID"] in offer_ids:
        print("Product is already in GMC\n updating started ")
    else:
        print("Product not available on GMC \n Adding product started")
        insert_product_unique(product)
else:
    print("GMC feed is empty\nAdding product")
    insert_product_unique(product)
    offer_ids=[product["ID"]]


#Get child SKUs
if "-V" in product["ID"][-2:]:   #Fix this
    childskus=[]

    print("Getting Child SKUs")
    childskus_p=neto_childsku_p(product["ID"])
    for i in childskus_p["Item"]:
        childskus.append(i["SKU"])
else:
    childskus=[]
    print("Fetching Parentsku")
    parentSKU_p=get_parentSKU(product["ID"])
    childskus_p=neto_childsku_p(parentSKU_p["Item"][0]["ParentSKU"])
    defaultprice=childskus_p["Item"][0]["DefaultPrice"]
    for i in childskus_p["Item"]:
        childskus.append(i["SKU"])

print(f"child SKUs are \n {childskus}")


testing_price="26.00"

if float(testing_price) > float(defaultprice):
    print("Price changing found\n")
    print("changing price started\n")
    lt=neto_gmc_price_updater(testing_price,childskus,offer_ids)
