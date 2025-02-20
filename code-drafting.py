#!/usr/bin/env python
"""
A program to generate random draft codings from a corpus. It calculates the frequency of each letter in the corpus, and randomly splits 
each letter into 4 approximately equal groups. It then calculates the average frequency of each group, comparing the average
frequency of each group to determine whether the draft would be "balanced."
"""

import string
import random
import collections
from collections import Counter
import argparse

#Returns a random group of n characters from the a list
def get_random_sample(freqs: list, num_sublists: int) -> list:
    random.shuffle(freqs)
    sublist_size = len(freqs) // num_sublists
    sublists = []

    for i in range(num_sublists):
        start = i * sublist_size
        end = start + sublist_size
        sublists.append(freqs[start:end])

    remainders = len(freqs) % sublist_size
    if remainders:
        for i in range(remainders):
            sublists[i].append(freqs[end + i])
    
    return sublists

#Returns the average of items in a list
def get_average(pcts: list) -> int:
    n = len(pcts)
    total = 0
    if not n:
        return 0
    
    for pct in pcts:
        total += pct
    
    return total / n

#Calculates the frequency of each character in the corpus
def get_frequencies(corpus:str):
    #Generate alphabet
    alphabet = frozenset(string.ascii_letters.upper())
    
    #Create counter
    counts = collections.Counter()
    
    #Get the counts of each alphabetical character in the corpus
    for char in corpus:
        if char in alphabet:
            counts[char] += 1
            
    #Calcuate the freq % of each alphabetical character in the corpus, and create a final freqency list
    freqs = []
    [freqs.append([char, count, count / len(corpus)]) for char, count in counts.items()]

    return freqs

#Formats and prints the generated drat coding
def print_draft(lst: list):
    #Header
    print(f"{'Shaft':8} {'Draft':8} Frequency")

    #Draft
    for j in range(len(lst[1])):
        shaft = str(lst[1][j]["shaft"])
        draft = lst[1][j]["chars"]
        freq = lst[1][j]["freq"]
        
        print(f"{shaft:9}{draft:9}{round(freq,5)}")

def main(args: argparse.Namespace):

    #read in corpus
    corpus = ""
    
    with open(args.input,"r") as source: #create a list to contain the text data 
      for line in source:
        corpus += line.strip().upper()
        
    assert source.closed

    #Get character frequencies
    freqs = get_frequencies(corpus) 

    #Get the average frequency of each character in the set as a baseline
    baseline = []
    for freq in freqs:
        baseline.append(freq[-1])
    baseline = get_average(baseline)

    balanced_draft_count = 0
    balanced_drafts = {}

    r = 0
    while r < 100000:
        sublists = get_random_sample(freqs, 4)
        shaft_pcts = []

        #create a shaft counter
        sc = 1
        for sub in sublists:
            pcts = []
            chars = ""
            temp_shaft_list = {} 


            for char,_,pct in sub:
                pcts.append(pct)
                chars += char

            temp_shaft_list["shaft"] = sc
            temp_shaft_list["chars"] = "".join(sorted(chars))
            temp_shaft_list["freq"] = get_average(pcts)

            shaft_pcts.append(temp_shaft_list) #add shaft list to shaft dictionary
            
            sc += 1 #increase shaft counter

            temp = [] #create a list to hold the frequenices of the shaft
            for i in shaft_pcts:
                temp.append(i["freq"])
        
        #Final average for shaft
        shaft_max = max(temp) #calculate max frequency
        shaft_min = min(temp) #calculate min frequency
        delta = shaft_max - shaft_min #calculate the difference

        
        if delta <= 0.001:
            balanced_draft_count += 1
            balanced_drafts.update({balanced_draft_count:shaft_pcts})
        r = r + 1
    if balanced_draft_count > 0:
        print_draft(random.choice(list(balanced_drafts.items())))
    else:
        print("No balanced drafts generated. Run again to get new results.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="The filepath of the input file.")
    main(parser.parse_args())