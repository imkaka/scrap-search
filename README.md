# Scrap-Search
An example program that scrapes data from AllRecipes.com and store in Elasticsearch.

It is built while learning elasticsearch basics.

### Setup and Run
* `fetch_recipies.py` is the main script.
* `python fetch_recipies.py fetch` will scrap saldas data and put it in ES.
* `python fetch_recipies.py search` will give the search res against the query defined in `fetch_recipies.py`

#### Note:
* You can customize every script accordingly.
* we can run `scrap_data.py` seperately just to scrap salads and print, It is independent.
