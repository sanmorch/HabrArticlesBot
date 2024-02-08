import requests
from bs4 import BeautifulSoup
from config import URL_TOPICS, URL_FLOW, URL_BASIC
import article


# обход всех страниц и получение всех разделов
def parse_topics():
    i = 1
    page = requests.get(URL_TOPICS + str(i))
    i_end = int(BeautifulSoup(page.content, "html.parser").find_all("a", class_="tm-pagination__page")[-1].text.strip())
    topics = []
    while i <= i_end:
        soup = BeautifulSoup(page.content, "html.parser")
        block = soup.find_all("a", class_="tm-hub__title")
        for el in block:
            topics.append(el.find_all("span"))
        i = i + 1
        page = requests.get(URL_TOPICS + str(i))
    topics = [x.text for xs in topics for x in xs]
    return topics


# получение статей из определенного FLOW
def parse_by_flow(flow):
    page = requests.get(URL_FLOW + str(flow) + '/articles/')
    articles = []
    soup = BeautifulSoup(page.content, "html.parser")
    block = soup.find_all("div", class_="tm-article-snippet tm-article-snippet")
    for el in block:
        author = el.find("a", class_="tm-user-info__username").text.strip()
        time_added = el.find("time", datetime=True)["datetime"].strip()
        title = el.find("a", class_="tm-title__link").text.strip()
        if not el.find("span", class_="tm-article-complexity__label"):
            complexity = None
        else:
            complexity = el.find("span", class_="tm-article-complexity__label").text.strip()
        if not el.find("span", class_="tm-article-reading-time__label"):
            minutes_to_read = None
        else:
            minutes_to_read = int(el.find("span", class_="tm-article-reading-time__label").text.strip().split()[0])
        url = URL_BASIC + el.find("a", class_="tm-title__link", href=True)["href"].strip()
        art = article.Article(author, time_added, title, complexity, minutes_to_read, url)
        articles.append(art)
    return articles

