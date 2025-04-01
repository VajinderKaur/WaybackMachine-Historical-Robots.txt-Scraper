import pandas as pd

def extract_all_blocked_crawlers(robots_txt):
    """Extract all crawlers explicitly blocked in robots.txt"""
    blocked = set()
    if pd.isna(robots_txt):   # If no content in RobotTxt, returns ""
        return ""

    lines = robots_txt.splitlines() #Split RobotTxt in single lines.
    current_agent = None

    for line in lines:
        line = line.strip().lower() #Removes whitespaces and convert everything into lower case.

        # Detect user agents
        if line.startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()  #extracts the agent 

        # Check for disallow rules
        elif line.startswith("disallow:") and current_agent: #if that line has disallow under that particular agent, adds that into blocked crawler list.
            # Add the crawler to the blocked list
            blocked.add(current_agent)     

    return ", ".join(blocked) if blocked else ""

# Load your CSV with the `robots.txt` content
df = pd.read_csv("Group2.csv")

# Extract all blocked crawlers
df['Blocked_Crawlers'] = df['RobotsTxt'].apply(extract_all_blocked_crawlers)

# Save the results to a new CSV
output_file = "Blocked.csv"
df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
