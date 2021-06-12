#!/usr/bin/env python3

import re
from PyPDF2 import PdfFileReader


def text2pgs(text):
    p_text = ''.join([word for page in text for word in page])
    paragraphs = re.split('(?<=[\.A-Z])\n \n|\n \n \n', p_text)
    paragraphs = [re.sub('\n', '', p).strip() for p in paragraphs]
    paragraphs = [p for p in paragraphs if p]

    return paragraphs

def pgs2tales(pgs):
    tales = {'to_drop': []}
    titles = ['LOS INVÁLIDOS', 'CAÑUELA Y PETACA', 'EL CHIFLÓN DEL DIABLO',
              'EL GRISÚ', 'JUAN FARIÑA', 'EL POZO', 'LA MANO PEGADA', 'EL PAGO',
              'CAZA MAYOR', 'EL REGISTRO', 'LA BARRENA', 'ERA ÉL SOLO']
    for p in pgs:
        if p in titles:
            title = p
            tales[title] = []
        else:
            try:
                tales[title].append(p)
            except UnboundLocalError:
                tales['to_drop'].append(p)

    return tales

def hand_cleanning(tales):
    #for tale in tales:
    #    for i, p in enumerate(tales[tale]):
    #        if len(p) < 10:
    #            print(tale, i, p)
    tales['LOS INVÁLIDOS'].pop(25)
    tales.pop('to_drop')

    return tales

def extract_text(file):
    text = []
    with open(file, 'rb') as f:  # pdf has to be read in 'rb' mode
        print('reading pdf')
        pdf = PdfFileReader(f)  # pdf manager
        num_ps = pdf.getNumPages()
        print(f'pdf has {num_ps} pages')
        # traversing pdf pages and getting text
        for i in range(num_ps):
            page = pdf.getPage(i)
            #print(repr(page.extractText()))
            text.extend(page.extractText())

    return text

def extract_tales(file):
    text = extract_text(file)
    pgs = text2pgs(text)
    tales = pgs2tales(pgs)
    tales = hand_cleanning(tales)

    return tales

if __name__ == '__main__':
    file = 'subterra.pdf'
    tales = extract_tales(file)
    for k,v in tales.items():
        print(k)

    for title, text in tales.items():
        with open(f'{title}.txt', 'w') as output:
            for line in text:
                output.write(line)
        quit()
