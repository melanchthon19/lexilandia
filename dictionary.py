#!/usr/bin/env python3


import os
import re
import requests
from bs4 import BeautifulSoup


class DRAE:
	def __init__(self):
		self.drae = 'https://dle.rae.es/'
		self.wordreference = 'https://www.wordreference.com/sinonimos/'
		self.page = False
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
		self.max_meanings = 3

	def search_meaning(self, word):
		self.page = requests.get(self.drae + word, headers=self.headers)
		if self.page.status_code != 200:
			return ['No se pudo acceder a ' + self.drae]
		soup = BeautifulSoup(self.page.content, 'html.parser')
		results = soup.find_all('p', attrs={'class':'j'})
		meanings = [result.text for result in results[:self.max_meanings-1]]
		if len(meanings) == 0:
			return ['Definiciones no encontradas']
		return meanings

	def search_sinonyms(self, word):
		self.page = requests.get(self.wordreference + word)
		if self.page.status_code != 200:
			return ['No se pudo acceder a ' + self.drae]
		soup = BeautifulSoup(self.page.content, 'html.parser')
		results = soup.find_all('div', attrs={'class':'trans clickable'})

		synonyms = []
		antonyms = []
		for r in results:
			li = r.find_all('li')
			for l in li:
				if re.search('[aA]nt[oó]nimo[s]', str(l)):
					antonyms.append(re.sub(r'</*span.*?>|</*li>|[aA]nt[oó]nimo[s]: ', '', str(l)))
				else:
					synonyms.append(re.sub(r'</*li>', '', str(l)))

		if not antonyms:
			antonyms = ['Antónimos no encontrados']
		if not synonyms:
			synonyms = ['Sinónimos no encontrados']

		return {'synonyms': synonyms, 'antonyms': antonyms}
