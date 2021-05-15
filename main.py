import requests
import re
from bs4 import BeautifulSoup

def scrape(word):
	url = f'https://dictionary.cambridge.org/search/direct/?datasetsearch=english-vietnamese&q={word}'
	header = {
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
	}
	response = requests.get(url, headers=header)
	content = response.content
	soup = BeautifulSoup(content, 'html.parser')

	query = soup.find("h2", {"class": "tw-bw dhw dpos-h_hw di-title"}).text
	wordType = soup.find("span", {"class": "pos dpos"}).text
	pronunciation = soup.find("span", {"class": "pron dpron"}).text

	defBlocks = soup.find_all("div", {"class": "sense-block pr dsense dsense-noh"})
	definitions = []
	for defBlock in defBlocks:
		textBlock = defBlock.text.strip() #3 lines of texts
		texts = textBlock.split('\n') #split into 3 texts
		texts[0] = texts[0][2:].strip() #trip the first
		texts[1] = texts[1].strip() #trip the second
		definitions.append({"en": texts[0], "vn": texts[1]})

	return {
		"query": query,
		"wordType": wordType,
		"pronunciation": pronunciation,
		"definitions": definitions
	}

def main():
	data = scrape('nice')
	for definition in data["definitions"]:
		print(definition['vn'])

main()