import requests

from bs4 import BeautifulSoup
import json

URL = "https://en.wikipedia.org/wiki/History_of_Mexico"

def  get_citations_needed_count(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  all_results = soup.find_all('a', title="Wikipedia:Citation needed")
  return len(all_results)


def get_citations_needed_report(URL):
    response = requests.get(URL)
    paragraphs = BeautifulSoup(response.content, 'html.parser').find(id="bodyContent").find_all('p')
    citations = []

    for p in paragraphs:
        if p.find_all('a', title='Wikipedia:Citation needed'):
            paragraph = p.text
            citation_count = paragraph.count ("[citation needed")
            i = 0

            while i < citation_count:
                partition = paragraph.split("[citation needed]")
                citation_dict = {"sentence": partition[0]}
                paragraph = paragraph.replace(partition[0], "", 1)
                paragraph = paragraph.replace("[citation needed]", "", 1)
                citations.append(citation_dict)
                i += 1

    json_object = json.dumps(citations, indent=4)
    with open('reports.json', 'w') as f:
        f.write(json_object)

    result = ""   
    for c in citations:
        result += (f"Citation needed for: \"{c['sentence']}\n\n")

    return result

print("THE NUMBER OF CITATIONS", get_citations_needed_count(URL))
print(get_citations_needed_report(URL))



if __name__ == "__main__":
    print("web_scraping is done")