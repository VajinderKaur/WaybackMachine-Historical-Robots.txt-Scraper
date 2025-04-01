import asyncio
import aiohttp
import pandas as pd
from datetime import datetime

# Function to convert date to timestamp string format (Wayback Machine timestamp)
def convert_to_timestamp(year, month):
    return datetime(year, month, 1).strftime("%Y%m%d%H%M%S")

# Function to extract user-agent from robots.txt content by going through each line and extracts where the line starts with `user-agent'
def extract_user_agent(robots_txt):
    user_agents = []
    for line in robots_txt.splitlines():
        if line.lower().startswith('user-agent:'):
            user_agents.append(line.split(':', 1)[1].strip())
    return user_agents

# Fetch Wayback Machine timestamps using CDX API - https://archive.org/developers/wayback-cdx-server.html
async def fetch_cdx_data(session, domain, start_timestamp, end_timestamp):
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/robots.txt&output=json&filter=statuscode:200"
    
    try:
        async with session.get(cdx_url) as response: # an asynchronous GET request
            if response.status == 200:  # Only getting sucessfull captures and skipping errors like 404(Page not Found), 403(Forbidden), 500(Server Problem) etc.
                data = await response.json()  # Output in JSON
                timestamps = [entry[1] for entry in data[1:]]  # Skip header row
                return [ts for ts in timestamps if start_timestamp <= ts <= end_timestamp] 
            else:
                print(f"Failed to fetch CDX for {domain}: {response.status}")
                return []
    except Exception as e:
        print(f"Error fetching CDX for {domain}: {e}")
        return []

# Fetch robots.txt file for each timestamp.
async def fetch_robots_txt(session, timestamp, domain):
    url = f"https://web.archive.org/web/{timestamp}id_/{domain}/robots.txt"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                return content
            else:
                print(f"Failed to fetch robots.txt for {domain} at {timestamp}: {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Process a single domain
async def process_domain(session, domain, start_timestamp, end_timestamp, sleep_interval):
    all_data = []

    # Fetch timestamps from CDX
    timestamps = await fetch_cdx_data(session, domain, start_timestamp, end_timestamp)
    
    if not timestamps:
        print(f"No records found for {domain} in the specified range.")
        return []

    # Fetch robots.txt content for each timestamp by fetch_robots_txt function
    for timestamp in timestamps:
        print(f"Fetching {domain} at {timestamp}...")
        
        robots_txt = await fetch_robots_txt(session, timestamp, domain)
        
        if robots_txt:
            user_agents = extract_user_agent(robots_txt) # Extracts UserAgents
            
            for user_agent in user_agents:          
                all_data.append({
                    "Domain": domain,
                    "Timestamp": timestamp,
                    "UserAgent": user_agent,
                    "RobotsTxt": robots_txt
                })

        await asyncio.sleep(sleep_interval)

    return all_data

# Main function to scrape robots.txt data for all the domains.
async def scrape_historical_robots(domains, start_month, start_year, end_month, end_year, output_file, sleep_interval=0.05):
    start_timestamp = convert_to_timestamp(start_year, start_month)
    end_timestamp = convert_to_timestamp(end_year, end_month)

    async with aiohttp.ClientSession() as session:
        tasks = [process_domain(session, domain, start_timestamp, end_timestamp, sleep_interval) for domain in domains] #Concurrent domain tasks

        # Gather all results concurrently
        all_results = await asyncio.gather(*tasks)

        # Flatten results
        all_data = [item for sublist in all_results for item in sublist]

        # Save to CSV
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_csv(output_file, index=False)
            print(f"Data saved to {output_file}")   #Putting everything in one file.
        else:
            print("No data scraped.")

# Function to run the scraper
def run_scraper():
    domains = [
        "time.com", "spiegel.de", "fortune.com", "entrepreneur.com",
        "latimes.com"]  #Domain URLs
    
    start_month, start_year = 3, 2025
    end_month, end_year = 4, 2025
    output_file = "Group1.csv"

    # Run the asyncio event loop
    asyncio.run(scrape_historical_robots(domains, start_month, start_year, end_month, end_year, output_file))

# Run the scraper
if __name__ == "__main__":
    run_scraper()

