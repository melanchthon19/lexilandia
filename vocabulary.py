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
    text = re.sub(r'[¿\?¡!\-&%$_]', 'PUNT', text)
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
    for unk in unks:
        print(unk)
        print(revert(sentences[unk[0]]))

def penalize_sw(words, partial, N, sw):
    csw = len([word for word in words if word in sw])
    if csw == len(words):
        return 100000
    else:
        return partial

def compute_score(sentence, formas, sw):
    words = sentence.split()
    if remove_sw:
        N = len([word for word in words if word not in sw])
        partial = sum([float(formas[word][2])/N for word in words
                    if word in formas.keys() and word not in sw])
        score = penalize_sw(words, partial, N, sw)

    else:
        N = len([word for word in words if word in formas.keys()])
        score = sum([float(formas[word][2])/N for word in words
                    if word in formas.keys()])

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

    return sentence

def unknown_vocab(formas, sentences, sw):
    rank = {}
    for i, s in enumerate(sentences):
        rank[i] = compute_score(s, formas, sw)

    most_unk = rank_unk(rank)

    return most_unk


if __name__ == '__main__':
    folder = 'subterra'
    tale = 'LOS INVÁLIDOS.txt'
    file_f = '10000_formas.txt'
    file_sw = 'stopwords.txt'
    remove_sw = True
    compare_vocab(file_f, os.path.join(folder, tale), file_sw)
