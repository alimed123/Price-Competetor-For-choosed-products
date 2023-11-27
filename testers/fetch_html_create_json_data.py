import requests
import json
import re

def fetch_webpage_content(url):
    response = requests.get(url)
    return response.text

def extract_json_from_script_tags(html_content):
    pattern = r'<script.*?type="application/json".*?id="ProductJson-product-template".*?>(.*?)<\/script>'
    script_data = re.findall(pattern, html_content, re.DOTALL)
    return script_data[0] if script_data else None

def extract_meta_tags(html_content):
    pattern = r'<meta.*?property="og:(.*?)".*?content="(.*?)".*?>'
    meta_tags = re.findall(pattern, html_content)
    return {property_name: content for property_name, content in meta_tags}

def main():
    user_input = input("Please enter URL: ")
    url = user_input
    html_content = fetch_webpage_content(url)
    script_data = extract_json_from_script_tags(html_content)
    meta_tags_data = extract_meta_tags(html_content)

    if script_data:
        try:
            json_data = json.loads(script_data)
            json_data.update(meta_tags_data)
            print(json.dumps(json_data, indent=4))
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON data: {e}")
    else:
        print("No JSON data found.")

if __name__ == "__main__":
    main()