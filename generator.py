#!/usr/bin/env python3


import os
import re


class Generator:
	def __init__(self, target_sentences, file_name, output_path='', target_meanings=None, from_django=False):
		if from_django:
			"""
			[{'hola': [['1. interj. U. como salutación familiar.', '2. interj. p. us. U. para denotar extrañeza, placentera o desagradable. U. t. repetida.'], {'synonyms': ['Sinónimos no encontrados'], 'antonyms': ['Antónimos no encontrados']}]}, {'como': [['1. m. desus. Burla, chasco. Dar como, o un como.', '1. adv. relat. En el que, en el cual o en que. U. con los antecedentes nominales manera, modo, forma o con los antecedentes adverbiales así, tal e igual. Me encantaba la manera como sonreía. Lo hice tal como me dijiste.'], {'synonyms': ['tal,  tanto,  a modo,  a manera', 'manducar,  tragar,  engullir,  yantar,  devorar,  zampar,  jamar,  masticar,  mascar,  ingerir,  alimentarse,  nutrirse,  llenar de andorga,  echarse al coleto', 'desayunar,  almorzar,  merendar,  cenar', 'gastar,  consumir,  derrochar,  disipar,  dilapidar,  despilfarrar', 'roer,  corroer,  perforar,  erosionar,  desazonar,  concomer'], 'antonyms': ['ayunar,  abstenerse']}]}, {'estasd': [['Definiciones no encontradas'], {'synonyms': ['Sinónimos no encontrados'], 'antonyms': ['Antónimos no encontrados']}]}]
			"""
			tm = target_meanings[0]
			for word, meaning in tm.items():
				f.write(f'palabra: "{word}"\n')
				definiciones = '\n\t-'.join(meaning[0])
				f.write(f'definiciones de "{word}":\n\t-{definiciones}\n')
				synonyms = '\n\t-'.join(meaning[1]['synonyms'])
				antonyms = '\n\t-'.join(meaning[1]['antonyms'])
				f.write(f'sinónimos de "{word}":\n\t-{synonyms}\n')
				f.write(f'antónimos de "{word}":\n\t-{antonyms}\n')
			f.write('\n')
		else:
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
