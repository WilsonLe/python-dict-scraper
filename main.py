import requests
import re
from pprint import pprint
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
	htmlSoup = BeautifulSoup(content, 'html.parser')
	# this dictionary page top hierarchy is divided into word types (noun, verb, adj, interjection)
	typeDOMs = htmlSoup.find_all("div", {"class": "d pr di english-vietnamese kdic"})
	typeStrings = [*map(lambda dom: str(dom), typeDOMs)]
	typeSoups = [*map(lambda dom: BeautifulSoup(dom, 'html.parser'), typeStrings)]
	
	types = []
	for typeSoup in typeSoups:
		query = typeSoup.find("h2", {"class": "tw-bw dhw dpos-h_hw di-title"}).text
		wordType = typeSoup.find("span", {"class": "pos dpos"}).text
		defBlocks = typeSoup.find_all("div", {"class": "sense-block pr dsense dsense-noh"})
		definitions = []
		for defBlock in defBlocks:
			textBlock = defBlock.text.strip() #3 lines of texts
			texts = textBlock.split('\n') #split into 3 texts
			texts[0] = texts[0][2:].strip() #trip the first
			texts[1] = texts[1].strip() #trip the second
			definitions.append({"en": texts[0], "vn": texts[1]})
		types.append({
			"query": query,
			"wordType": wordType,
			"definitions": definitions
		})
	return types

def translate(word):
	""" translate function with english input
	return data: [
		{
			query: input search
			wordType: noun, adj, verb, interjection
			definitions:[
				{
					en: english definition 1
					vn: vietnamese definition 1
				},...
			]
		},...
	]
	"""
	word = cleanInput(word)
	response = sendRequest(word)
	content = response.text #.text or .content works fine with beautiful soup
	data = extractContent(content)
	return data

def main():
	data = translate('relative')
	for wordType in data:
		pprint(wordType)

main()
