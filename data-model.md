# Data Model

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

<!-- Here is a potential table that I'm thinking about to store metadata from raw files -->
ingest_metadata:
  file_name: text,
  store_name: text,
  search_term: text,
  pull_timestamp: timestamp with tz,
  source_url: text,
  status: pending

## Categories / Tags

I want to be able to capture what the product is, generally. I'm thinking that the most simple way to do that is through tags or categories. I would like to prevent situations like 1 jar peanut butter to not result in "1 Chobani Flip Low-Fat Chocolate Peanut Butter Cup Greek Yogurt", and rather result in 1 jar of Jif or Skippy peanut butter.

If i have to provide some proper form of measurement with the product (e.g., 1 40oz Jar Peanut Butter), the chances of that kind of thing happening if I just search the title are smaller, I think. 

What if I don't want to be super specific? Are there situations that might benefit me doing that? I'm thinking something more generalized, like dinner ideas for two weeks, and the associated ingredients. Something like that might be good, but I also don't want to cast too wide of a net in terms of functionality. So, I think I'll have some kind of root form or category that I will reference.

---

I'm going to end up referencing both, having an heirarchical set of "Categories", for which each item will be a part of one. This necessitates a "Categories" table for which I need to setup.

