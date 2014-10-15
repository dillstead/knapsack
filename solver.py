#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import fpformat
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
ofile = None

def pickItems3(numItems, capacity, items):
    global ofile
    percent = numItems / 20
    if percent == 0:
        percent = 1
        
    maxValues = [[0 for cIdx in range(0, capacity + 1)] for iIdx in range(0, 2)]
    chosen = [[] for iIdx in range(0, numItems + 1)]
    
    start = time.time()
    aIdx = 1
    adj = -1
    for iIdx in range(1, numItems + 1):
        lastChosen = False
        for cIdx in range(0, capacity + 1):
            includedValue = 0
            includedCapacity = cIdx - items[iIdx - 1].weight
            if includedCapacity >= 0: 
                includedValue = items[iIdx - 1].value + maxValues[aIdx + adj][includedCapacity]
            excludedValue = maxValues[aIdx + adj][cIdx]
            if includedValue > excludedValue:
                maxValues[aIdx][cIdx] = includedValue
                if not lastChosen:
                    # chosen at this capacity
                    chosen[iIdx].append(cIdx)
                    lastChosen = True
            else:
                maxValues[aIdx][cIdx] = excludedValue
                if lastChosen:
                    # not chosen at this capacity
                    chosen[iIdx].append(cIdx)
                    lastChosen = False
        aIdx += adj
        adj = -adj
        if iIdx % percent == 0:
            sys.stdout.write(fpformat.fix(time.time() - start, 3) + " ")
            start = time.time()
    sys.stdout.write("\n")
    
    maxValue = maxValues[aIdx + adj][capacity]

    remainingCapacity = capacity
    taken = [0 for iIdx in range(0, numItems)]
    
    
    for iIdx in range(numItems, 0, -1):
        # find insertion point for remainingCapacity
        cIdx = len(chosen[iIdx]) - 1
        while cIdx >= 0:
            if remainingCapacity >= chosen[iIdx][cIdx]:
                break
            cIdx -= 1
        if cIdx != -1:
            # in list
            lastChosen = (cIdx % 2 == 0) 
            #if remainingCapacity > chosen[iIdx][cIdx]:
            #    lastChosen = not lastChosen
        else:
            # not in list
            lastChosen = False
        if lastChosen:
            taken[iIdx - 1] = 1
            remainingCapacity -= items[iIdx - 1].weight
        else:
            taken[iIdx - 1] = 0
    return maxValue, taken

def pickItems2(numItems, capacity, items):
    global ofile
    percent = numItems / 20
    if percent == 0:
        percent = 1
        
    maxValues = [[0 for cIdx in range(0, capacity + 1)] for iIdx in range(0, 2)]
    eMaxValues = [[] for iIdx in range(0, numItems + 1)]
    eMaxValues[0].append(capacity + 1)
    eMaxValues[0].append(0)
    
    start = time.time()
    aIdx = 1
    adj = -1
    for iIdx in range(1, numItems + 1):
        value = 0
        count = 0
        for cIdx in range(0, capacity + 1):
            includedValue = 0
            includedCapacity = cIdx - items[iIdx - 1].weight
            if includedCapacity >= 0: 
                includedValue = items[iIdx - 1].value + maxValues[aIdx + adj][includedCapacity]
            excludedValue = maxValues[aIdx + adj][cIdx]
            if includedValue > excludedValue:
                maxValues[aIdx][cIdx] = includedValue
            else:
                maxValues[aIdx][cIdx] = excludedValue
            if maxValues[aIdx][cIdx] == value:
                count += 1
            else:
                eMaxValues[iIdx].append(count)
                eMaxValues[iIdx].append(value)
                value = maxValues[aIdx][cIdx]
                count = 1
        eMaxValues[iIdx].append(count)
        eMaxValues[iIdx].append(value)
        aIdx += adj
        adj = -adj
        if iIdx % percent == 0:
            sys.stdout.write(fpformat.fix(time.time() - start, 3) + " ")
            start = time.time()
    sys.stdout.write("\n")
    
    #for ev in eMaxValues:
    #    print(ev)
    
    maxValue = maxValues[aIdx + adj][capacity] 
                
    aIdx = 1
    adj = -1
    remainingCapacity = capacity
    taken = [0 for iIdx in range(0, numItems)]
    decode(eMaxValues[numItems], maxValues[aIdx])
    for iIdx in range(numItems, 0, -1):
        #print(str(iIdx))
        decode(eMaxValues[iIdx - 1], maxValues[aIdx + adj])
        if maxValues[aIdx][remainingCapacity] == maxValues[aIdx + adj][remainingCapacity]:
            taken[iIdx - 1] = 0
        else:
            taken[iIdx - 1] = 1
            remainingCapacity -= items[iIdx - 1].weight
        aIdx += adj
        adj = -adj
        
    return maxValue, taken

def decode(src, dest):
    # num val num val
    offset = 0
    for i in range(0, len(src), 2):
        for j in range(offset, offset + src[i]):
            dest[j] = src[i + 1]
        offset += src[i]
    #print("dest")
    #print(dest)

def pickItems1(numItems, capacity, items):
    percent = numItems / 10
    if percent == 0:
        percent = 1
    maxValue = [[0 for iIdx in range(0, numItems + 1)] for cIdx in range(0, capacity + 1)]
    for iIdx in range(1, numItems + 1):
        for cIdx in range(0, capacity + 1):
            includedValue = 0
            includedCapacity = cIdx - items[iIdx - 1].weight
            if includedCapacity >= 0: 
                includedValue = items[iIdx - 1].value + maxValue[includedCapacity][iIdx - 1]
            excludedValue = maxValue[cIdx][iIdx - 1]
            maxValue[cIdx][iIdx] = max(includedValue, excludedValue)
        #if iIdx % percent == 0:
        #    sys.stdout.write(". ")
    #sys.stdout.write("\n")
            
    taken = [0 for iIdx in range(0, numItems)]
    remainingCapacity = capacity
    for iIdx in range(numItems, 0, -1):
        if maxValue[remainingCapacity][iIdx] == maxValue[remainingCapacity][iIdx - 1]:
            taken[iIdx - 1] = 0
        else:
            taken[iIdx - 1] = 1
            remainingCapacity -= items[iIdx - 1].weight
            
    #for cIdx in range(0, capacity + 1):
    #    for iIdx in range(0, numItems + 1):
    #        sys.stdout.write(str(maxValue[cIdx][iIdx]) + " ")
    #    sys.stdout.write("\n")
    
    return maxValue[capacity][numItems], taken
    
def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global ofile
    ofile = open("knapsack.out", "w")
    ofile.write(input_data)
    ofile.flush()

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
        
    maxValue, taken = pickItems3(item_count, capacity, items)
    # prepare the solution in the specified output format
    output_data = str(maxValue) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    
    ofile.close()
    
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

