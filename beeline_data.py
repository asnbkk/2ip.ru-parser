from bs4 import BeautifulSoup
import requests
import csv

url = 'https://2ip.ru/isp-reviews/Beeline+KZ/?pageId=1&orderBy=id&itemPerPage=10'

csv_file = open('beeline_review.csv', 'w')

csv_wirter = csv.writer(csv_file)
csv_wirter.writerow(['date', 'location', 'total_rating',
                     'speed_small_rating', 'availability_small_rating',
                     'support_small_rating_tab', 'price_quality_small_rating',
                     'headline', 'summary'])


def get_data(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def get_next_page_link(soup):
    paginator = soup.find('ul', {'class': 'pagination pagination-review'})
    if paginator:
        url = 'https://2ip.ru/isp-reviews/Beeline+KZ/' + \
            str(paginator.find(
                'a', {'class': 'pagination__link pagination__link-next'})['href'])
        return url
    else:
        return


def get_total_rating(rating):
    if 'star-full' in rating:
        return 1
    elif 'star-1-2' in rating:
        return 0.5
    elif 'star-1-5' in rating:
        return 0.2
    elif 'star-2-5' in rating:
        return 0.4
    elif 'star-3-5' in rating:
        return 0.6
    elif 'star-4-5' in rating:
        return 0.8
    else:
        return 0


while True:
    soup = get_data(url)
    url = get_next_page_link(soup)
    print(url)

    for card in soup.find_all('div', {'class': 'reviewItem__inner'}):

        headline = card.find('div', {'class': 'reviewItem__title'}).text
        print(headline)

        summary = card.p.text
        print(summary)

        location = card.find(
            'a', {'class': 'reviewItem__city reviewItem__link'}).text
        print(location)

        date = card.find('div', {'class': 'reviewItem__date'}).span.text
        print(date)

        total_rating_tab = card.find(
            'div', {'class': 'rating reviewItem__rating'})
        total_rating = 0
        for star in total_rating_tab.find_all('img'):
            total_rating += get_total_rating(star['src'])
        print(total_rating)

        small_rating = card.find(
            'div', {'class': 'provider-rating__more reviewRating__more'})

        speed_small_rating_tab = small_rating.find_all(
            'div', {'class': 'provider-rating__item'})[0]
        speed_small_rating = 0
        for star in speed_small_rating_tab.find_all('img'):
            speed_small_rating += get_total_rating(star['src'])
        print(speed_small_rating)

        availability_small_rating_tab = small_rating.find_all(
            'div', {'class': 'provider-rating__item'})[1]
        availability_small_rating = 0
        for star in availability_small_rating_tab.find_all('img'):
            availability_small_rating += get_total_rating(star['src'])
        print(availability_small_rating)

        support_small_rating_tab = small_rating.find_all(
            'div', {'class': 'provider-rating__item'})[2]
        support_small_rating = 0
        for star in support_small_rating_tab.find_all('img'):
            support_small_rating += get_total_rating(star['src'])
        print(support_small_rating)

        price_quality_small_rating_tab = small_rating.find_all(
            'div', {'class': 'provider-rating__item'})[3]
        price_quality_small_rating = 0
        for star in price_quality_small_rating_tab.find_all('img'):
            price_quality_small_rating += get_total_rating(star['src'])
        print(price_quality_small_rating)

        print()

        csv_wirter.writerow([date, location, total_rating,
                            speed_small_rating, availability_small_rating,
                            support_small_rating,
                            price_quality_small_rating, headline, summary])

        if not url:
            csv_file.close()
            break
