#!/usr/bin/env python3


import os
import re
import sys
from io import BytesIO
from tqdm import tqdm
import numpy as np
from . import preprocessing
from . import dictionary


class FileReader:
	def __init__(self, text_file, formas_file='laguiadelprofe/lexilandia/10000_formas.txt'):
		self.pp = preprocessing.FilePreprocesser()
		self.formas = preprocessing.Formas(formas_file).formas
		self.drae = dictionary.DRAE()

		if isinstance(text_file, str):
			self.text = self.pp.clean_text(text_file)
			print(self.text)
		else:
			self.file = self.read_file(text_file)
			self.text = self.pp.file2text(self.file)

		self.paragraphs = False
		self.sentences = False
		self.sentences_types = False
		self.tokens = False
		self.vocab = False

	def read_file(self, file):
		""" reads the file """
		try:
			with open(file, 'r') as f:
				return f.read()
		except TypeError:
			# TODO: FIX THIS BOILERPLATE
			f = file.open().read().decode()
			f = re.sub(r"'\\ufeff", '', repr(f))
			f = re.sub(r"\\n|\\\\n", '', f)
			return f

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

	def get_sentences_types(self):
		""" returns text as a list of sentences
		considering types only and stopwords removed """
		self.sentences_types = self.pp.text2sentences_types(self.text)
		return self.sentences_types

	def get_tokens(self):
		""" returns text as a list of tokens """
		self.tokens = self.pp.text2tokens(self.text, per_sentence=False)
		return self.tokens

	def get_vocab(self):
		""" returns text as a list of unique vocabulary """
		self.vocab = set(self.pp.text2tokens(self.text, per_sentence=False))
		return self.vocab

	def describe(self):
		""" returns statistics about the text """
		self.stats = {
			'n_paragraphs': len(self.get_text()),
			'n_sentences': len(self.get_sentences()),
			'n_tokens': len(self.get_tokens()),
			'n_vocab': len(self.get_vocab()),
			'avg_tok_sent': np.round(sum([len(s) for s in self.sentences])/len(self.sentences),0),
			'avg_type_sent': np.round(sum([len(s) for s in self.sentences_types])/len(self.sentences_types),0)
		}
		return self.stats

	def get_target_sentences(self):
		""" returns a list of pairs:
		(original sentences, target meanings).
		target meanings are dictionaries with each
		target vocab and its synonyms and antonyms"""
		sentences = self.pp.text2sentences(self.text)
		target_vocab = self.get_target_vocab()
		target_sa = self.get_target_meanings(target_vocab)
		target_sentences = [(' '.join(sentences[i]), target_sa[i]) for i in range(len(sentences))]
		return target_sentences

	def get_target_meanings(self, target_vocab, from_django=False):
		#lemma_vocab = self.pp.lemmatize(target_vocab)
		target_sa = []
		# django implementation
		if from_django:
			for word in tqdm(target_vocab):
				tm = {word:
					[self.drae.search_meaning(word),
					self.drae.search_synonyms(word)]}
				# if tm[word][0] == ['Definiciones no encontradas']:
				# 	word = self.pp.lemmatize(word)
				# 	tm = {word:
				# 		[self.drae.search_meaning(word),
				# 		self.drae.search_sinonyms(word)]}
				target_sa.append(tm)

			#print(target_vocab, lemma_vocab)
			return target_sa
		else:  # standalone file implementation
			for s in tqdm(lemma_vocab):
				if s:
					target_sa.append({tv[0]:
						[self.drae.search_meaning(tv[0]),
						self.drae.search_sinonyms(tv[0])]
						for tv in s})
				else:
					target_sa.append([])
		return target_sa

	def get_target_vocab(self):
		""" returns a list of interesting vocabulary
		considering most unfrequent tokens according
		to given formas and their rank """
		self.sentences = self.pp.text2sentences(self.text, remove_punct=True, remove_sw=True, lower=True)
		ranked_sentences = [self.rank_sentence(s) for s in self.sentences]
		target_vocab = [self.mark_vocab(s) for s in ranked_sentences]
		return target_vocab

	def mark_vocab(self, sentence, threshold=None):
		""" returns the sentence filtered by threshold.
		by default it consideres words in the sentence
		that were not found in formas
		thus do not have any rank """
		mark_vocab = []
		if threshold:
			for word in sentence:
				try:
					if word[1] >= threshold:
						mark_vocab.append(word)
				except TypeError:
					mark_vocab.append(word)
			return mark_vocab

		return [word for word in sentence if word[1]==threshold]

	def rank_sentence(self, sentence):
		""" returns the sentence as a list of pairs:
		(word, rank) according to given formas and their rank.
		if word is not found in formas,
		then it returns (word, None) """
		rs = []
		for word in sentence:
			try:
				rs.append((word, self.formas[word]))
			except KeyError:
				rs.append((word, None))
		return rs

def main(file):
	Fr = FileReader(file)
	sm = Fr.get_target_sentences()
	print(sm)
	Gn = generator.Generator(sm, 'test.txt')

if __name__ == '__main__':
	#file = 'subterra/CAZA MAYOR3.txt'
	# formas = '10000_formas.txt'
	# fr = FileReader(file, formas)
	# t = fr.get_text()  # keeps punctuation and stopwords
	# v = fr.get_vocab()  # removed punctuation and stopwords
	# tk = fr.get_tokens()  # removed punctuation and stopwords
	# s = fr.get_sentences()  # keeps punctuation and stopwords
	# st = fr.get_sentences_types()  # removed punctuation and stopwords
	# d = fr.describe()
	# print('describe:', d)
	#drae = dictionary.DRAE()
	#sa = drae.search_sinonyms('elevábanse')
	#print(sa['synonyms'])
	#print(sa['antonyms'])

	# tv = fr.get_target_vocab()
	# sm = fr.get_target_sentences()
	# print(sm)
	main(sys.argv[1])
