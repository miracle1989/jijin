# -*- coding:utf-8 -*-


import requests
from bs4 import BeautifulSoup
from prettytable import *


def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_fund_data(code, start='', end=''):
    record = {'Code': code}
    url = r'http://quotes.money.163.com//fund/jzzs_' + code + '.html'
    params = {'start': start, 'end': end}
    html = get_url(url, params)
    soup = BeautifulSoup(html, 'html.parser')
    records = []
    tab = soup.findAll('tbody')[0]
    for tr in tab.findAll('tr'):
        if tr.findAll('td') and len((tr.findAll('td'))) == 4:
            record['Date'] = str(tr.select('td:nth-of-type(1)')[0].getText().strip())
            record['NetAssetValue'] = str(tr.select('td:nth-of-type(2)')[0].getText().strip())
            record['ChangePercent'] = str(tr.select('td:nth-of-type(4)')[0].getText().strip())
            records.append(record.copy())
    return records


def demo(code, start, end):
    table = PrettyTable()
    table.field_names = ['Code', 'Date', 'NAV', 'Change']
    table.align['Change'] = 'r'
    records = get_fund_data(code, start, end)
    print(len(records))
    for record in records:
        table.add_row([record['Code'], record['Date'], record['NetAssetValue'], record['ChangePercent']])
    return table


if __name__ == "__main__":
    print (demo('161725', '2015-03-02', '2016-03-02'))
