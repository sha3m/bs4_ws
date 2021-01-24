from bs4 import BeautifulSoup
import requests
import re

header = ({'User-Agent':
            # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
           # 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
           'Accept-Language': 'en-US, en;q=0.5'
           })

URL_list = [
    "https://www.amazon.de/Zewa-Toilettenpapier-zuverl%C3%A4ssiger-Komfortlagen-Qualit%C3%A4t-Vorratspack/dp/B01C7109VE",
    "https://www.amazon.de/Tena-Night-Monats-Paket-Einlagen-Packungen/dp/B06XYJ4PF3",
    "https://www.amazon.de/Tena-Lady-Maxi-Night-Duo/dp/B01N9R7TKX/ref=mp_s_a_1_55?dchild=1&keywords=tena&qid=1610983502&sr=8-55",
]

items_info = ""

def title_str(pg_contents):
    try:
        title_id = pg_contents.find("span", attrs={"id": 'productTitle'})
        attrib_string = title_id.string.strip()
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def img_urls(pg_contents):
    try:
        img_url = pg_contents.find(id="imgTagWrapperId")
        attrib_string = img_url.img.get("data-a-dynamic-image")
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def descr_str(pg_contents):
    try:
        descr_id = pg_contents.find("div", attrs={"id": 'productDescription'})
        attrib_string = descr_id.get_text().strip()
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def review_count(pg_contents):
    try:
        review_id = pg_contents.find("span", attrs={'id': 'acrCustomerReviewText'})
        attrib_string = review_id.string.strip()
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def ratings_str(pg_contents):
    try:
        ratings_id = pg_contents.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'})
        attrib_string = ratings_id.string.strip()
    except AttributeError:
        try:
            ratings_id = pg_contents.find("span", attrs={'class': 'a-icon-alt'})
            attrib_string = ratings_id.string.strip()
        except AttributeError:
            attrib_string = ""
    return f"{attrib_string}|"


def price_str(pg_contents):
    try:
        price_id = pg_contents.find("span", attrs={"id": 'priceblock_ourprice'})
        attrib_string = price_id.string.strip()
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def availability_str(pg_contents):
    try:
        avail_str = pg_contents.find("div", attrs={"id": 'availability'})
        attrib_string = avail_str.find("span").string.strip()
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def bullets_str(pg_contents):
    try:
        bullet_points = pg_contents.find("div", attrs={"id": 'feature-bullets'})
        descript = filter(None, bullet_points.text.split("\n"))
        attrib_string = "".join(descript)
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


def asinumber(urlink):
    asin = re.search(r'/[dg]p/([^/]+)', urlink, flags=re.IGNORECASE)
    attrib_string = asin.group(1)
    return f"{attrib_string}|"


def brand_str(pg_contents):
    # table id = "productDetails_techSpec_section_1"
    try:
        brand = pg_contents.find("table", attrs={"id": 'productDetails_techSpec_section_1'})
        attrib_string = brand.text.split("\n\n\n")[-2]
    except AttributeError:
        attrib_string = ""
    return f"{attrib_string}|"


for URL in URL_list:
    webpage = open(URL).read()
    # webpage = requests.get(URL, headers=header)
    page_content = BeautifulSoup(webpage, "lxml")
    items_info += title_str(page_content)
    items_info += img_urls(page_content)
    items_info += descr_str(page_content)
    items_info += brand_str(page_content)
    items_info += review_count(page_content)
    items_info += ratings_str(page_content)
    items_info += price_str(page_content)
    items_info += availability_str(page_content)
    items_info += bullets_str(page_content)
    items_info += asinumber(URL) + "\n"
    with open('ws_info.csv', 'a', newline='') as csvfile:
        csvfile.write(items_info)
    items_info = ""
# todo user-agent check
