# julziscraper
 
1. Get access token from `Auth` header
2. Replace the value of `auth_token` in `bata.py` LINE 168
3. run bata.py

when seeing `-- response 401 for id : xxxx`, repeat above steps, until you only see:
---  script COMPLETE ---
WITHOUT any 401. That's when you know the script has finished.

After the script is completed successfully, run `light.py`.
Upload `output.csv` into shopify


BEFORE EACH FRESH RUN (DAY):

- Delete old `bata.csv` + `done_ids.txt`
- start running `bata.csv`


521D_2020_5429739_040

failed: 521D_2020_5612458_060 