#!/usr/bin/env python3
# coding: utf8
# Author: Michael Staehli

import gzip
import os
import random

from typing import BinaryIO
from lxml import etree

def split_corpus(infile: BinaryIO, targetdir: str, n=1000):
    """

    :param infile:
    :return:
    """
    base_name = os.path.join(targetdir, os.path.basename(infile.name))[:-7]
    #TODO: gz files.
    with open(base_name + '.training', 'w', encoding="utf-8") as train_file, \
            open(base_name + '.development', 'w', encoding="utf-8") as dev_file, \
            open(base_name + '.test', 'w', encoding="utf-8") as test_file:
        train_writer = BufferedWriter(train_file)

        dev, test = sample(iter_sentences(infile), n, n,
                           overflow_func=train_writer.write)

        train_writer.flush()
        BufferedWriter(dev_file).write(*dev).flush()
        BufferedWriter(test_file).write(*test).flush()

def iter_sentences(infile):
    """
    Generate all sentences as strings in an xml file.
    :param infile:
    :return:
    """
    context = etree.iterparse(infile, tag='document')

    for _, document in context:
        content = ""
        for sentence in document.iterfind('.//sentence'):
            content += sentence.text+" "
        #Filter out documents with no sentences.
        if content != "":
            yield content

        # We don't need the document anymore, so clear it and remove it from the
        # parent element to save memory.
        document.clear()
        document.getparent().remove(document)

def sample(iterable, *k, overflow_func=None):
    """
    Returns a list of random samples of :param iterable with size n for all n in :param k,
    applies :param overflow_func to all other items.
    :param iterable:
    :param k:
    :param overflow_func:
    :return:
    """

    reservoir = []

    for t, item in enumerate(iterable):
        if t < sum(k):
            reservoir.append(item)
        else:
            m = random.randint(0,t)
            if m < sum(k):
                item, reservoir[m] = reservoir[m], item
            if overflow_func:
                overflow_func(item)
    reservoir = random.shuffle(reservoir)
    return chunks(reservoir, *k)

def chunks(l, *k):
    """
    Splits a list :param l into chunks of size n for all n in :param k
    :param l:
    :param k:
    :return:
    """
    start = 0
    for size in k:
        yield l[start: start+size]
        start += size

class BufferedWriter():
    """
    Writes lists of strings in chunks.
    """
    def __init__(self, file, buffer_size=10000):
        self.file = file
        self.buffer_size = buffer_size
        self.buffer = []

    def write(self, *strings):
        if len(self.buffer) > self.buffer_size:
            self.flush()
            self.buffer.clear()
        self.buffer.extend(strings)
        return self

    def flush(self):
        self.file.write('\n'.join(self.buffer) + '\n')

def main():
    file = gzip.open("C://Users//Michael//Desktop//PCL2_Übung 04//pcl2_ex4//Korpusdaten//abstracts.xml.gz", mode="rb")
    test = open("C://Users//Michael//Desktop//PCL2_Übung 04//pcl2_ex4//Korpusdaten//abstracts_test.txt", "rb")
    # for item in iter_sentences(test):
    #     print(type(item))
    split_corpus(file, "C://Users//Michael//Desktop//PCL2_Übung 04//pcl2_ex4//Korpusdaten//")

if __name__ == '__main__':
    main()