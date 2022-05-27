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

	def text2sentences(self, text):
		sentences = [s.strip() for p in text for s in p.split('.') if s]
		return sentences

	def text2tokens(self, text, remove_punct=True, remove_sw=True, lower=True):
		sentences = self.text2sentences(text)
		tokens = [tok for s in sentences for tok in s.split()]

		if remove_punct:
			tokens = self.remove_punctuation(tokens)
		if remove_sw:
			tokens = self.remove_stopwords(tokens)
		if lower:
			tokens = [tok.lower() for tok in tokens]

		return tokens

	def remove_punctuation(self, tokens):
		return [re.sub(r'\W+', '', tok) for tok in tokens]

	def remove_stopwords(self, tokens):
		return [tok for tok in tokens if tok not in self.stopwords]
