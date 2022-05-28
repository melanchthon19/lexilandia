#!/usr/bin/env python3


import os
import re
from string import punctuation
from nltk.corpus import stopwords


class FilePreprocesser:
	def __init__(self):
		self.stopwords = stopwords.words('spanish')

	def file2text(self, file):
		raw = [line for line in file.split('\n') if line]
		return raw

	def text2sentences(self, text, remove_punct=False, remove_sw=False, lower=False):
		sentences = [s.strip().split() for p in text for s in p.split('.') if s]

		if remove_punct:
			sentences = [self.remove_punctuation(s[:]) for s in sentences]
		if remove_sw:
			sentences = [self.remove_stopwords(s[:]) for s in sentences]
		if lower:
			sentences = [[tok.lower() for tok in s] for s in sentences]

		return sentences

	def text2sentences_types(self, text, per_sentence=True, remove_punct=True, remove_sw=True, lower=True):
		sentences = self.text2tokens(text, per_sentence, remove_punct, remove_sw, lower)
		sentences_types = [list(dict.fromkeys(s)) for s in sentences]
		return sentences_types

	def text2tokens(self, text, per_sentence=True, remove_punct=True, remove_sw=True, lower=True):
		sentences = self.text2sentences(text)
		tokens = []
		# TODO: use list comprehension
		for s in sentences:
			tokens_s = []
			if remove_punct:
				tokens_s = self.remove_punctuation(s[:])
			if remove_sw:
				tokens_s = self.remove_stopwords(tokens_s[:])
			if lower:
				tokens_s = [tok.lower() for tok in tokens_s[:]]
			tokens.append([tok for tok in tokens_s])

		if not per_sentence:
			tokens = [tok for toks in tokens for tok in toks]
			return tokens
		return tokens

	def remove_punctuation(self, tokens):
		return [re.sub(r'\W+', '', tok) for tok in tokens]

	def remove_stopwords(self, tokens):
		return [tok for tok in tokens if tok not in self.stopwords]

class Formas:
	def __init__(self, formas_file):
		self.formas = self.read_file(formas_file)

	def read_file(self, file):
		formas = {}
		with open(file, 'r', encoding='latin-1') as f:
			lines = f.readlines()
			for line in lines[1:]:  # skipping head
				row = re.split(r'[\t\n]', line)
				row = [r.strip() for r in row if r]
				# [Orden, Forma, Frec.absoluta, Frec.normalizada]
				# ['10000.', 'normalización', '1,182', '7.74']
				formas[row[1]] = int(re.search(r'\d+', row[0]).group(0))
		return formas
