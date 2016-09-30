import sys
import getopt
import os
import math
import operator
from collections import defaultdict
from sets import Set

class NaiveBayes:
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
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.BOOLEAN_NB = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.FILTER_STOP_WORDS = False
    self.BOOLEAN_NB = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.classSet= Set()
    self.numberOfDocuments = 0
    self.numberOfDocuments_per_class = defaultdict(int);
    self.totalwordperclass = defaultdict(list)
    self.prior_probability = defaultdict(float)
    self.classProbability = defaultdict(float)
    self.max_likelihood_estimate = defaultdict(float)
    self.countProbEachWord= defaultdict(int)
    self.vocabulary =defaultdict(int)
    self.documentCount_boolean = 0
    self.countProbEachWordBooelan=defaultdict(int)
    self.count_per_class_boolean = defaultdict(list)
    self.vocabulary_boolean= defaultdict(int)


  #############################################################################
  # TODO TODO TODO TODO TODO
  # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
  # Boolean (Binarized) features.
  # If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
  # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
  # that relies on feature counts.
  #
  #
  # If any one of the FILTER_STOP_WORDS and BOOLEAN_NB flags is on, the
  # other one is meant to be off.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    if self.FILTER_STOP_WORDS:
      words =  self.filterStopWords(words)



    for s in self.classSet:
        if self.prior_probability[s]==0:
            self.prior_probability[s]=float(self.numberOfDocuments_per_class[s])/float(self.numberOfDocuments)
            self.prior_probability[s]= math.log1p(self.prior_probability[s])

    if not self.BOOLEAN_NB:

        for word in words:
            for s in self.classSet:
                countofthis= float(self.countProbEachWord[(s,word)])+1
                denominator = float(len(self.totalwordperclass[s]))+float(len(self.vocabulary))
                self.max_likelihood_estimate[(word,s)]=math.log1p(countofthis)-math.log1p(denominator)
                self.classProbability[s]= self.max_likelihood_estimate[(word,s)]+self.classProbability[s]

    if self.BOOLEAN_NB:
        for word in words:
            #print "current word",word
            for s in self.classSet:
                countofthis= float(self.countProbEachWordBooelan[(s,word)])+1
                #print "count of this word",countofthis
                denominator = float(len(self.count_per_class_boolean[s]))+float(len(self.vocabulary_boolean))
                self.max_likelihood_estimate[(word,s)]=math.log1p(countofthis)-math.log1p(denominator)
                self.classProbability[s]= self.max_likelihood_estimate[(word,s)]+self.classProbability[s]




    for s in self.classSet:
        self.classProbability[s]= self.classProbability[s]+self.prior_probability[s]
    answer=''
    if self.classProbability['pos']>=self.classProbability['neg']:
        answer= 'pos'
    else:
        answer= 'neg'


    for s in self.classProbability:
        self.classProbability[s]=0

    return answer
    # Write code here



  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier
     * in the NaiveBayes class.
     * Returns nothing
    """

    if self.BOOLEAN_NB:
        self.documentCount_boolean= self.documentCount_boolean+1
    self.classSet.add(klass)
    documentSet = Set()
    self.numberOfDocuments +=1
    self.numberOfDocuments_per_class[klass]+=1
    for word in words:
        if self.BOOLEAN_NB:
            documentSet.add(word)
            continue
        self.countProbEachWord[(klass,word)]+=1
        self.totalwordperclass[klass].append(word)

        self.vocabulary[word]+=1
    if self.BOOLEAN_NB:
        for s in documentSet:
            self.countProbEachWordBooelan[(klass,s)]+=1
            self.count_per_class_boolean[klass].append(word)
            self.vocabulary_boolean[s]+=1
    documentSet.clear()






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

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)


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

def test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB):
  nb = NaiveBayes()
  splits = nb.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    classifier.BOOLEAN_NB = BOOLEAN_NB
    accuracy = 0.0
    for example in split.train:
      words = example.words
      #print "length of training first trainng documents",len(example.words)
      classifier.addExample(example.klass, words)



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


def classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB, trainDir, testDir):
  classifier = NaiveBayes()
  classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
  classifier.BOOLEAN_NB = BOOLEAN_NB
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testSplit = classifier.trainSplit(testDir)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy


def main():
  FILTER_STOP_WORDS = False
  BOOLEAN_NB = False
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if ('-f','') in options:
    FILTER_STOP_WORDS = True
  elif ('-b','') in options:
    BOOLEAN_NB = True

  if len(args) == 2:
    classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB,  args[0], args[1])
  elif len(args) == 1:
    test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB)

if __name__ == "__main__":
    main()
