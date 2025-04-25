# System Design

The potential high-level components are:

Data Ingestion
  - Coupon Scanning Service + Ingestion
  - Weekly Ad Scanning Service + Ingestion
  - Receipt Ingestion Service
  - TJoes Ingestion Service from traderjoesprices
  - Manual website scraping
    - Target
    - Ralphs
    - Trader Joe's
    - Vons (maybe)
    - Jons (maybe)

Data Storage
  - Feature DB

CLI/Frontend
  - cli app

Solver
  - LP/MIP Solver

## Data Ingestion

### Drive-By Scraping

I want to focus on ways of getting price data for groceries in bulk. I'm thinking of either automated or manual "drive-by" scraping of search results on each of the grocers that I'm closest to. Drive-by scraping meaning, using something like EasyScraper (Chrome extension), and searching terms like "Peanut Butter", and other things that I purchase frequently on each of the three stores.

Pros:
  - Relatively simple setup process, I don't even think I'm going to be using any scripts for data capture
  - I can't imagine that not working for simple queries
  - Difficult for servers to detect I'm doing anything
  - Don't have to rely on named entity recognition or anything like that to separate prices or sizing

Cons:
  - Going to take time manually searching things
  - I don't know if I'll be able to easily differentiate temporary or promotional pricing easily

#### Design

- I want to drive by scrape into a number of csv input files using EasyScraper
- I want to have some interface that I've built to "clean" the csv data and transform it into data to insert into postgres
- I *think* I'm going to write this service in Scala, just to give myself some more exposure
- The actual data transformations will likely be done in postgres with scala as the glue
- I *think* I want to manually review & tag elements before the ingest job;
  - I could also have an automated LLM/GPT tagger
- I think at first blush, it's probably easier for me to think about this as a set of transformations I can execute on a dataframe
- Create temporary table to read data into
- execute set of transformations and write results into tables
  - products
  - product_tags
  - price_history
  - store_selection

##### Step 1 | Ingest grocier ads/website into db

- Store scraped data into "data/raw/<store>/<filename>.csv"
  - Where <store> is one of trader-joes | target | ralphs
  - Where <filename> is <search-term>-<datetime>
    - shows when it was pulled <datetime> 
    - reflects the search term that was used to get resuts <search-term>

- Develop Interface for using postgres to execute transformations
- Could also use something like DuckDB or SQLite, which would be a little more portable (in the sense that I just have a single binary alongside a store)
  - I think OLAP makes more sense given the nature of the problem, so maybe I pick duckDB here

- Take input data in columnar format
  - obstensibly, each row will have a different item
  - add product to products table if it doesn't exist already (check via hash SHA256)
  - add product to store_selection table if it doesn't exist already (if it's in products, it should be in store_selection)  
  - add product row to price_history table
  - if product is discounted as a deal, then we can add the deal to the coupons table

- Each input file is going to be based off of a specific store, so i think i should have those represented by the time they get there (aka, stores should be already added to the database in the `stores` table)

- Size constraints investigation
  - One year of pricing information for trader joes is pretty small (105.6MB)
  - There are 2412 items
  - If I say Target & Ralphs have 5x the items, 
    - 10k each, and likely include more price changes as well
    - 110 * 5 = 550MB (for 6 mos) * 2 = 1.5GB data += trader_joes = 1.8GB maybe

- Target and Ralphs are going to list the original price and the sale price
  - During ingestion I will caputure this information and add it to the coupons table
  - I should also check if there is a coupon for the store (esp Target/Ralphs) when I'm ingesting data, and add exp date of ingestion if not already

### Manual Tagging

Categories and Tags are both things that I want the ability to manually override pretty easily. DML to the Feature DB is one way of doing that, but I'm wondering if there's some other step that I should be considering. Something as simple as editing a spreadsheet before it gets converted and ingested might just be what I do. 

### GPT Tagging | Named Entity-Recognition

I think language models are going to help out in two general areas, tagging / catgorizing items on ingest from scraping, and also with respect to coupons that are scanned  

## User Journey

I type up grocery list and input it into the cli tool. The cli tool spits out a grocery plan

```md
# Example Plan

- Bagels
- Pasta 2lbs
- Extra Creamy Oatmilk
- Coca-Cola 2 liter
- Potato Bread
- 80/20 ground beef 1lb

```

I think, for simplicity's sake, I'm just going to return a JSON document with objects representing different grocery trips where I can get all of the foods

```json
{   
    "no_trips": 2,
    "total_cost": 89.91, 
    "trips": [
    -- See below
    ]
}

-- Here is the trips list:

[
    {
        "store": "ralphs",
        "location": "3927 Hollywood Blvd., Los Angeles, CA 90027",
        "store_total": "29.27",
        "items": [
                    {
                        "search_term": "Bagels",
                        "product_name": "Thomas' Original Bagels",
                        "qty": 1,
                        "price": "3.99"
                    }
                 ]
    }
]
```

## CLI App | Interface

I imagine I will call the app like:

```bash
grocery_calculator list.txt --no-stores 2
```

The app will parse the text file into a list of groceries, and then run a search for matching entities in the database. Any entities that can't be matched will be logged as an error, but will not prevent the application from returning with a partial list of groceries to buy.

After conducting a search for all parsed items, we will (normalize them for solving (tbd)), and return the list of groceries to purchase in json format.

