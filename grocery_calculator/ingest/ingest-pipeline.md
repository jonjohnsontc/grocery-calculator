# Ingest Design

I'm ingesting raw csv files from 2 different sources to start with:
    - Ralphs
    - Target

I think I might also fork the Trader Joe's pricing list, or put together a small solution to do it myself. It might also just end up in tabular/csv format
    - Trader Joes

## High Level Steps

1. Unzip file and load into temporary table or dataframe
2. Configure metdata for file, and check to see if it's present in the metadata table
    a. If so, we can skip the file
    b. Otherwise, continue
3. Add metadata for file to metadata db
4. Validate that each row is valid (has the following we'd expect to find in the same place as always)
    a. A product name 
    b. A single price
    c. A single size
    d. (Optional) a promotional price
5. Normalize the input data
    a. product name is all lower case
    b. remove special characters
    c. (Not sure) remove stop words from name
6. Hash the products
    a. Hash the product name + the quantity (its size)
    b. Search and see if it's been stored before
        - If it has, we update the price and it's price history
        - If it hasn't, we store everything new
7. Store the data in tables  

## Interface

- COPY data from input to db
- VALIDATE data looks as we expect it to
- NORMALIZE input data
- HASH the product
- CHECK if its stored
- STORE/UPDATE info