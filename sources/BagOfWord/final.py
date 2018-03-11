from libBagOfWord import BagOfWord
import collections

if __name__ == "__main__":
    bag = {}
    BagOfWord(bag, "I'm stupids man, I can't talk english")
    BagOfWord(bag, "I learn English for the long time")
    BagOfWord(bag, "He is young men")
    bag = collections.OrderedDict(sorted(bag.items()))
    print (bag)
