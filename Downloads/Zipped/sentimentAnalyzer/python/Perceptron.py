import sys
import getopt
import os
import math
import operator
from collections import defaultdict
import numpy as np

class Perceptron:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """Perceptron initialization"""
    #in case you found removing stop words helps.
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.vocabulary= defaultdict(int)
    self.length = 47814
    self.weights = [0 for x in range(0,self.length)]
    self.npweights = np.array(self.weights)
    self.weightsavg = [0 for x in range(0,self.length)]
    self.npweightsavg = np.array(self.weightsavg)
    self. wordlist = [0 for x in range(0,self.length)]
    self.npwordlist = np.array(self.wordlist)
    self.bias =0
    self.biasavg=0
    self.result=0
    self.ordereddict = defaultdict(int)
    self.counter=0
    self.c =1


  #############################################################################
  # TODO TODO TODO TODO TODO
  # Implement the Perceptron classifier with
  # the best set of features you found through your experiments with Naive Bayes.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    temp = self.npweightsavg
    tempbiasavg = self.biasavg
    self.npweightsavg = self.npweightsavg/self.c
    self.npweightsavg = self.npweights- self.npweightsavg
    self.biasavg = self.biasavg/self.c
    self.biasavg = self.bias - self.biasavg
    mylist =[0 for x in range(0,self.length)]
    for word in words:
        if self.ordereddict[word] < len(mylist):
            mylist[self.ordereddict[word]]=1
    mylist = np.array(mylist)
    #print "dot product",np.dot(self.npweightsavg,mylist)
    if np.dot(self.npweightsavg,mylist)+self.biasavg>0:
        #self.npweightsavg = temp
        #self.biasavg = tempbiasavg
        return 'pos'
    else:
        #self.npweightsavg = temp
        #self.biasavg = tempbiasavg
        return 'neg'

    # Write code here




  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier
     * in the Perceptron class.
     * Returns nothing
    """
    words = self.filterStopWords(words)
    for word in words:
        if not word in self.ordereddict:
            self.ordereddict[word]=self.counter
            self.counter = self.counter +1

    wordlist = [0 for x in range(0,self.length)]
    npwordlist = np.array(self.wordlist)


    for word in words:
        if self.ordereddict[word] < len(npwordlist):
            npwordlist[self.ordereddict[word]]=1




    if klass=='pos':
        self.result=1
    else:
        self.result=-1

        # I apply a threshold limiting the positive and negative values till length^2 the length we can handle

    if (abs((self.result)*(np.dot(self.npweights,npwordlist) +self.biasavg)))<=(self.length)**2:
        if self.result == 1:
            self.npweights = self.npweights +self.result*(npwordlist)
            self.npweightsavg = self.npweightsavg+ (self.c)*(npwordlist)*(self.result)
        if self.result ==-1:
            self.npweights= self.npweights+(self.result)*(npwordlist)
            self.npweightsavg = self.npweightsavg+(self.c)*(npwordlist)*(self.result)
        self.bias = self.bias +self.result
        self.biasavg = self.biasavg+self.c*self.biasavg










    # Write code here

    pass

  def train(self, split, iterations):
      """
      * TODO
      * iterates through data examples
      * TODO
      * use weight averages instead of final iteration weights
      """
      for i in range(0,iterations):
          for example in split.train:
              words = example.words
              self.addExample(example.klass, words)
              self.c = self.c+1




  # END TODO (Modify code beyond here with caution)
  #############################################################################


  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents))
    return result


  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()


  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = []
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits


  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args):
  pt = Perceptron()

  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)

    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0


    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy


def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy

def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')

  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

if __name__ == "__main__":
    main()
