import numpy
from numpy.linalg import norm

'''method cosSim use to calculate cosine Similarity base on formula cos(a) = (vectorA dot vectorB) / [ mag(vectorA) * mag(vectorB) ] '''
'''https://www.learndatasci.com/glossary/cosine-similarity/'''

def cosSim(vecA ,vecB):
    dotOfab= numpy.dot(vecA,vecB)
    normA= norm(vecA)
    normB= norm(vecB)
    return (dotOfab)/(normA * normB)