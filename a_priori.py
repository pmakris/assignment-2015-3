import sys
from collections import defaultdict
import csv
import argparse

#calculate the support for items in the itemsets and return the item which
# it's support satisfies the threshold
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):

        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = count
                if support >= int(minSupport):
                        _itemSet.add(item)
        return _itemSet

#join  set with itself
def joinSet(itemSet, length):

        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

#generate one set items
def getItemSetTransactionList(data_iterator):

    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList

#Run apriori algorithm
def runApriori(data_iter, minSupport):

    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()

    oneCSet = returnItemsWithMinSupport(itemSet,transactionList, minSupport,freqSet)
    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k += 1

    def getSupport(item):

            return freqSet[item]

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])
    return toRetItems

#function to read string csv files
def dataFromFile(fname):

        file_iter = open(fname, 'rU')
        csv_reader = csv.reader(file_iter, delimiter=',')
        for line in csv_reader:
            line = [field.strip().lower() for field in line]
            record = frozenset(line)
            yield record

#function to read numeric csv files
def dataFromNumericFile(fname):

        file_iter = open(fname, 'rU')
        csv_reader = csv.reader(file_iter, delimiter=',')
        for line in csv_reader:
            line = [int(field) for field in line]
            record = frozenset(line)
            yield record

#print results with specific format
def printDict(itemdct):

        sortedItems = sorted(itemdct.items(), key=lambda x: len(x[0]))
        keyLen = 1
        row = []
        for itm in sortedItems:
            if keyLen != len(itm[0]):
                keyLen = len(itm[0])
                print( ';'.join('%s:%s' % entry for entry in row))
                row = []
            row.append(itm)
        if row != []:
            print( ';'.join('%s:%s' % entry for entry in row))

if __name__ == "__main__":

    # python a_priori.py [-n] [-p] [-o OUTPUT] support filename

    parser = argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numeric", help="items are numeric",
                        action="store_true", default=False)
    parser.add_argument("support", help="support threshold")
    parser.add_argument("-p", "--percentage",
                        action="store_true", default=False,
                        help="treat support threshold as percentage value")
    parser.add_argument("filename", help="input filename")
    parser.add_argument("-o", "--output", type=str, help="output file")

    args = parser.parse_args()

    inFile = dataFromFile(args.filename)
    minSupport = args.support
    outFile = args.output
    items = runApriori(inFile, minSupport)
    itemdct = dict(items)

    if inFile == None :
        print('No input filename specified, system will exit\n')
        sys.exit('System will exit')
    if args.numeric:
        inFile = dataFromNumericFile(args.filename)
    # if args.percentage:
    #     not done :-(
    if args.output:
        sys.stdout = open(outFile, 'w')
        printDict(itemdct)
    else:
        printDict(itemdct)