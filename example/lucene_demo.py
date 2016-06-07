# =========================================================================== #
# Just a simple PyLucene Demo.
#
# Note:
#   - Python v2.x (x >= 3.5) is required
#       (see: http://lucene.apache.org/pylucene/)
#   - ... and Python v3.x seems not to be supported.
#   - Tested with Python 2.7.11 and PyLucene 4.9.0
#   - Extensive input files can be obtained from http://www.gutenberg.org/
#
# This application is ispired by the PyLucene 4.9.0 sample's and several
# blogs and tutorials e.g.:
#   - http://graus.co/blog/pylucene-4-0-in-60-seconds-tutorial/
#   - https://freethreads.wordpress.com/2012/09/17/pylucene-part-i-
#       creating-index/
#
# =========================================================================== #
#
# Author: Hendrik Thorun
#         hendrik.thorun@stud.fh-luebeck.de
# Date:   7 June 2016
#
# =========================================================================== #

# Common imports:
import sys, lucene
from os import path, listdir

from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import RAMDirectory
from datetime import datetime

# Indexer imports:
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# from org.apache.lucene.store import SimpleFSDirectory

# Retriever imports:
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

# ---------------------------- global constants ----------------------------- #

BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
INPUT_DIR = BASE_DIR + "/input/"
INDEX_DIR = BASE_DIR + "/lucene_index/"

NoT = 100000 # Number of Tokens

# --------------------------------------------------------------------------- #

print "------------------------------------------------------"
print "PyLucene Demo started (lucene_demo.py)"
print "Python version: %d.%d.%d" % (sys.version_info.major,
                                      sys.version_info.minor,
                                      sys.version_info.micro)
print 'Lucene version:', lucene.VERSION
print "------------------------------------------------------\n"

# --------------------------------------------------------------------------- #
#                    ___           _                                          #
#                   |_ _|_ __   __| | _____  _____ _ __                       #
#                    | || '_ \ / _` |/ _ \ \/ / _ \ '__|                      #
#                    | || | | | (_| |  __/>  <  __/ |                         #
#                   |___|_| |_|\__,_|\___/_/\_\___|_|                         #
#                                                                             #
# --------------------------------------------------------------------------- #

"""
This method returns a document which afterwards can be added to the IndexWriter.
"""
def create_document(file_name):
    path = INPUT_DIR+file_name # assemble the file descriptor
    file = open(path) # open in read mode
    doc = Document() # create a new document
    # add the title field
    doc.add(StringField("title", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("text", file.read(), Field.Store.YES))
    file.close() # close the file pointer
    return doc

# Initialize lucene and the JVM
lucene.initVM()

# Create a new directory. As a SimpleFSDirectory is rather slow ...
directory = RAMDirectory() # ... we'll use a RAMDirectory!

# Get and configure an IndexWriter
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
analyzer = LimitTokenCountAnalyzer(analyzer, NoT)
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
writer = IndexWriter(directory, config)

print "Number of indexed documents: %d\n" % writer.numDocs()
for input_file in listdir(INPUT_DIR): # iterate over all input files
    print "Current file:", input_file
    if input_file.endswith(".txt"): # consider only .txt files
        doc = create_document(input_file) # call the create_document function
        writer.addDocument(doc) # add the document to the IndexWriter

print "\nNumber of indexed documents: %d" % writer.numDocs()
writer.close()
print "Indexing done!\n"
print "------------------------------------------------------"


# --------------------------------------------------------------------------- #
#                    ____      _        _                                     #
#                   |  _ \ ___| |_ _ __(_) _____   _____ _ __                 #
#                   | |_) / _ \ __| '__| |/ _ \ \ / / _ \ '__|                #
#                   |  _ <  __/ |_| |  | |  __/\ V /  __/ |                   #
#                   |_| \_\___|\__|_|  |_|\___| \_/ \___|_|                   #
#                                                                             #
# --------------------------------------------------------------------------- #

"""
Asks the user for query strings and will show the corresponding result
"""
def search_loop(searcher, analyzer):
    while True:
        print "\nEnter a blank line to quit."
        command = raw_input("Query: ")
        if command == '':
            return

        print
        print "Searching for:", command
        query = QueryParser(Version.LUCENE_CURRENT, "text", analyzer).parse(command)
        start = datetime.now()
        scoreDocs = searcher.search(query, 50).scoreDocs
        duration = datetime.now() - start
        print "%s total matching documents in %s:" % (len(scoreDocs), duration)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print doc.get("title")#, 'name:', doc.get("name")

        print "\n------------------------------------------------------"


# Create a searcher for the above defined RAMDirectory
searcher = IndexSearcher(DirectoryReader.open(directory))

# Create a new retrieving analyzer
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

# ... and start searching!
search_loop(searcher, analyzer)

# ----------------------------------- EOF ----------------------------------- #
