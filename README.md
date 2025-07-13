# HomeAdvisor Scraper 

This project is a Scrapy spider designed to crawl and extract cost data from [HomeAdvisor's Cost Guide](https://www.homeadvisor.com/cost/).

## Spider: `cost_spider`

### What it Extracts:
- Project title
- Average cost
- Normal cost range (low/high)
- Highlights
- Cost factors
- URL of each cost page

##  Example Run


scrapy crawl cost_spider -o costs.json

{
  "title_of_project": "Install a Roof",
  "average_cost": "$10,000",
  "normal_range_low_cost": "$7,000",
  "normal_range_high_cost": "$13,000",
  "highlights": "Includes labor and materials; Based on national averages",
  "cost_factors": "Size, materials, labor rates, location...",
  "website_url": "https://www.homeadvisor.com/cost/..."
}

