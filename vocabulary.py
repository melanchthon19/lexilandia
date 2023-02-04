#!/usr/bin/env python3


import os
import re
import pandas as pd
import numpy as np


def preprocess(text):
	text = ''.join([char.lower() for char in text])
	text = re.sub(r',', ' COMA1', text)
	text = re.sub(r';', ' COMA2', text)
	text = re.sub(r':', ' COMA3', text)
	#text = re.sub(r'-', ' COMA4 ', text)
	text = re.sub(r'[¿\?¡!\-\&%$_]', 'PUNT', text)
	#text = ' '.join([word for word in text if word not in stopwords.words('spanish')])
	sentences = re.split('[\.\n(PUNT)]', text)
	sentences = [s.strip() for s in sentences]
	sentences = [s for s in sentences if s]

	return sentences

def read_tale(file):
	with open(file, 'r') as input:
		text = input.read()
	sentences = preprocess(text)

	return sentences

def read_formas(file):
	formas = {}
	with open(file, 'r', encoding='latin-1') as input:
		for line in input:
			line = [term.strip() for term in line.split('\t')]
			try:
				formas[line[1]] = (line[0], line[2], line[3])
			except IndexError:
				pass

	return formas

def read_stopwords(file):
	sw = []
	with open(file, 'r', encoding='latin-1') as input:
		for line in input:
			line = [term.strip() for term in line.split('\t')]
			sw.append(line[1])

	return sw

def compare_vocab(file_f, file_s, file_sw):
	formas = read_formas(file_f)
	sentences = read_tale(file_s)
	sw = read_stopwords(file_sw)
	unks = unknown_vocab(formas, sentences, sw)

	output_results(unks, sentences, formas)

	return unks

def penalize_sw(words, partial, N, sw):
	csw = len([word for word in words if word in sw])
	if csw == N:
		return 100000
	else:
		return partial/(N-csw)

def sentence_score(sentence, formas, sw):
	words = sentence.split()
	N = len(words)
	if remove_sw:
		#N = len([word for word in words if word not in sw])
		partial = sum([float(formas[word][2]) for word in words
					if word in formas.keys() and word not in sw])/N
		score = penalize_sw(words, partial, N, sw)

	else:
		#N = len([word for word in words if word in formas.keys()])
		score = sum([float(formas[word][2]) for word in words
					if word in formas.keys()])/N

	return score

def rank_unk(rank):
	ordered = []
	for k in list(rank.keys()):
		most_unk = min(rank.items(), key=lambda x: x[1])
		ordered.append(most_unk)
		rank.pop(most_unk[0])

	return ordered

def revert(sentence):
	if re.search(r'COMA', sentence):
		sentence = re.sub(r' COMA1', ',', sentence)
		sentence = re.sub(r' COMA2', ';', sentence)
		sentence = re.sub(r' COMA3', ':', sentence)
		sentence = re.sub(r' COMA4', '-', sentence)

	return sentence

def unknown_vocab(formas, sentences, sw):
	rank = {}
	for i, s in enumerate(sentences):
		rank[i] = sentence_score(s, formas, sw)

	most_unk = rank_unk(rank)

	return most_unk

def word_score(word, formas):
	try:
		return float(formas[word][2])
	except KeyError:
		return 0

def highlight(sentence, formas):
	most_unk = (100000, 0)
	bold = []
	for i, word in enumerate(sentence.split()):
		if word in P:
			continue
		score = word_score(word, formas)
		if score == 0:
			bold.append(i)
		else:
			if score < most_unk[0]:
				most_unk = (score, i)

	bold.append(most_unk[1])

	sentence = ' '.join([word.upper() if i in bold else word
						for i, word in enumerate(sentence.split())])

	return sentence

def output_results(unks, sentences, formas):
	for sent_ix, score in unks[:10]:
		bold = highlight(sentences[sent_ix], formas)
		print(sent_ix, score, '\n', revert(bold))


if __name__ == '__main__':
	P = ['COMA1', 'COMA2', 'COMA3']
	folder = 'subterra'
	tale = 'JUAN FARIÑA.txt'
	#tale = 'LOS INVÁLIDOS.txt'
	file_f = '10000_formas.txt'
	file_sw = 'stopwords.txt'
	remove_sw = True
	compare_vocab(file_f, os.path.join(folder, tale), file_sw)
