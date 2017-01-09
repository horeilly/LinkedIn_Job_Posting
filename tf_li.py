import json
import sys
import string
import itertools
from collections import Counter

reload(sys)
sys.setdefaultencoding('UTF8')
exclude = string.punctuation + string.digits


def get_desc(job):
    return job["decoratedJobPosting"]["jobPosting"]["description"]["rawText"]


def parse_desc(desc):
    parsed = desc.decode("unicode-escape").encode("ascii", "ignore")

    space_set = ("'s", ":", ".", "/")
    stop = ['', 'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
            'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
            'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
            'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for',
            'from', 'get', 'got ', 'had', 'has', 'have', 'he', 'her', 'hers',
            'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
            'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
            'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
            'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
            'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
            'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
            'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
            've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
            'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
            'you', 'your']

    for entry in space_set:
        parsed = parsed.replace(entry, " ")

    parsed = "".join(ch for ch in parsed if ch not in exclude).lower().split(" ")

    parsed = [entry for entry in parsed if entry not in stop]

    return parsed


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


if __name__ == "__main__":
    FILE = "linkedin_biostatistician_job_data.json"
    with open(FILE, "rb") as f:
        text = f.read()

    data = text.split("\n")

    # data[0] = data[0] + "}"
    # data[-1] = "{" + data[-1]
    # for i in range(1, len(data) - 1):
    #     data[i] = "{" + data[i] + "}"
    #
    new_data = [json.loads(entry) for entry in data[0:179]]

    # document_frequency = list()
    # i = 1
    # for entry in new_data:
    # 	desc = get_desc(entry)
    # 	bag_of_words = parse_desc(desc)
    # 	for word in set(bag_of_words):
    # 		document_frequency.append(word)
    # 	print i
    # 	i += 1

    bags_of_words = [parse_desc(get_desc(entry)) for entry in new_data]

    length = len(bags_of_words)

    print "UNIGRAMS"

    unigrams = itertools.chain(*[list(set(find_ngrams(bag_of_words, 1)))
                                 for bag_of_words in bags_of_words])

    unigrams = Counter(unigrams)

    print "BIGRAMS"

    bigrams = itertools.chain(*[list(set(find_ngrams(bag_of_words, 2)))
                                for bag_of_words in bags_of_words])

    bigrams = Counter(bigrams)

    print "TRIGRAMS"

    trigrams = itertools.chain(*[list(set(find_ngrams(bag_of_words, 3)))
                                 for bag_of_words in bags_of_words])

    trigrams = Counter(trigrams)

    results = list()

    for key, value in unigrams.iteritems():
        results.append((key[0], value / float(length)))

    for key, value in bigrams.iteritems():
        results.append((key[0] + " " + key[1], value / float(length)))

    for key, value in trigrams.iteritems():
        results.append((key[0] + " " + key[1] + " " + key[2], value / float(length)))

    final = sorted(results, key=lambda x: x[1], reverse=True)

    # with open("results.txt", "wb") as f:
    #     for item in final:
    #         f.write(item[0] + ", " + str(item[1]) + "\n")

    print final
