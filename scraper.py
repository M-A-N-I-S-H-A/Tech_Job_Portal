import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_indeed(query="python developer", location="India", pages=5):
    base_url = "https://www.indeed.com/jobs"
    jobs = []

    # Better User-Agent to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for page in range(pages):
        params = {"q": query, "l": location, "start": page * 10}
        
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Warning: Failed to fetch page {page + 1}. Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all job cards. Note: Indeed's class names change frequently.
        for job_card in soup.find_all("div", class_="job_seen_beacon"):
            
            title_tag = job_card.find("h2", class_="jobTitle")
            company_tag = job_card.find("span", class_="companyName")
            location_tag = job_card.find("div", class_="companyLocation")
            link_tag = job_card.find("a", href=True)

            jobs.append({
                "title": title_tag.text.strip() if title_tag else None,
                "company": company_tag.text.strip() if company_tag else None,
                "location": location_tag.text.strip() if location_tag else None,
                "link": "https://www.indeed.com" + link_tag["href"] if link_tag and link_tag.get('href') else None
            })

    df = pd.DataFrame(jobs)
    df.to_csv("jobs.csv", index=False) 
    print(f"✅ Jobs scraped: {len(jobs)} entries saved to jobs.csv")
    return df

if __name__ == "__main__":
    print("Running scraper standalone...")
    scrape_indeed(pages=1)
    print("Scraper run complete.")
