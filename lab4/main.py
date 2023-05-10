import random
import string

from thefuzz import fuzz
import simplexml
import base64


def read_xml(name):
    with open(name) as fin:
        a = simplexml.loads(fin.read())

    texts = list()
    for document in a['dataset']['document']:
        texts.append(base64.b64decode(document['content']).decode(encoding='windows-1251'))
    return texts


def shingle(text, length=6):
    res = list()
    text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    for i in range(len(words) - length):
        res.append(''.join(words[i:i + length]))
    return res


texts = read_xml('news-1.xml')

shingled = [shingle(text) for text in texts]

duplicates = set()
threshold = 60
for i in range(len(shingled) - 1):
    print("Searching for", i)
    go = True
    for j in range(i + 1, len(shingled)):
        if go and i not in duplicates and j not in duplicates:
            matches = set()
            n = min(len(shingled[i]), len(shingled[j]))
            m = min(n, 50)
            comp = random.sample(range(n), m)
            for sh in comp:
                if fuzz.ratio(shingled[i][sh], shingled[j][sh]) > threshold:
                    matches.add((shingled[i][sh], shingled[j][sh]))
                    if len(matches) >= 3:
                        duplicates.add(i)
                        duplicates.add(j)
                        print("Duplicated texts:", texts[i], texts[j], sep='\n')
                        print("by: ", matches)
                        print('\n')
                        go = False
