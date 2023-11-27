# import sys
# sys.path.insert(1, '/home/marketpro/public_html/dev/common')
# from main_error import email_error_report
# import traceback

# except Exception as err:
#     trace = traceback.format_exc()          
#     email_error_report(subject="K2F Coupon SMS - Neto API Fetch",error=err,trace=trace,json_get_customer=json_get_customer)

import sys
# sys.path.insert(1, '/home/marketpro/public_html/dev/common')
from helpers.main_email import send_email
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

def email_error_report(**kwargs):

    dict_items = locals()['kwargs'] #locals() returns a dict with both argument's name and value
    subject = dict_items["subject"] 

    body = ""
    for key, value in dict_items.items(): 
        # logging.info("%s %s", key, value)
        if key != "subject":
            body += f"{key} = {value} \n"            

    send_email(os.getenv(f"{ENV}EMAIL"),subject,body)


# except Exception as err:
#     trace = traceback.format_exc()          
#     email_error_report(subject="K2F Coupon SMS - Neto API Fetch",error=err,trace=trace,json_get_customer=json_get_customer)