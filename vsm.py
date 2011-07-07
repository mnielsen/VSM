"""vsm.py implements a toy search engine to illustrate
the vector space model for documents.

It asks you to enter a query, and then returns all documents matching
the query, in decreasing order of cosine similarity, according to the
vector space model."""

from collections import defaultdict
import math
import sys

# We use a corpus of four documents.  Each document has an id, and
# these are the keys in the following dict, together with the
# corresponding filename.
document_filenames = {0 : "documents/lotr.txt",
                      1 : "documents/silmarillion.txt",
                      2 : "documents/rainbows_end.txt",
                      3 : "documents/the_hobbit.txt"}

# The size of the corpus
N = len(document_filenames)

# dictionary: all terms (i.e., words) in the document corpus
dictionary = set()

# postings: key: term; value: a dict whose keys are document ids, and
# whose values are the frequency with which the term occurs in the
# document.
#
# Note that it is conventional to call postings[term] the postings
# list for term.
postings = defaultdict(dict)

# document_frequency: key: term;  value: how many docs contain the key
document_frequency = defaultdict(int)

# length: key: document id; value: the Euclidean length of the
# corresponding document vector.
length = defaultdict(float)

# The list of characters (mostly, punctuation) we want to strip out of
# terms in the document.
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

def main():
    initalize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    while True:
        do_search()

def initialize_terms_and_postings():
    """Reads in each document in document_filenames, splits it into a
    list of terms (i.e., tokenizes it), adds new terms to the global
    dictionary, and adds the document to the posting list for each
    term, with value equal to the frequency of the term in the
    document."""
    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id],'r')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term) # value is the
                                                   # frequency of the
                                                   # term in the
                                                   # document

def tokenize(document):
    """Returns a list whose elements are the separate terms in
    document.  Something of a hack, but for the simple documents we're
    using, it's okay."""
    terms = document.lower().split()
    return [term.strip(characters) for term in terms]

def initialize_document_frequencies():
    """For each term in the dictionary, count the number of documents
    it appears in, and store the value in document_frequncy[term]."""
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    """Computes the length for each document."""
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)

def imp(term,id):
    """Returns the importance of term in document id.  If the term
    isn't in the document, then return 0."""
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    """Returns the inverse document frequency of term.  Note that if
    term isn't in the dictionary then it returns 0, by convention."""
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0

def do_search():
    """Asks the user what they would like to search for, and returns a
    list of relevant documents, in decreasing order of cosine
    similarity."""
    query = tokenize(raw_input("Search query >> "))
    # find document ids containing all query terms
    relevant_document_ids = intersection(
            [set(postings[term].keys()) for term in query])
    if not relevant_document_ids:
        print "No documents matched all query terms."
    else:
        scores = sorted([(id,similarity(query,id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        for (id,score) in scores:
            print str(score)+": "+document_filenames[id]

def intersection(sets):
    """Returns the intersection of all sets in the list sets. Requires
    that sets contains at least one element, otherwise it raises an
    error."""
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
    """Returns the cosine similarity between query and document id.
    Note that this is unnormalized by the length of the query vector,
    since this doesn't make any difference to the ordering of
    results."""
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()
