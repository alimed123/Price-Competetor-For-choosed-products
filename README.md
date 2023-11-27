# product-spyder

## System requirements
Recommended Python version: `>= 3.11.2`

## Install Dependencies
`$ pip install -r requirements.txt`

## Packages Overview
[Ultimate Sitemap Parser](https://ultimate-sitemap-parser.readthedocs.io/en/latest/index.html)  
[Dotenv](https://github.com/theskumar/python-dotenv)  
[Extruct](https://pypi.org/project/extruct/)  
[ZenRows](https://www.zenrows.com/)

## Environment Variables

This project is using `dotenv` to setup environment variables.  
Use the `.env.example.dev` file, supply your credentials and rename it to `.env`


## Competitor Product Scraper

Since the Application still has no front-end, the app utilizes different CSV file inputs to complete various tasks.  

Staring file:  
`product_spyder.py`  

#### Input files  

`input_urls.csv` - Use this to scrape competitor products.

`is_use_sitemap_parser` (`Default: False`)  
- `True` - When `True` will use the ultimate-sitemap-parser
- `False` - When `False` will not use usp, but user is required input product page urls.

`input_competitor_scrape_price.csv` - Use this to scrape competitor product prices.  
- When scraping  competitor prices, it is required to scrape/add the product pages first since it will validate if the product exists on the competitor_pages table.

## User Product Scraper

Starting files:  

All of the user's files are under `/users/` folder except for some function tasks in the `/helpers/` folder

`/manual_product_upload/manual_product_upload.py` - This file is responsible for uploading User's product to the database
`/users/user_scrape_products.py` - This file is responsible for scraping the User's website site-wide using USP.
`/users/user_price_scraper.py` - This file runs after `user_scrape_products.py`, as the name suggest, it scrapes the prices.
`/users/user_manual_input_scrape.py` - This file is where the User will input individual product pages with its corresponding competitor pages.

#### User input files

`/manual_product_upload/input_manual_product_upload.csv` - Use this if you just want to upload the Users products to the database.

`user_input_urls.csv` - Use this to scrape User's product pages using ultimate-sitemap-parser.

`user_input_manual_list.csv` - Use this if you don't want to use ultimate-sitemap-parser to save User's product pages. Users are required to have two columns:
- `Url` - User's product page
- `Competitor Product Page` - The corresponding Competitor's product page.
- Optional Columns - May be required if you want to get the Competitor products' **Lowest Price** and **Price Beat By**.
	- `Cost Price` - Given by the user
	- `Mark Up Percentage` - Given by the user
	- `Mark Up Dollar Value` - Given by the user
	- `Miminum Sale Price Manual` - If no Cost Price, Mark Up Percentage/Mark Up Dollar Value is given, this will be required.
	- `Price Beat By Percentage` - Given by the user, use to calculate Price Beat By
	- `Price Beat By Dollar Value` - Given by the user, if no Price Beat By Percentage given, this is required.

- It is important that the URLs on the `Competitor Product Page` exists in the competitor_pages tables, if they don't exist, then run the URLs using the `input_urls.csv` with `is_use_sitemap_parser = False`

`input_user_scrape_price.csv` - Use this to scrape user product prices site-wide. Make sure that the user's page exist in the user_product_pages table, if not run the URLs using the `user_input_urls.csv` with `user_input_manual_list.csv`

## Main Function

`main.py` - This is the main function. It contains several task functions:  

`process_scrape_google_for_competitors()` - This is the function that is responsible for tracking the user's website (Price Action computations) and scrape competitors from Google SERP using ZenRows. It accepts the CSV file input `/input_user_scrape_google.csv` and the number of threads you want to run (1-10).  

`generate_reports_scrape_google_for_competitors()` - After running the process_scrape_google_for_competitors() function, the application then runs the function that will generate the CSV Reports and Email the price actions to the User's specified email.  

`update_products_online_shop()` - This function is responsible for updating the online shops (`NETO` and `Google Merchant Center`). (WIP)  

`spyder()` - This is the function that will call all of the task functions in the Competitor Product Scraper and the User Product Scrapers. Just uncomment this function in the `main` to be able to use it. Make sure you supply the right CSV Input files.

## Neto

All of the functions for the NETO Product API integration can be found in the `/neto/` folder. Its main file is the `neto_update_price_by_json.py` file.

## Google Merchant

All of the functions for updating Google Merchant Center are under the `/google_merchant/` folder. Its main file is the `google_content_merchant_center.py` file.

## Helper Functions

Inside the `/helpers/` folder are the different helper functions for the application (Database connection, Price Action computation, String manipulation, etc.)  

`db_connect.py` - Function to establish database connection  
`fetch_html_create_json.py` - Functions to scrape page and convert into JSON data  
`get_price_calculations.py` - Functions to calculate prices  
`json_parser.py` - Function to convert JSON String into Python dictionary  
`main_email.py` - Functions to send generated emails to the User  
`main_error.py` - Functions to send generated error reports to the User  
`price_db_tasks.py` - Functions to store price actions to the database  
`price_scrape_with_extruct.py` - Function that uses extruct module package to scrape page price  
`price_scraper.py` - Functions that uses Beautiful Soup package to scrape page for price  
`proxies.py` - Functions that lets you use proxies when requesting the page
`special_case_search.py` - Functions that are used when searching specific keys/values on a page (Used in bcf.com)  
`substring_processor.py` - Functions to manipulate/process strings  
`urlchecker.py` - Functions to check if a URL exists in the database (Use to check if the url is New/Old/Redirected)
`user_agent.py` - Functions that returns random user-agents for requests
`zenrows_json_search.py` - Function used when you want to use ZenRows' parsed option
`zenrows.py` - Functions used when you want to use normal ZenRows' normal options

## Testers

Inside the `/testers/` folders are some functions that get tested before being integrated into the main applications.  

`bcf_tester.py` - Tester for the bcf.com website's api.bazaarvoice.com API request  
`fetch_html_create_json_data.py` - Tester when requesting an HTML or JSON data of a page  
`match_confidence_tester.py` - Match confidence tester for K2F MPN and UPC codes (WIP)  
`multithreading-test.py` - Used to test the multi-threading  
`sitemap_decompressor.py` - Tester for scraping sitemaps with `.xml.gz` formats  
`soupas.py` - Used to test MPN/UPC code searching using Beautiful Soup  
`usp_tester.py` - Ultimate Sitemap Parser tester  
`zenrows_search_code_tester.py` - Tester for finding the MPN/UPC code when ZenRows returns a parsed JSON data


## Required Folders

These are the required folders that needs to be created. They will store all of the generated CSV files and text outputs. Starting in the root folder.

- `/check_url_status/` - Use to store Competitors URLS status (3xx, 4xx, 5xx)
- `/csvfiles/` - Use to store scrape pages using USP
- `/inspection/` - Use to store scrape sitemaps for inspection
- `/pending_queue/`- Use to store scrape sitemaps for sitemap pending queue
- `/users/check_urls_status/` - Use to store User's page status (3xx, 4xx, 5xx)
- `/users/csvfiles/` - Use to store User's scrape pages using USP
- `/users/inspection/` - Use to store User's sitemap for inspection
- `/users/pending_queue/` - Use to store User's sitemap pending queue
- `/users/price_action/` - Use to store Price Action reports
- `/users/response_data/` - Use to store response data from ZenRows and/or Beautifulsoup
- `/users/user_google_competitor/` - Use to store the Price Action consolidated report (Price Action summary and Competitor lists)