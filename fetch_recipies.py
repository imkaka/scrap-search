import json
import sys
from time import sleep

import search as se
import scrap_data as sd


def search_query(index_name, query):
    es = se.connect_elasticsearch()
    if es is not None:
        se.search(es, index_name, query)

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    links = sd.parse_website(url, headers)

    if links:
        if len(links) > 0:
            es = se.connect_elasticsearch()

        for link in links:
            sleep(2)
            result = sd.parse(link['href'], headers)
            if es is not None:
                if se.create_index(es, 'recipes'):
                    out = se.store_record(es, 'recipes', result)
                    print('Data indexed successfully')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'fetch':
            print("Data fetching is in process..")
            main()
        elif sys.argv[1] == 'search':
            # search_object = {'query': {'match': {'calories': '102'}}}
            # search_object = {'_source': ['title'], 'query': {'match': {'calories': '102'}}}
            search_object = {'_source': ['title'], 'query': {'range': {'calories': {'gte': 20}}}}
            search_query('recipes', json.dumps(search_object))
        else:
            sys.stderr.write(f"Usage: {sys.argv[0]} [fetch] [search]")
    else:
        sys.stderr.write(f"Usage: {sys.argv[0]} [fetch] [search]")

