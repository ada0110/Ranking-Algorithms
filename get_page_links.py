from argparse import ArgumentParser
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# get all the links on the page
def get_page_links(page_url, base_url, only_internal_links=True):
    # get all the links on the page
    page_links = []

    # get page
    try:
        response = requests.get(page_url)
    except Exception as e:
        print(f"error in fetching {page_url} {e}")
        return page_links
    
    # parse the html
    soup = BeautifulSoup(response.content, 'html.parser')

    # get internal links only
    if only_internal_links:
        start_str = base_url
    # http or https
    else:
        start_str = urlparse(base_url).scheme

    for link in soup.find_all('a'):
        try:
            href = link.get('href')
            if href is None:
                continue
                
            # full link
            if href.startswith(start_str):
                page_links.append(href)
            # relative link
            elif href.startswith('/'):
                full_link = urljoin(base_url, href)
                page_links.append(full_link)
                
        except AttributeError as e:
            print(f"error in parsing {link} {e}")

    # we return ordered set of links 
    page_links = dict.fromkeys(page_links)
    return page_links


if __name__ == '__main__':
    # read arguments
    parser = ArgumentParser()
    
    parser.add_argument('-p', '--page_url',
                         default= 'https://www.iiit.ac.in/')
    parser.add_argument('-b', '--base_url',
                         default= 'https://www.iiit.ac.in/')
    
    parser = parser.parse_args()
    
    # get links on page
    print(f"fetching from page: {parser.page_url} | base: {parser.base_url}")
    page_links = get_page_links(parser.page_url, parser.base_url)
    
    for i,url in enumerate(page_links):
        print(i, url)
        

"""
Output
0 https://www.iith.ac.in/
1 https://www.iith.ac.in/academics/index.html#admissions
2 https://www.iith.ac.in/academics/programmes-offered/
3 https://www.iith.ac.in/academics/departments/
4 https://www.iith.ac.in/academics/calendars-timetables/
5 https://www.iith.ac.in/academics/index.html
6 https://www.iith.ac.in/research/researchHighlights/
7 https://www.iith.ac.in/research/facilities/
8 https://www.iith.ac.in/research/centres-incubators/
9 https://www.iith.ac.in/research/technology-transfer/
10 https://www.iith.ac.in/research/
.
.
.
"""