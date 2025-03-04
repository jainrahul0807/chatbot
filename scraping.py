import requests
from bs4 import BeautifulSoup
import json
# import pandas as pd

# Function to fetch and preprocess website data
# def fetch_and_preprocess_data(url):
#     # Send GET request to the website
#     try:
#         response = requests.get(url)
#         if response.status_code != 200:
#             print("Failed to retrieve the webpage.")
#             return None
#
#         # Parse the webpage content with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Extract the title of the webpage (as an example)
#         title = soup.title.string.strip() if soup.title else "No Title Found"
#
#         # Example: Extracting all paragraphs from the page
#         paragraphs = soup.find_all('p')
#         paragraph_texts = [para.get_text().strip() for para in paragraphs if para.get_text().strip()]
#
#         # Example: Extracting all links from the page
#         links = soup.find_all('a')
#         links_list = [link['href'] for link in links if link['href'].startswith('http')]
#
#         # Clean extracted data (for example, removing unwanted characters)
#         # clean_paragraphs = [re.sub(r'\s+', ' ', para) for para in paragraph_texts]
#
#         # Preprocessing links to ensure they are unique
#         # unique_links = list(set(links_list))
#
#         # Return the results as a dictionary
#         return {
#             'title': title,
#             'paragraphs': paragraph_texts,
#             'links': links_list
#         }
#     except Exception as e:
#         print("Error scraping webpage:", str(e))
#         return None

# def fetch_and_preprocess_data(url):
#     """
#     Fetches and processes key data from a webpage:
#     - Title
#     - Meta Description & Keywords
#     - Headings (H1, H2, H3)
#     - Important Text Content
#     - All Links (Internal & External)
#     """
#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         if response.status_code != 200:
#             print("❌ Failed to retrieve the webpage.")
#             return None
#
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Extract Page Title
#         title = soup.title.string.strip() if soup.title else "No Title Found"
#
#         # Extract Meta Description & Keywords
#         meta_desc = soup.find("meta", attrs={"name": "description"})
#         meta_keywords = soup.find("meta", attrs={"name": "keywords"})
#         description = meta_desc["content"].strip() if meta_desc else "No description available"
#         keywords = meta_keywords["content"].strip() if meta_keywords else "No keywords available"
#
#         # Extract Headings (H1, H2, H3)
#         headings = {
#             "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
#             "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
#             "h3": [h.get_text(strip=True) for h in soup.find_all("h3")]
#         }
#
#         # Extract Important Paragraphs
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 20]
#
#         # Extract All Links (Internal & External)
#         links = {
#             "internal": [],
#             "external": []
#         }
#
#         for link in soup.find_all("a", href=True):
#             href = link["href"]
#             if href.startswith("http"):
#                 links["external"].append(href)
#             else:
#                 links["internal"].append(href)
#
#         # Remove duplicate links
#         links["internal"] = list(set(links["internal"]))
#         links["external"] = list(set(links["external"]))
#
#         # Store extracted data in a structured dictionary
#         extracted_data = {
#             "title": title,
#             "description": description,
#             "keywords": keywords,
#             "headings": headings,
#             "paragraphs": paragraphs,
#             "links": links
#         }
#
#         # Save data to a JSON file
#         with open("scraped_data.json", "w", encoding="utf-8") as file:
#             json.dump(extracted_data, file, indent=4, ensure_ascii=False)
#
#         print("✅ Data successfully scraped and saved to 'scraped_data.json'.")
#         return extracted_data
#
#     except Exception as e:
#         print(f"❌ Error scraping webpage: {e}")
#         return None

def fetch_and_preprocess_data(url):
    """
    Scrapes and processes **detailed** data from a webpage, including:
    - Title, Meta Description & Keywords
    - All Headers (H1 - H6)
    - Text Content (Paragraphs, Lists, Tables)
    - Images, Scripts, Forms
    - All Internal & External Links
    - Embedded Content (Iframes, Videos)
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print("❌ Failed to retrieve the webpage.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Title
        title = soup.title.string.strip() if soup.title else "No Title Found"

        # Extract Meta Description & Keywords
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        description = meta_desc["content"].strip() if meta_desc else "No description available"
        keywords = meta_keywords["content"].strip() if meta_keywords else "No keywords available"

        # Extract All Headings (H1 - H6)
        headings = {f"h{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

        # Extract Paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 20]

        # Extract Lists (UL & OL)
        lists = {
            "unordered": [[li.get_text(strip=True) for li in ul.find_all("li")] for ul in soup.find_all("ul")],
            "ordered": [[li.get_text(strip=True) for li in ol.find_all("li")] for ol in soup.find_all("ol")]
        }

        # Extract Tables (Headers + Rows)
        tables = []
        for table in soup.find_all("table"):
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows = [[td.get_text(strip=True) for td in row.find_all("td")] for row in table.find_all("tr")]
            tables.append({"headers": headers, "rows": rows})

        # Extract Forms (Input Fields & Actions)
        forms = [
            {
                "action": form.get("action"),
                "method": form.get("method", "GET"),
                "inputs": [
                    {"name": inp.get("name"), "type": inp.get("type", "text")}
                    for inp in form.find_all("input")
                ]
            }
            for form in soup.find_all("form")
        ]

        # Extract Images & Scripts
        images = [img["src"] for img in soup.find_all("img", src=True)]
        scripts = [script["src"] for script in soup.find_all("script", src=True)]

        # Extract Iframes & Videos
        embedded_content = {
            "iframes": [iframe["src"] for iframe in soup.find_all("iframe", src=True)],
            "videos": [video["src"] for video in soup.find_all("video", src=True)]
        }

        # Extract All Links (Internal & External)
        links = {"internal": [], "external": []}
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("http"):
                links["external"].append(href)
            else:
                links["internal"].append(href)

        # Remove duplicates
        links["internal"] = list(set(links["internal"]))
        links["external"] = list(set(links["external"]))

        # Store extracted data
        extracted_data = {
            "title": title,
            "description": description,
            "keywords": keywords,
            "headings": headings,
            "paragraphs": paragraphs,
            "lists": lists,
            "tables": tables,
            "forms": forms,
            "images": images,
            "scripts": scripts,
            "embedded_content": embedded_content,
            "links": links
        }

        # # Save data to a JSON file
        # with open("scraped_complete_data.json", "w", encoding="utf-8") as file:
        #     json.dump(extracted_data, file, indent=4, ensure_ascii=False)

        # print("✅ Data successfully scraped and saved to 'scraped_complete_data.json'.")
        return extracted_data

    except Exception as e:
        print(f"❌ Error scraping webpage: {e}")
        return None



def is_api_endpoint(url):

    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get('Content-Type', '').lower()

        # Check if the response is JSON
        if 'application/json' in content_type:
            return True

        # Try parsing the response as JSON
        try:
            data = response.json()
            if isinstance(data, (dict, list)):  # JSON is usually a dict or list
                return True
        except ValueError:
            pass  # Not a JSON response

    except requests.RequestException:
        print("Failed to fetch the URL.")

    return False

def fetch_and_clean_api_data(url):
  try:
    response=requests.get(url)
    if response.status_code != 200:
          print("Failed to retrieve the API data.")
          return None
    try:
      # Parse the JSON response
          data = response.json()
    except requests.JSONDecodeError:
            print("❌ Error: API response is not valid JSON.")
            return None
    if isinstance(data, dict):
            data = [data]

    if not isinstance(data, list):  # Ensure it's a list before processing
            print("❌ Unexpected API response format.")
            return None

        # Cleaning: Remove null, empty, or 'N/A' values
    cleaned_data = [
            {k: v for k, v in item.items() if v not in [None, '', 'N/A']}
            for item in data
        ]

    return cleaned_data if cleaned_data else None  # Return None if empty

  except requests.RequestException as e:
        print("❌ Error fetching API data:", str(e))
        return None

def save_to_json(data, filename):
    """
    Saves the given data to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print("Error saving JSON file:", str(e))

def process_url(url):
    """
    Determines if the URL is an API or a webpage, fetches data accordingly, and saves it as JSON.
    """
    if is_api_endpoint(url):
        print(f"🔍 Detected API endpoint: {url}")
        data = fetch_and_clean_api_data(url)
        filename = 'data.json'
    else:
        print(f"🔍 Detected Webpage: {url}")
        data = fetch_and_preprocess_data(url)
        filename = 'data.json'

    if data:
        save_to_json(data, filename)
    else:
        print("No data fetched.")

def save_json_as_text(json_file,text_file):
    try:
        # Load JSON data
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON to a readable text format
        text_content = json.dumps(data, indent=4)  # Pretty format JSON

        # Save to a text file
        with open(text_file, "w", encoding="utf-8") as file:
            file.write(text_content)

        print(f"✅ JSON data saved as text in {text_file}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Example Usage

if __name__ == "__main__":
    url_input = "https://digiflex.ai/"
    process_url(url_input)
    save_json_as_text("data.json", "output.txt")
