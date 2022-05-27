#!/usr/bin/env python3


import os
import re
import numpy as np
import preprocessing


class FileReader:
	def __init__(self, file):
		self.file = self.read_file(file)
		self.pp = preprocessing.FilePreprocesser()

		self.text = self.pp.file2text(self.file)
		self.paragraphs = False
		self.sentences = False
		self.tokens = False
		self.vocab = False

	def read_file(self, file):
		""" reads the file """
		with open(file, 'r') as f:
			return f.read()

	def get_file(self):
		""" returns the input file as it is """
		return self.file

	def get_text(self):
		""" returns text as a list of paragraphs """
		return self.text

	def get_sentences(self):
		""" returns text as a list of sentences """
		self.sentences = self.pp.text2sentences(self.text)
		return self.sentences

	def get_tokens(self):
		""" returns text as a list of tokens """
		self.tokens = self.pp.text2tokens(self.text)
		return self.tokens

	def get_vocab(self):
		""" returns text as a list of unique vocabulary """
		self.vocab = set(self.pp.text2tokens(self.text))
		return self.vocab

	def describe(self):
		""" returns statistics about the text """
		self.stats = {
			'n_paragraphs': len(self.get_text()),
			'n_sentences': len(self.get_sentences()),
			'n_tokens': len(self.get_tokens()),
			'n_vocab': len(self.get_vocab()),
			'avg_tok_sent': np.round(sum([len(s) for s in self.sentences])/len(self.sentences),0)
		}
		return self.stats

	def get_target_vocab(self):
		""" returns a list of interesting vocabulary """
		pass

if __name__ == '__main__':
	file = 'subterra/CAZA MAYOR.txt'
	fr = FileReader(file)
	t = fr.get_text()
	v = fr.get_vocab()
	s = fr.get_sentences()
	d = fr.describe()
	print(d)
	for se in s:
		print(se)
		print()
