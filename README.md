# Historical-Robots.txt-Scraper
## Objective
This research project analyzes how online publishers have modified their `robots.txt` files over time in response to the rise of generative AI-based search engines. Your task is to systematically collect and analyze historical robots.txt data from selected publishers using the Internet Archive's Wayback Machine.

## What is `robots.txt` File?
`robots.txt` is simply a text file which contains information or rather rules about which part of the website are web crawlers and search engines allowed to access. It is like a written format about the structure of the website and which nodes are accessible by which engines and bots.
`*` means all the web crawlers or search engines are either allowed or disallowed based on `Allow` or `Disallow` option for the node.
### For example:
`User-agent: *` --- All the bots are not allowed to /private/ and /admin/    
`Disallow: /private/`   
`Disallow: /admin/`    

`User-agent: Google-Extended` --- Google-Extended is allowed to /public/    
`Allow: /public/`   

## Time Frame 
June 2023 to March 2025

## Group A 

https://time.com/robots.txt   
https://www.spiegel.de/robots.txt    
https://fortune.com/robots.txt    
https://www.entrepreneur.com/robots.txt    
https://www.latimes.com/robots.txt    
https://www.independent.co.uk/robots.txt   
https://www.adweek.com/robots.txt    
https://www.blavity.com/robots.txt    
https://www.prisa.com/robots.txt    
https://www.rtl.de/robots.txt    

## Group B

https://www.nytimes.com/robots.txt    
https://www.wsj.com/robots.txt   
https://www.washingtonpost.com/robots.txt    
https://www.bbc.com/robots.txt    
https://www.theguardian.com/robots.txt     
https://www.bloomberg.com/robots.txt    
https://www.businessinsider.com/robots.txt    
https://www.vox.com/robots.txt    
https://www.wired.com/robots.txt    
https://www.forbes.com/robots.txt    

## Description of the Files

### Code 
1. `main.py` : Contains code to get the data for the list of domains. Process the requests concurrently for the user provided timeframe. Creates a csv file with User selected name which contains robots.txt content, timestamp, user agent and domains.
2. `blocked.py`: Helps in reading the robots.txt contents in the dataset and further extracting Blocked crawlers from the domains. Created column `Blocked_Crawlers`
3. `Preprocessing.py`: Merging datasets with same timelines and different domains as well as same domains but different timelines. This is helpful when data is extracted in pieces due to slow response from the website and breaking task into small pieces to fasten the process. This file also contains code for collapsing User-Agent column as the original dataset will contain multiple rows with different user agents for the same stamps. 
4. `EDA.rmd`: Contains functions for loading data, converting timestamps into proper format, creating frequency plots and heatmaps. Additional study is done on the exceptional cases as well. 
5. `main.rmd`: Contains R code for scraping robots.txt. This extracts more details such as Rule (`Allow`, `Disallow`), Path (Path for which this Rule is about) in addition to the `main.py`. But this creates larger files due to more details.
6. `requirement.txt`: Required libraries for the python code.

### Reports
1. `Report_for_Historical_Robots_txt_Retrieval.pdf` : Main report containig all the details related to project objective, code, visualizations and challenges faced during data collection.
2. `EDA.pdf`: Report for just Exploratory Data analysis explaining the functions used for visuals and data visualizations.

### Data
1. `UpdatedGroup1.csv`: Group A publishers data
2. `UpdatedGroup2.csv`: Group B publishers data except the guardian.com which couldn't be retrived due to it being redirected to \us and \international for the snapshots. Work in progress for these kind of cases.
3. `historical_robots_data1.csv`: Sample data extracted from the `main.rmd`

### Visuals
Contains the visuals from `EDA.rmd`. Heatmaps and Frequency Plots

## Reference
As a reference for this project, we utilized the open-source GitHub repository: https://github.com/alexlitel/historical-robots-txt-parser/blob/master/historical_robots/scraper.py. However, our final implementation deviates significantly from the original version. Using this base code, we optimized and extended the functionality with additional features, including:
1. Custom timeframes for retrieval,
2. Extraction of robots.txt file contents and associated domains,
3. Concurrent request handling for efficiency.

Thus, the final code used in this project is mostly custom-built.
