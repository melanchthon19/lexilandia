#!/usr/bin/env python3


import os
import re
import requests
from bs4 import BeautifulSoup


class DRAE:
	def __init__(self):
		self.drae = 'https://dle.rae.es/'
		self.wordreference = 'https://www.wordreference.com/sinonimos/'
		self.linguee = 'https://www.linguee.es/espanol-ingles/search?source=auto&query='
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
			return ['No se pudo acceder a ' + self.wordreference]
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

	def search_sentences(self, words):
		ts = {}
		for word in words:
			self.page = requests.get(self.linguee + word)
			if self.page.status_code != 200:
				return ['No se pudo acceder a ' + self.linguee]
			soup = BeautifulSoup(self.page.content, 'html.parser')
			results = soup.find_all('td', attrs={'class':'sentence left'})
			results = [r.text for r in results]
			# preprocessing
			sentences = [re.sub(r'\xa0|\r|\[...\]', ' ', r) for r in results]
			sentences =[re.sub(r' +', ' ', s).strip() for s in sentences]
			sentences = [s.split('\n') for s in sentences]
			for i in range(len(sentences)):
				pat = sentences[i][-1]
				sentences[i] = sentences[i][:-1]
				sentences[i][-1] = re.sub(rf'{pat}', '', sentences[i][-1])
			sentences = [''.join(s) for s in sentences]
			sentences = [re.sub(' +', ' ', s).strip() for s in sentences]

			ts[word] = sentences[:3]
		return ts

if __name__ == "__main__":
	d = DRAE()
	ts = d.search_sentences(['llamándola', 'capricho'])
	print(ts)
