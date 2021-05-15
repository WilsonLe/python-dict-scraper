import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

def scrape(word):
	url = 'https://dictionary.cambridge.org/search/direct/?datasetsearch=english-vietnamese&q=good+time'
	header = {
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
	}
	response = requests.get(url, headers=header)
	content = response.content
	soup = BeautifulSoup(content, 'html.parser')
	dom = etree.HTML(str(soup))
	text = dom.xpath('//*[@id="page-content"]/div[2]/div[1]/span[1]/div/div[3]/h2')[0].text
	print(text)

def main():
	scrape('good')

main()