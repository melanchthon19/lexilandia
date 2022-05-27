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

	def text2sentences(self, text, remove_punct=False, remove_sw=False):
		# TODO: add punct and sw flags
		sentences = [s.strip().split() for p in text for s in p.split('.') if s]
		return sentences

	def text2sentences_types(self, text, per_sentence=True, remove_punct=True, remove_sw=True, lower=True):
		sentences = self.text2tokens(text, per_sentence, remove_punct, remove_sw, lower)
		sentences_types = [list(dict.fromkeys(s)) for s in sentences]
		return sentences_types

	def text2tokens(self, text, per_sentence=True, remove_punct=True, remove_sw=True, lower=True):
		sentences = self.text2sentences(text)
		tokens = []
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
