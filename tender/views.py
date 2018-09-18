from django.shortcuts import render

# Create your views here.
#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup
import urllib.parse


# Create your views here.



def tenders(request):
    prefs = ''
    # if __name__ == '__main__':

        # for tId, tender in enumerate(tenders):
        #     print(f"item# {tId}: {tender['title']} & Date:{tender['startDateFa']}")
    scraper = TendersScraper()
    tenders_items = scraper.scrape()
    return render(request, 'tenders/tenders.html', {'tenders_items': tenders_items})


class TendersScraper(object):
    def __init__(self):
        self.search_request = "term=الکترو"

    def scrape(self):
        tens = self.scrape_jobs(5)
        return tens


    def scrape_jobs(self, max_pages=3):
        tenders = []
        pageno = 1
        url = "https://www.parsnamaddata.com/parsnamad/tenders/search/find"

        querystring = {"langid": "1065"}

        term = requests.utils.quote('الکتروموتور')
        while pageno <= max_pages:
            # print(f"term= {term} & pageNo= {pageno}")
            payload = f"term={ term }&allGrpId=0&current={pageno}&status=2"
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                # 'postman-token': "4c38e3b7-7fb8-91ff-b671-485856b94cf2"
            }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

            results = response.json()
            res = results['list']
            print(res)
            pager = results['pagerData']['total']
            for x in res:
                tender = {}
                tender['title'] = x['title']
                tender['startDateFa'] = x['startDateFa']
                tender['summary'] = x['summary']
                tender['link'] = x['link']
                tender['tenderId'] = x['tenderId']
                tenders.append(tender)
            pageno += 1
        return tenders


