import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv, os

flatten = lambda l : [item for sublist in l for item in sublist]

href_url = lambda url : "https://en.wikipedia.org" + url

def get_page_content_bfsoup(url, parser="html5lib"):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content.decode(), parser)
    return content

def get_texts(*urls, depth=4, i=0, path="data/", title="first"):
    urls = list(urls)
    title = title.replace("/","")
    while len(urls) and depth:
        print(i, depth)
        url = urls.pop()
        content = get_page_content_bfsoup(url)

        paragraphs = []
        for field in content.find_all('p'):
            paragraphs.append(field.text)

        with open(path+title+".txt", "w") as file:
            for paragraph in paragraphs:
                file.write(paragraph)
        i += 1
        for a in content.find_all('a'):
            if 'title' in a.attrs:
                title = a.attrs["title"]
            elif len(paragraphs) and len(paragraphs[0])>5:
                title = paragraphs[0][:5]
            else:
                continue
            if 'class' not in a.attrs and 'href' in a.attrs and title not in os.listdir():
                try:
                    i = get_texts(href_url(a.attrs["href"]), depth=depth-1, i=i, title=title)
                except Exception as e:
                    continue
    return i


get_texts("https://en.wikipedia.org/wiki/Portal:Current_events")
