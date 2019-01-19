from django.contrib import messages
import request.templatetags.functions as funcs
from django.shortcuts import render, render_to_response, redirect

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
    key = ''
    if 'key' in request.POST:
        key = request.POST['key']

    scraper = TendersScraper()
    tenders_items = scraper.scrape(key)
    aria_tender = AriaTender()
    aria_items = aria_tender.scrape(key)

    # return render(request, 'requests/admin_jemco/tenders/tenders.html', {'tenders_items': tenders_items, 'aria_tenders': aria_items, 'key': key})
    return render(request, 'tenders/tenders.html', {'tenders_items': tenders_items, 'aria_tenders': aria_items, 'key': key})

def find_tenders(key=''):
    prefs = ''
    scraper = TendersScraper()
    parsnamad_items = scraper.scrape(key)
    aria_tender = AriaTender()
    aria_items = aria_tender.scrape(key)
    return parsnamad_items, aria_items


def render_tenders(request, parsTender, ariaTender, key=''):
    print('05')
    # return render(request, 'requests/admin_jemco/tenders/tenders.html', {'tenders_items': parsTender, 'aria_tenders': ariaTender, 'key': key})
    return redirect('requests/admin_jemco/tenders/tenders.html', {'tenders_items': parsTender, 'aria_tenders': ariaTender, 'key': key})


def tenders_admin(request, key='', path_to_html_file=''):

    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')

    if 'key' in request.POST:
        key = request.POST['key']
    pars_tenders, aria_tenders = find_tenders(key)
    path_to_html_file = 'requests/admin_jemco/tenders/tenders.html'
    # render_tenders(pars_tenders, aria_tenders, key)
    return render(request, 'requests/admin_jemco/tenders/tenders.html', {'tenders_items': pars_tenders, 'aria_tenders': aria_tenders, 'key': key})


class TendersScraper(object):
    def __init__(self):
        self.search_request = "term=الکترو"

    def scrape(self, key=''):
        tens = self.scrape_jobs(5, key)
        return tens


    def scrape_jobs(self, max_pages=3, key = ''):
        tenders = []
        pageno = 1
        url = "https://www.parsnamaddata.com/parsnamad/tenders/search/find"

        querystring = {"langid": "1065"}

        term = requests.utils.quote('الکترو')
        term = requests.utils.quote(key)
        while pageno <= max_pages:
            # print(f"term= {term} & pageNo= {pageno}")
            payload = f"term={term}&allGrpId=0&current={pageno}&status=2"
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


class AriaTender(object):
    def scrape(keyword='', key=''):
        tenders = []
        term = requests.utils.quote(key)
        url = "http://www.ariatender.com/beta/query.php"
        # payload = "subject%5B%5D=%D8%A7%D9%84%DA%A9%D8%AA%D8%B1%D9%88%D9%85%D9%88%D8%AA%D9%88%D8%B1"
        payload = f'subject%5B%5D={term}'
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.text

        soup = BeautifulSoup(result, 'html.parser')
        # print(soup)
        links = soup.findAll('a')
        # print(links)
        # print(links)
        # results = response.json()
        # resinner = results['list']
        # print(resinner)
        links = soup.select('div.Tender-Box-Div-Description-f a')
        print(links)
        i = 1
        for link in links:
            tender = {}
            href = link.get('href')
            tender['href'] = href
            tender['title'] = link.text
            href = f'http://www.ariatender.com{href}'
            # print(f'{i} -  {link.text} | {href}')
            tenders.append(tender)
            i += 1

        print(tenders)
        return tenders
