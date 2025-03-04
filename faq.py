import json
import pandas as pd

# Load the scraped JSON data
file_path = "C:/Users/HP/PycharmProjects/avatar/Digiflex_Avatar/digiflex_full_data.json"  # Update this path if needed
with open(file_path, "r", encoding="utf-8") as file:
    scraped_data = json.load(file)

# Convert title, description, keywords to DataFrame
df_summary = pd.DataFrame([{
    "Title": scraped_data.get("title", "N/A"),
    "Description": scraped_data.get("description", "N/A"),
    "Keywords": scraped_data.get("keywords", "N/A")
}])

# Convert headings to DataFrame
headings_data = []
for level, texts in scraped_data.get("headings", {}).items():
    for text in texts:
        headings_data.append({"Heading Level": level, "Text": text})
df_headings = pd.DataFrame(headings_data)

# Convert paragraphs to DataFrame
df_paragraphs = pd.DataFrame({"Paragraphs": scraped_data.get("paragraphs", [])})

# Convert unordered lists to DataFrame
list_data = []
for unordered_list in scraped_data.get("lists", {}).get("unordered", []):
    for item in unordered_list:
        list_data.append({"List Type": "Unordered", "Text": item})
df_lists = pd.DataFrame(list_data)

# Convert tables to DataFrame
table_data = []
for table in scraped_data.get("tables", []):
    headers = table["headers"]
    for row in table["rows"]:
        row_data = dict(zip(headers, row)) if headers else {"Row Data": row}
        table_data.append(row_data)
df_tables = pd.DataFrame(table_data)

# Convert forms to DataFrame
form_data = []
for form in scraped_data.get("forms", []):
    for inp in form.get("inputs", []):
        form_data.append({
            "Form Action": form.get("action", "N/A"),
            "Method": form.get("method", "GET"),
            "Input Name": inp.get("name", "N/A"),
            "Input Type": inp.get("type", "text")
        })
df_forms = pd.DataFrame(form_data)

# Convert images to DataFrame
df_images = pd.DataFrame({"Image URLs": scraped_data.get("images", [])})

# Convert scripts to DataFrame
df_scripts = pd.DataFrame({"Script URLs": scraped_data.get("scripts", [])})

# Convert embedded content to DataFrame
df_embedded = pd.DataFrame({
    "Iframes": scraped_data.get("embedded_content", {}).get("iframes", []),
    "Videos": scraped_data.get("embedded_content", {}).get("videos", [])
})

# Convert links to DataFrame
link_data = []
for link in scraped_data.get("links", {}).get("internal", []):
    link_data.append({"Link Type": "Internal", "URL": link})
for link in scraped_data.get("links", {}).get("external", []):
    link_data.append({"Link Type": "External", "URL": link})
df_links = pd.DataFrame(link_data)

# Save DataFrames to CSV
df_summary.to_csv("data/summary.csv", index=False, encoding="utf-8")
df_headings.to_csv("data/headings.csv", index=False, encoding="utf-8")
df_paragraphs.to_csv("data/paragraphs.csv", index=False, encoding="utf-8")
df_lists.to_csv("data/lists.csv", index=False, encoding="utf-8")
df_tables.to_csv("data/tables.csv", index=False, encoding="utf-8")
df_forms.to_csv("data/forms.csv", index=False, encoding="utf-8")
df_images.to_csv("data/images.csv", index=False, encoding="utf-8")
df_scripts.to_csv("data/scripts.csv", index=False, encoding="utf-8")
df_embedded.to_csv("data/embedded.csv", index=False, encoding="utf-8")
df_links.to_csv("data/links.csv", index=False, encoding="utf-8")

print("✅ Data successfully structured and saved as CSV files.")

