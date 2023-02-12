"""
Python 3.9 программа считывает одну страницу и сохраняет ее в pdf файле
Название файла config.py

Version: 0.1
Author: Andrej Marinchenko
Date: 2023-02-12
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json, base64

from PyPDF2 import PdfMerger


def send_devtools(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  if response.get('status'):
    raise Exception(response.get('value'))
  return response.get('value')

def get_pdf_from_html(path, chromedriver='./chromedriver', print_options = {}):
  webdriver_options = Options()
  webdriver_options.add_argument('--headless')
  webdriver_options.add_argument('--disable-gpu')
  driver = webdriver.Chrome(chromedriver, options=webdriver_options)

  driver.get(path)

  calculated_print_options = {
    'landscape': False,
    'displayHeaderFooter': False,
    'printBackground': True,
	  'preferCSSPageSize': True,
  }
  calculated_print_options.update(print_options)
  result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
  driver.quit()
  return base64.b64decode(result['data'])


url_list = ['https://github.com/Sindou-dedv', 'https://github.com/kmung']
num = 1
if __name__ == "__main__":
  for url in url_list:
    result = get_pdf_from_html(url, chromedriver=r"C:\Users\root\Downloads\chromedriver_win32\chromedriver")
    with open(f'pdf\\out{num}.pdf', 'ab') as file:
      file.write(result)
    num += 1

  merger = PdfMerger()
  for i in [1, num-1]:
    merger.append(f'pdf\\out{i}.pdf')

  merger.write(f'pdf\\result.pdf')
  merger.close()
