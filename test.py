from collections import Counter

def term_freq (d):
    with open(d, 'r') as input:
        input = input.read()
        freq = Counter(input.split()).most_common()
    print(freq)
    print("------")
    return freq

term_freq("preproc_d3")