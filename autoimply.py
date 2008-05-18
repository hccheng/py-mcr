from informat import *
from identifan import *
import pprint
import random
import pprint
import fanimplications

def remove_non_implied(combo, always_also):
    affect_all_combo_parts = True
    special_hands = ["Seven Pairs", 
                     "Seven Shifted Pairs",
                     "Thirteen Orphans", 
                     "Greater Honors and Knitted Tiles", 
                     "Lesser Honors and Knitted Tiles"]
    for h in special_hands:
        if h in combo:
            implied = always_also[h]
            always_also[h] = [f for f in implied if f in combo]
            affect_all_combo_parts = False

    if affect_all_combo_parts:
        for base in combo:
            implied = always_also[base]
            always_also[base] = [f for f in implied if f in combo]

def main():
    all_fans = fanimplications.get_implied_map().keys()

    always_also = {}
    for has_fan in all_fans:
        always_also[has_fan] = [fan for fan in all_fans 
                                if fan != has_fan and fan != "Flower Tiles"]

    c = 0
    for file_name in ['inex.txt', 'extra_inex.txt']:
        f = open(file_name)
        c = c + do_file(f, always_also)

    #always_also['Thirteen Orphans'].append('Single Wait')

    pprint.pprint(always_also)

    has_implications = dict([(key, value) for key, value in always_also.items() if len(value) != 0])
    has_no_implications = [key for key, value in always_also.items() if len(value) == 0]

    has_no_implications.sort()
    pprint.pprint(has_no_implications)
    pprint.pprint(has_implications)
    print "situations:", c
    print sum([len(implied_list) for implied_list in always_also.values()], 0)

def do_file(f, always_also):
    c = 0
    try:
        for line in f:
            if not line.startswith('#'):
                line = line[:-1]
                c = c + 1
                print c, line
                sit = parse_command_line(line)
                options = get_options(sit)
                if len(options) == 0:
                    print "!!! No options for " + line
                for op in options:
                    fans = get_fans(op)
                    remove_non_implied(fans.keys(), always_also)

    finally:
        f.close()
    return c

def find_random():
    #sit = parse_command_line('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')
    tiles = 4* ([s+r for s in 'bcd' for r in '123456789'] + 
                ['W'+w for w in 'eswn'] + 
                ['D'+d for d in 'rgw'])

    hasHand = False
    options = []
    tries = 0
    while len(options) < 1:
        tries = tries + 1
        random.shuffle(tiles)
        hand = tiles[0:14]
        walls = tiles[14:]
        sit_string = " h " + "".join(hand[:-1]) + " w " + hand[-1]
        print tries, sit_string
        sit = parse_command_line(sit_string)
        options = get_options(sit)

    fans = get_fans(options[0])
    pprint.pprint(fans)
    print tries

if __name__ == "__main__":
    main()

