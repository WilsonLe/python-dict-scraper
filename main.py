import requests
import re
from bs4 import BeautifulSoup

def cleanInput(input):
	input = input.strip()
	input = input.replace(' ', '-')
	return input

def sendRequest(word):
	url = f'https://dictionary.cambridge.org/search/direct/?datasetsearch=english-vietnamese&q={word}'
	header = {
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
	}
	response = requests.get(url, headers=header)
	return response

def extractContent(content):
	soup = BeautifulSoup(content, 'html.parser')

	query = soup.find("h2", {"class": "tw-bw dhw dpos-h_hw di-title"}).text
	wordType = soup.find("span", {"class": "pos dpos"}).text

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
		"definitions": definitions
	}

def translate(word):
	""" translate function with english input
	return data: {
		query: input word
		wordType: type of input word (n., v., adj., ...)
		definitions: [
			{
				en: english definition 1
				vn: vietnamese definition 1
			},
			{
				en: english definition 2
				vn: vietnamese definition 2
			},
	}
	"""
	word = cleanInput(word)
	response = sendRequest(word)
	content = response.content
	data = extractContent(content)
	return data

def main():
	data = translate('funny')
	for definition in data["definitions"]:
		print(definition['vn'])

main()