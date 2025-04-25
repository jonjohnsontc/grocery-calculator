# Data Model

## Main / App Schema

categories:
  category_id: int pk,
  parent_id: int,
  name: text

products:
  item_id: identity generated pk,
  category_id: int,
  name: text,
  size: int,
  unit: text

product_tags:
  item_id: identity,
  tag: text
  (item_id, tag is pk) 

coupons:
  item_id: identity,
  value: decimal,
  store_id: int,
  exp: date,
  type: text or enum

price_history:
  store_id: int,
  item_id: identity,
  date: date,
  price: decimal

stores:
  store_id: int,
  name: text,
  address: text,
  city: text,
  zip_code: int
  location_lat: decimal,
  location_long: decimal,

store_selection:
  store_id: int,
  item_id: identity, 
  price: decimal,
  last_found: date

store_coupon_policies:
  store_id: int,
  category: text,
  min_spend: decimal,
  discount_type: text 

## File Ops Schema

ingest_metadata:
  file_name: text,
  store_name: text,
  search_term: text,
  pull_timestamp: timestamp with tz,
  source_url: text,
  status: pending

## Preprocess Schema

target_preprocess:
  id: int,
  product_detail: text,
  price: text,
  orig_price: text,
  price_per: text
  created_at: timestamp with tz

(I don't know if this is necessary because the info is well-labeled)
tjoes_preprocess:
  pass

ralphs_preprocess:
  pass

## Categories / Tags

I want to be able to capture what the product is, generally. I'm thinking that the most simple way to do that is through tags or categories. I would like to prevent situations like 1 jar peanut butter to not result in "1 Chobani Flip Low-Fat Chocolate Peanut Butter Cup Greek Yogurt", and rather result in 1 jar of Jif or Skippy peanut butter.

If i have to provide some proper form of measurement with the product (e.g., 1 40oz Jar Peanut Butter), the chances of that kind of thing happening if I just search the title are smaller, I think. 

What if I don't want to be super specific? Are there situations that might benefit me doing that? I'm thinking something more generalized, like dinner ideas for two weeks, and the associated ingredients. Something like that might be good, but I also don't want to cast too wide of a net in terms of functionality. So, I think I'll have some kind of root form or category that I will reference.

---

I'm going to end up referencing both, having an heirarchical set of "Categories", for which each item will be a part of one. This necessitates a "Categories" table for which I need to setup.

--- 

I'm thinking I could also add the flavor or variant attribute to the product_name. Because I'm going to be writing plain text, I don't know if I'm going to be able to easily parse it to figure out which parts are 'favor or variant' and which parts are the product name

## Preprocessing Data

Taking in raw data from scraped sources, and converting into the data model above. I've been thinking about it as a two-step process. 

- Spit data into preprocess table with high-level details about the raw data
- Preprocess that data into the final data model (normalization, add categories/tags, etc)

Theoretically, it could be a one-step process, where the data goes from the scraped result to the data model directly. Could I do that?

- Import in scraped data
- Magic
  - extract title from scraped data
  - not use category or base it off of some rules based process
  - nothing goes in tags
- Data is stored in data-model

I think having it be a multi-step process is probably better. Especially since I can use a combination of automated and manual labeling after the scraping.

## Full-Text Search

It seems like other companies / software uses full-text search to rank and retrieve results according to their relevance. Rather than trying to build a query that will allow me to search for sizes, flavors, or tags, I can leverage FTS to search them all. One idea I've been thinking, is that I could just append all descriptive information about a product from a retailer into a product_description column, and then use that for FTS

