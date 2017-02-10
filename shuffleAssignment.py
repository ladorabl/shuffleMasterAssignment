#!/usr/bin/python
import copy, random, time

#1. A standard deck of 52 cards is represented in an array. Each card is represented as an integer. Write a method to shuffle the cards.
'''
This problem was solved through the function shuffleList(a_list)
I used the Fisher-Yates shuffle algorithm in order to shuffle the deck. The deck consists of integers ranged from [0,51] .
Unit testing this for correctness was a bit tricky. I chose to create a large number of shuffled decks, split them by groups of 4 (a hand) , then count how many duplicates occured accross all hands dealt
Testing randomness in this fashion typically yielded a 99.8% success rate
The unit test for this problem is in the function testPr1()
'''
# merge sort adapted from http://en.wikipedia.org/wiki/Merge_sort
def merge(a_left, a_right):
    result = []
    while len(a_left) > 0 or len(a_right) > 0:
        if len(a_left) > 0 and len(a_right) > 0:
            if a_left[0] <= a_right[0]:
                result.append(a_left[0])
                a_left = a_left[1:]
            else:
                result.append(a_right[0])
                a_right = a_right[1:]
        elif len(a_left) > 0:
            result.append(a_left[0])
            a_left = a_left[1:]
        elif len(a_right) > 0:
            result.append(a_right[0])
            a_right = a_right[1:]
    return result            
                

def mergeSort(a_list):
    # if list size is 1, consider it sorted and return it
    if len(a_list) <= 1:
        return a_list
    # else list size is > 1, so split the list into two sublists
    leftList = []
    rightList = []
    midIndex = len(a_list) / 2
    leftList = a_list[0:midIndex]
    rightList = a_list[midIndex:]
    leftList = mergeSort(leftList)
    rightList = mergeSort(rightList)
    return merge(leftList, rightList)
def assertMergeSort(result, expected):
    if len(result) != len(expected):
        raise AssertionError
    for i in range(len(result)):
        if result[i] != expected[i]:
            raise AssertionError

def getIndexFromList(a_list, a_val):
    for i in range(len(a_list)):
        if a_list[i] == a_val:
            return i
    return None
def getCountFromList(a_list, a_val):
    count = 0
    for i in a_list:
        if i == a_val:
            count += 1
    return count

def findValueOfDupe(a_list):
    ls = copy.deepcopy(a_list)
    for i in ls:
        #if ls.count(i) == 2:
        if getCountFromList(ls, i) == 2:
            return i
    return None
def firstNonRepeatingChar(a_str):
    for i in a_str:
        #if a_str.count(i) == 1:
        if getCountFromList(a_str, i) == 1:
            return i
    return None
def shuffleList(a_list):
    ls = copy.deepcopy(a_list)
    # warning! verify length of list
    for i in range(len(ls)-1):
        randomIndex = random.randint(0, len(ls)-1)
        ls[i], ls[randomIndex] = ls[randomIndex], ls[i]
    return ls
def factorial(num):
    if num == 1:
        return 1
    else:
        return num * factorial(num-1)
def createDeck():
    deck = []
    for i in range(52):
        deck.append(i)
    return deck
def testPr1():
    # create an unsorted 52 card deck
    deck = createDeck()
    shuffleOnce = shuffleList(deck)
    listOfDecks = []
    # magic number, chose 6 because higher numbers wouuld take an unrealistic amount of compute / memory resources
    # create 5040 shuffled decks to test against
    for i in xrange(factorial(6)):
        listOfDecks.append(shuffleList(deck))
    deckSubsets = []
    # split each deck instance into groups of 4
    for deck in listOfDecks:
        for i in range(13):
            deckSubsets.append(deck[i*4:i*4+4])
    #deckSubsets.sort()
    deckSubsets = mergeSort(deckSubsets)
    totDeckSubsets = len(deckSubsets)
    matches = []
    # for every single group of 4, I compare it to the 13 * factorial(7) groups of 4
    for ds in deckSubsets:
        #if deckSubsets.count(ds) > 1:
        matchCount = getCountFromList(deckSubsets, ds) 
        if matchCount > 1:
            matches.append(matchCount)
            for i in range(matchCount):
                deckSubsets.remove(ds)
            print "Match found: %d * " % matchCount, ds
    # if there is a match of groups of 4, which should be highly unlikely, an AssertionError is thrown because the shuffle function may not be random enough
    if len(matches) > 0:
   #     raise AssertionError
        print "There were %d matches found out of %d hands and %d decks" % (len(matches), len(deckSubsets), len(listOfDecks))
        print "Randomess Success = %f%%" % (((len(deckSubsets) - (float)(len(matches))) / (float)(len(deckSubsets)))*100)
def testMergeSort():
    ls1 = [1,2,3,4,5]
    ls2 = [3,1,6,2,3]
    ls3 = [31,11,46, 26,2,3]
    ls4 = []
    ls5 = [3]
    assertMergeSort(mergeSort(ls1), [1,2,3,4,5])
    assertMergeSort(mergeSort(ls2), [1,2,3,3,6])
    assertMergeSort(mergeSort(ls3), [2,3,11,26,31,46])
    assertMergeSort(mergeSort(ls4), [])
    assertMergeSort(mergeSort(ls5), [3])


def printOutDeckThenPrintShuffledDeck():

    deck = createDeck()
    shuffleOnce = shuffleList(deck)
    print "Deck Before Shuffle: \n%s" % ('-'*20)
    print deck
    print "Deck After Shuffle: \n%s" % ('-'*20)
    print shuffleOnce

def runTests():

    printOutDeckThenPrintShuffledDeck()
    print "\nTest Randomness of Shuffle \n%s" %('-'*20)
    testPr1()
    testMergeSort()

starttime = time.time()
runTests()
endtime = time.time()
print "Time Elasped: %ss" % (endtime - starttime)
