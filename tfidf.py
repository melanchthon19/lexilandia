#!/usr/bin/env python3

import json
import math
import operator
import argparse
import numpy as np
import pandas as pd
import vocab
import preprocessing
import plot


class TFIDF():
	def __init__(self, documents, vocab):
		"""
		Term Frequency - Inverse Document Frequency Class
		It takes a set of documents and a vocabulary to compute TF and IDF.
		When initialize, it generates the TFIDF score per each word per each document
		stored in tfidf_documents variable.

		It is also able to process a document query and evaluate document comparisons:
		- matching score
		- cosine similarity
		"""
		self.documents = documents
		self.vocab = vocab
		self.N = len(documents)

		self.tf_documents = {doc: self.compute_tf(documents[doc]) for doc in self.documents}
		# tf_documents is a dictionary to store each word's tf value per document.
		# tf_documents['doc']['word'] = tf_score

		self.idf = self.compute_idf()
		# idf is a dictionary to store each word's idf value.
		# as opposed to tf, idf is a unique value per word across the corpus.
		# idf['word'] = idf_score

		self.tfidf_documents = {doc: self.compute_tfidf(self.tf_documents[doc], self.idf) for doc in self.documents}
		# tfidf is the tf_score multiplied by idf_score per each word per each document
		# tfidf['doc']['word'] = tfidf_score
		#self.print()

		self.documents_vectors = {doc: self.vectorize_tfidf(self.tfidf_documents[doc]) for doc in self.tfidf_documents}
		# in order to achieve cosine similarity, tfidf must be vectors
		# documents_vectors['doc']['vector']

	def frequency(self, term, document):
		"""
		returns the normalized frequency of term t in document d
		"""
		freq = document.count(term)
		freq_normalized = freq / len(document)

		return freq_normalized

	def frequency_N(self, term):
		"""
		returns the number of documents that term t occurs in
		"""
		freq = 0
		for doc in self.documents:
			if term in self.documents[doc]:
				freq += 1

		return freq

	def compute_tf(self, document):
		"""
		function that computes the term frequency for all vocabulary:
		the amount of times that term t occurs in document d
		normalized by the total amount of occurrences in document d
		"""
		tf = {voc: self.frequency(voc, document) for voc in self.vocab}

		return tf

	def compute_idf(self):
		"""
		function that computes the inverse document frequency:
		total amount of documents d divided by
		the number of documents d in which the term t occurs
		"""
		idf = {}
		for voc in self.vocab:
			# added 1 to numerator to avoid negative values
			# added 1 to denominator to avoid division by 0 if term t is not in any document
			df = self.frequency_N(voc)
			idf_score = math.log((self.N + 1) / (df + 1))

			# if term t appears in all documents: log(N/N) --> log(1) --> idf =  0.0
			# smoothing idf score to avoid multiplication by 0
			if idf_score == 0.0:
				idf_score = 0.0000001

			idf[voc] = idf_score

		return idf

	def compute_tfidf(self, tf, idf):
		"""
		function that computes tf-idf score:
		tf is passed as a dictionary with tf values per word in vocabulary for a specific document.
		idf is a dictionary with idf values per word in vocabulary.
		"""
		tfidf_score = {voc: tf[voc] * idf[voc] for voc in self.vocab}

		return tfidf_score

	def query2tfidf(self, query):
		"""
		function that computes tf-idf for query
		input: query preprocessed
		output: tfidf for query
		"""
		tf = self.compute_tf(query)
		idf = self.compute_idf()
		tfidf_query = self.compute_tfidf(tf, idf)

		return tfidf_query

	def matching_score(self, query):
		"""
		function that matches query to all documents
		and assigns a score for each.
		the score is calculated regarding the tfidf value per word in the document
		input: tfidf for each document and query preprocessed
		output: a dictionary with ordered results by their matching score
		"""
		matching_score = {doc: 0 for doc in self.tfidf_documents}

		for term in query:
			for doc in self.tfidf_documents:
				if term in self.tfidf_documents[doc]:
					matching_score[doc] += self.tfidf_documents[doc][term]

		best_k = self.rank_scores(matching_score)

		return best_k

	def rank_scores(self, scores, n=-1):
		"""
		function that ranks (descending order) score results
		input: scores is a dictionary, n is the amount of results to retrieve
		output: ranked scores dictionary with a max lenght of n
		if n == -1, then all results are retrieved
		"""
		if n == -1: n = len(scores)
		ranked_scores = {k: v for k, v in sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:n]}

		return ranked_scores

	def vectorize_tfidf(self, tfidf):
		"""
		function that converts the tfidf dictionary to vector space (numpy array)
		each word's value is stored in its index position
		"""
		vector = np.zeros(len(self.vocab))
		for voc in self.vocab:
			index = self.vocab.index(voc)
			vector[index] = tfidf[voc]

		return vector

	def compute_cosine_similarity_matrix(self):
		"""
		function that computes cosine similarity between all documents.
		returns a dataframe with cosine values.
		"""
		matrix = {doc: self.compute_cosine_similarity(self.documents_vectors[doc]) for doc in self.documents_vectors}

		matrix = pd.DataFrame.from_dict(matrix, orient='index')
		indexes = matrix.index.tolist()
		matrix = matrix.reindex(columns=indexes)

		return matrix

	def compute_cosine_similarity(self, query_vector):
		"""
		function that computes cosine similarity between documents and given query vector.
		returns ranked cosine similarity values stored in a dictionary.
		"""
		cosine_similarities = {doc: self.cosine_similarity(self.documents_vectors[doc], query_vector)
							  for doc in self.documents_vectors}

		ranked_cosine_similarities = self.rank_scores(cosine_similarities)

		return ranked_cosine_similarities

	def cosine_similarity(self, v1, v2):
		"""
		function that computes the cosine similarity between two vectors
		"""
		cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

		return cos_sim

	def print_tfidf(self):
		"""
		function that nicely prints tfidf scores
		"""
		for doc in self.tfidf_documents:
			print(doc)
			for voc in self.tfidf_documents[doc]:
				print('\t',voc, self.tfidf_documents[doc][voc])

	def print_scores(self, scores, n=-1):
		"""
		function that nicely prints scores
		"""
		if n == -1: n = len(scores)
		for i, (k, v) in enumerate(scores.items()):
			print(k, '\t', v)
			if i == n-1:
				break

	def higher_terms(self, n=10):
		ranked_scores = {doc: self.rank_scores(self.tfidf_documents[doc], n) for doc in self.tfidf_documents}

		return ranked_scores


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='...')
	parser.add_argument('-t', '--test', action='store_true', default=False)
	parser.add_argument('-c', '--cosine', action='store_true', default=False)
	parser.add_argument('-m', '--matching', action='store_true', default=False)
	parser.add_argument('-s', '--scores', action='store_true', default=False)
	parser.add_argument('-q', '--query', action='store', default=False)

	args = parser.parse_args()

	if args.test:
		documents = {'1':['hola','cómo','estás'], '2':['hola', 'y','tu', 'yo'], '3':['bien', 'cómo', 'estás']}
		query = 'hola cómo estás? yo'
		print(documents)
		print(query)
	else:
		with open('text_processed.json', 'r') as openfile:  # loading created json file
			book = json.load(openfile)
		documents = book['book_lemmas']
		query = ' '.join(['pedir', 'su', 'desayuno', 'temprano', 'pagar', 'su', 'cuenta', 'y', 'él', 'marchar', 'este', 'ser', 'todo', 'el', 'historia', 'uno', 'momento', 'de', 'silencio', 'y', 'no', 'él', 'ver', 'más', 'preguntar', 'dos', 'o', 'tres', 'voz', 'a', 'uno', 'tiempo', 'nunca', 'más', 'él', 'sentir', 'varios', 'puñetazo', 'sobre', 'el', 'mesa'])

	vocab_info = vocab.generate_vocab(documents)
	# vocab_info = tuple with types, total number of types, and total number of tokens
	vocab = list(vocab_info[0])
	tfidf = TFIDF(documents, vocab)

	if args.query:
		# input: query as a string (i.e. 'this is a query')
		query_preprocessed = preprocessing.preprocess_query(args.query)

		# comparison metrics:
		if args.matching:
			# 1) matching score
			matching_score = tfidf.matching_score(query_preprocessed)
			tfidf.print_scores(matching_score, n=3)

		if args.cosine:
			# 2) cosine similarity
			# it requires query in vector space
			query_tfidf = tfidf.query2tfidf(query_preprocessed)
			query_vector = tfidf.vectorize_tfidf(query_tfidf)
			cosine_similarities = tfidf.compute_cosine_similarity(query_vector)
			tfidf.print_scores(cosine_similarities)

			# plotting cosine similarity between documents
			cosine_similarity_matrix = tfidf.compute_cosine_similarity_matrix()
			plot.plot_heatmap(cosine_similarity_matrix)

	if args.scores:
		terms = tfidf.higher_terms()
		for doc in terms:
			print(doc)
			tfidf.print_scores(terms[doc])
