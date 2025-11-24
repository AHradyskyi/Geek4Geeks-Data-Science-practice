import requests
import pandas as pd
from bs4 import BeautifulSoup


# list to store scraped data
all_quotes = []
all_fieldnames = set(['Quote', 'Author']) 

# this part of the url is constant
base_url = "http://quotes.toscrape.com/"

# this part of the url will keep changing
url = "/page/1"

while url:
  
    # concatenating both urls
    # making request
    res = requests.get(f"{base_url}{url}")
    print(f"Scrapping {base_url}{url}")
    soup = BeautifulSoup(res.text, "html.parser")

    # extracting all elements
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        row_data = {}
        row_data["Quote"] = quote.find("span", class_="text").get_text(strip=True)
        row_data["Author"] = quote.find("small", class_="author").get_text(strip=True)
            
            # Extract tags and assign to dynamic keys (tag1, tag2, ...)
        tags_list = quote.find("div", class_="tags").find_all("a", class_="tag")
            
        for i, tag in enumerate(tags_list, 1):
            tag_key = f"tag{i}"
            row_data[tag_key] = tag.get_text(strip=True)
                # Keep track of all fieldnames we encounter globally
            all_fieldnames.add(tag_key)

        all_quotes.append(row_data)
        
       
    next_btn = soup.find(class_="next")
    url = next_btn.find("a")["href"] if next_btn else None
        
df = pd.DataFrame(all_quotes)
df.to_csv('scraped_products.csv', index=False)



