#!/usr/bin/python
import sys
import string
import re

url_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
INPUT_FILE = "datos_original_mitad.txt"
OUTPUT_FILE = "output.txt"
matches = []

def process_match(m):
    matches.append(m.group(0))
    return '{{URL}}'

def stringManipulation(file):
    file = open(file)
    counter = 0
    modifiedWords = []
    for line in file.readlines():
        try:
            counter += 1
            if counter % 500 == 0:
                print str(counter)

            cleanedLine = line.strip()
            
            cleanedLine = url_regex.sub(process_match, cleanedLine)

            words = cleanedLine.split()
            for r, word in enumerate(words):
                if r == 0:
                    modifiedWords = (modifiedWords + ['<s> '])
                word = word.translate(string.maketrans("",""), string.punctuation).lower()
                modifiedWords = modifiedWords + [word + ' ']
            modifiedWords = (modifiedWords + ['</s>'] + ['\n'])
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
    with open(OUTPUT_FILE, 'w') as f:
        for line in modifiedWords:
            f.write(line)
    return OUTPUT_FILE

def readFile(file):
    file = open(file)
    for line in file.readlines():
        line = line.strip()
        print line

readFile(stringManipulation(INPUT_FILE))