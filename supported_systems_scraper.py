from bs4 import BeautifulSoup
import requests
import csv

URL = "https://retropie.org.uk/about/systems/"
r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")
table = soup.find("table", id="wpsm-table-1")

# Define the CSV headers
csv_headers = ["SYSTEM", "YEAR", "ROM_EXTENSIONS", "BIOS"]

# Extract table rows (ignore the first column which contains images)
rows = []
for row in table.find_all("tr")[1:]:  # Skip header row
    cells = [cell.get_text(strip=True) for cell in row.find_all("td")[1:]]  # Ignore the image cell
    rows.append(cells)

# Write to CSV file
with open("supported_systems.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)  # Write header row
    writer.writerows(rows)        # Write data rows

print("Data successfully written to supported_systems.csv")
