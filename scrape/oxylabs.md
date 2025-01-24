# Exploring OxyLabs API offering

I just signed up for a 7-day trial of OxyLabs, I'm wondering if I can access local pricing information for Ralphs and Target. If so, I think this could be super helpful for scraping their offerings. 

I have my credentials in my password manager, and I'm wondering if I can programmatically access them from there, as opposed to creating an env file.

## Welcome Message


```bash
curl ''https://realtime.oxylabs.io/v1/queries'' --user 'lookingferdata_YrfEV:memo~BEATING~carlton~p4ris~better' -H 'Content-Type: application/json' -d '{"source": "universal", "url": "https://sandbox.oxylabs.io/"}'
```

## Target

- Target requires the full url to scrape
- It gives you the some of the same results you'd expect after traveling to the page manually and using EasyScraper, except
  - Coupons aren't shown (must be related to my user)
