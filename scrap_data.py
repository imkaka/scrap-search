import json
from time import sleep

import requests
from bs4 import BeautifulSoup


def parse(u_url, headers):
    title = '-'
    submit_by = '-'
    description = '-'
    calories = 0
    ingredients = []
    rec = {}

    try:
        r = requests.get(u_url, headers=headers)

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            # title
            title_section = soup.select('.recipe-summary__h1')
            # submitter?
            submitter_section = soup.select('.submitter__name')
            # description
            description_section = soup.select('.submitter__description')
            # ingredients
            ingredients_section = soup.select('.recipe-ingred_txt')
            # calories
            calories_section = soup.select('.calorie-count')
            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()

            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})

            if description_section:
                description = description_section[0].text.strip().replace('"', '')

            if submitter_section:
                submit_by = submitter_section[0].text.strip()

            if title_section:
                title = title_section[0].text

            rec = { 'title': title,
                    'submitter': submit_by,
                    'description': description,
                    'calories': calories,
                    'ingredients': ingredients
                    }
    except Exception as e:
        print("Exception while parsing")
        print(str(e))
    finally:
        return json.dumps(rec)

def parse_website(url, headers):
    r = requests.get(url, headers=headers)
    links = None
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.fixed-recipe-card__h3 a')
    return links

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    links = parse_website(url, headers)
    if links:
        for link in links:
            sleep(2)
            result = parse(link['href'], headers)
            print(result)
            print('===========================================')




if __name__ == "__main__":
    main()





