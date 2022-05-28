#!/usr/bin/env python3


import os
import re


class Generator:
	def __init__(self, target_sentences, file_name, output_path=''):
		self.target_sentences = target_sentences
		self.output_path = output_path
		self.file_name = self.check_if_exists(file_name)
		self.generate_guia()

	def generate_guia(self):
		with open(self.file_name, 'w') as f:
			for i, ts in enumerate(self.target_sentences):
				sentence = ts[0]
				f.write(f'oración {i+1}:\n{sentence}\n')
				target_vocab = ts[1]
				# {'word1': [['Definición 1', 'Definición 2'],
				#			{'synonyms': [lista de sinónimos],
				#			 'antonyms': [lista de antónimos]}]
				#  'word2'
				#}
				for word, meaning in target_vocab.items():
					f.write(f'palabra: "{word}"\n')
					definiciones = '\n\t-'.join(meaning[0])
					f.write(f'definiciones de "{word}":\n\t-{definiciones}\n')
					synonyms = '\n\t-'.join(meaning[1]['synonyms'])
					antonyms = '\n\t-'.join(meaning[1]['antonyms'])
					f.write(f'sinónimos de "{word}":\n\t-{synonyms}\n')
					f.write(f'antónimos de "{word}":\n\t-{antonyms}\n')
				f.write('\n')

	def check_if_exists(self, file_name):
		if os.path.isfile(os.path.join(self.output_path, file_name)):
			overwrite = input(f'file {file_name} already exists. overwrite? [y/n]')
			if overwrite != 'y':
				raise Exception('file already exists. guia not generated')
		return file_name
