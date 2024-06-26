from bs4 import BeautifulSoup as bs 
import requests
import re
def onerow(reviewbox):

    
    date = [reviewbox.find('meta',{'itemprop':'datePublished'})['content']]
    subline = reviewbox.find('h3', {'class': 'text_sub_header userStatusWrapper'})
    name = [subline.find('span', {'itemprop': 'name'}).text]

    # Extract the place
    place = reviewbox.find('h3').text.strip()
    match = re.search(r'\((.*?)\)', place)  #Learn regex properly
    place = [match.group(1) if match else '']

    row = date + name + place
    parameters = {
        'aircraft': '',
        'type_of_traveller': '',
        'seat_type': '',
        'route': '',
        'date_flown': '',
        'seat_comfort': '0',
        'cabin_staff_service': '0',
        'food_and_beverages': '0',
        'inflight_entertainment': '0',
        'ground_service': '0',
        'value_for_money': '0',
        'recommended': '',
        'ratingvalue': '0',
        'review_title': '',
        'verification': '',
        'review_content': ''
    }

    table = reviewbox.find('table')
    if table:
        r = table.find_all('tr')
        for row_elem in r:
            header = row_elem.find('td', {'class': 'review-rating-header'})
            value_td = row_elem.find('td', {'class': 'review-value'})
            stars_td = row_elem.find('td', {'class': 'review-rating-stars'})

            if header and value_td:
                key = header['class'][1]
                value = value_td.text.strip()
                parameters[key] = value
                
            elif header and stars_td:
                key = header['class'][1]
                stars = stars_td.find_all('span', {'class': 'star fill'})
                parameters[key] = str(len(stars))
        

    rev = reviewbox.find('div',{'itemprop':'reviewRating'})
    review = rev.find('span').text.strip() if rev else ''
    parameters['ratingvalue'] = review

    
    body = reviewbox.find('h2').text.replace('"',"").strip()
    parameters['review_title'] = body

    para = reviewbox.find('div',{'class':'text_content'}).text.strip()
    verify, paragraph = para.split("|",1) if "|" in para else ('', para)
    parameters['verification'] = verify.strip()
    parameters['review_content'] = paragraph.strip()

    row.extend([
        parameters['aircraft'],
        parameters['type_of_traveller'],
        parameters['seat_type'],
        parameters['route'],
        parameters['date_flown'],
        parameters['seat_comfort'],
        parameters['cabin_staff_service'],
        parameters['food_and_beverages'],
        parameters['inflight_entertainment'],
        parameters['ground_service'],
        parameters['value_for_money'],
        parameters['recommended'],
        parameters['ratingvalue'],
        parameters['review_title'],
        parameters['verification'],
        parameters['review_content']
    ])

    return row

# page_no = 10
# page_size = 100
# base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
def run(page_no, page_size, base_url):
    rows=[]
    for i in range(1,page_no+1):
        url = f"{base_url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"    
        html = requests.get(url)
        soup = bs(html.content, 'html.parser')
        fullbox = soup.find_all('article',{'itemprop':'review'})
        for reviewbox in fullbox:
            rows.append(onerow(reviewbox))
        print(f"   ---> {len(rows)} total reviews")
    return rows
# run(page_no, page_size, base_url)