import exceptions

class ParseException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

all_non_flower_tiles_ordered_string = \
        'c1d1b1c2d2b2c3d3b3c4d4b4c5d5b5c6d6b6c7d7b7c8d8b8c9d9b9DrDgDwWeWsWwWn'
all_flower_tiles_ordered_string = 'F1F2F3F4F5F6F7F8'
all_tiles_ordered_string = (all_non_flower_tiles_ordered_string + 
                            all_flower_tiles_ordered_string)

def all_tile_types():
    """
    >>> len(all_tile_types()) == 3*9 + 3 + 4 + 8
    True
    """
    return make_tile_list(all_tiles_ordered_string)

def all_non_flower_tile_types():
    """
    >>> len(all_non_flower_tile_types()) == 3*9 + 3 + 4 
    True
    """
    return make_tile_list(all_non_flower_tiles_ordered_string)

def sort_tiles(ts):
    """
    Sorts honors in the "natural" order
    >>> sort_tiles(['Dw', 'Dr'])
    ['Dr', 'Dw']
    """
    order = all_tiles_ordered_string
    order_dict = dict([(k, v) 
	               for (v, k) 
		       in enumerate([order[i:i+2] for i in range(0, len(order), 2)])])
    l = [(order_dict[t], t) for t in ts]
    l.sort()
    return [t for (r, t) in l]

def is_suited(ts):
    """
    >>> is_suited(['b1', 'b1'])
    True
    >>> is_suited(['b1', 'b2'])
    True
    >>> is_suited(['b1', 'c1'])
    False
    """
    return all([t[0] == ts[0][0] for t in ts])

all_possible_chows = [(s+str(r1), s+str(r1+1), s+str(r1+2)) 
		      for r1 in range(1,8) for s in "bcd"]

all_possible_start_of_chows = [(s+str(r1), s+str(r1+1)) 
		      for r1 in range(1,8) for s in "bcd"]

def is_sorted_chow(ts):
    """
    >>> is_sorted_chow([])
    False
    >>> is_sorted_chow(['b1', 'c2', 'd3'])
    False
    >>> is_sorted_chow(['b1', 'b2', 'b3'])
    True
    >>> is_sorted_chow(['b3', 'b2', 'b1'])
    False
    >>> is_sorted_chow([True])
    False
    """

    global all_possible_chows
    return tuple(ts) in all_possible_chows

def is_start_of_sorted_chow(ts):
    """
    >>> is_start_of_sorted_chow([])
    False
    >>> is_start_of_sorted_chow(['b1', 'c2'])
    False
    >>> is_start_of_sorted_chow(['b1', 'b2'])
    True
    >>> is_start_of_sorted_chow(['b7', 'b8'])
    True
    >>> is_start_of_sorted_chow(['b8', 'b9'])
    False
    >>> is_start_of_sorted_chow(['b3', 'b2'])
    False
    >>> is_start_of_sorted_chow([True])
    False
    """

    global all_possible_start_of_chows
    return tuple(ts) in all_possible_start_of_chows


def old_is_sorted_chow(ts):
    if len(ts) != 3 or not is_suited(ts) or len([t for t in ts if t[0] in "WDF"]) > 0:
	return False
    # All equal if shifted according to index
    return len(set([int(t[1])-i for i, t in enumerate(ts)])) == 1 
    """
    if len(ts) != 3:
        return False
    suit = ts[0][0]
    lrank = int(ts[0][1])
    mrank = int(ts[0][1])
    hrank = int(ts[0][1])
    return ((suit in "bcd") and 
            (ts[1][0] == suit) and (ts[2][0] == suit) and
            (mrank == lrank + 1) and (hrank == lrank +2))
    """

def is_pung(ts):
    """
    >>> is_pung([])
    False
    >>> is_pung(['b1', 'b1'])
    False
    >>> is_pung(['b1', 'b1', 'b1'])
    True
    >>> is_pung(['b1', 'b1', 'b1', 'b1'])
    False
    >>> is_pung(['b1', 'b1', 'c1'])
    False
    """
    return len(ts) == 3 and all([t == ts[0] for t in ts])

def is_triplet(ts):
    return is_pung(ts) or is_sorted_chow(ts)

def is_start_of_triplets(ts):
    return is_eye(ts) or is_start_of_sorted_chow(ts)

def is_kong(ts):
    """
    >>> is_kong([])
    False
    >>> is_kong(['b1', 'b1'])
    False
    >>> is_kong(['b1', 'b1', 'b1'])
    False
    >>> is_kong(['b1', 'b1', 'b1', 'b1'])
    True
    >>> is_kong(['b1', 'b1', 'c1'])
    False
    """
    return len(ts) == 4 and all([t == ts[0] for t in ts])

def is_eye(ts):
    """
    >>> is_eye([])
    False
    >>> is_eye(['b1', 'b1'])
    True
    >>> is_eye(['b1', 'b1', 'b1'])
    False
    >>> is_eye(['b1', 'b1', 'b1', 'b1'])
    False
    >>> is_eye(['b1', 'b1', 'c1'])
    False
    """
    return len(ts) == 2 and ts[0] == ts[1]

def is_terminal(t):
    """
    >>> is_terminal("b2")
    False
    >>> is_terminal("We")
    False
    >>> is_terminal("d1")
    True
    """
    return t in make_tile_list("b19c19d19")

def is_honor(t):
    """
    >>> is_honor("b2")
    False
    >>> is_honor("We")
    True
    >>> is_honor("d1")
    False
    """
    return t in make_tile_list("DrgwWeswn")

def is_knitted_tiles(ts):
    """
    >>> is_knitted_tiles(make_tile_list("d1"))
    True
    >>> is_knitted_tiles(make_tile_list("d1d1"))
    False
    >>> is_knitted_tiles(make_tile_list("d1d4"))
    True
    >>> is_knitted_tiles(make_tile_list("d1c2"))
    True
    >>> is_knitted_tiles(make_tile_list("d1c2b3"))
    True
    >>> is_knitted_tiles(make_tile_list("b1c2d3"))
    True
    """
    suits = set([t[0] for t in ts if t[0].islower()])
    maybe_knitted = list(set([t for t in ts if t[0] in suits]))
    if len(maybe_knitted) != len(ts):
        return False
    # each tile in maybe_knitted is now unique
    maybe_knitted.sort()
    low =    ([t for t in maybe_knitted if t[1] in "147"])
    middle = ([t for t in maybe_knitted if t[1] in "258"])
    high =   ([t for t in maybe_knitted if t[1] in "369"])
    if not is_suited(low) or not is_suited(middle) or not is_suited(high):
	return False
    group_suits = [g[0][0] for g in [low, middle, high] if len(g) > 0]
    if len(group_suits) != len(set(group_suits)): # No suit occurs twice
        return False
    return True
    
def get_knitted_straight_tiles(ts):
    for ks in [make_tile_list("147b258c369d"), 
               make_tile_list("147b258d369c"), 
               make_tile_list("147c258b369d"), 
               make_tile_list("147c258d369b"), 
               make_tile_list("147d258b369c"), 
               make_tile_list("147d258c369b")]:
        if set(ts).issuperset(set(ks)):
            return ks
        
def make_tile_list(s):
    """
    >>> "".join(make_tile_list("b1b2b3b4b5b6b7b8b9DrDrDrWeWe"))
    'b1b2b3b4b5b6b7b8b9DrDrDrWeWe'
    >>> "".join(make_tile_list("b123"))
    'b1b2b3'
    >>> "".join(make_tile_list("b111"))
    'b1b1b1'
    >>> "".join(make_tile_list("F123"))
    'F1F2F3'
    >>> "".join(make_tile_list("F231"))
    'F1F2F3'
    >>> "".join(make_tile_list("b11"))
    'b1b1'
    >>> "".join(make_tile_list("11b"))
    'b1b1'
    >>> "".join(make_tile_list("ewW"))
    'WeWw'
    >>> "".join(make_tile_list("Wsn"))
    'WsWn'
    >>> "".join(make_tile_list("Wsn"))
    'WsWn'
    >>> "".join(make_tile_list("b1b1b1b2b3b4b5b6b7b8b9b9b9b5"))
    'b1b1b1b2b3b4b5b5b6b7b8b9b9b9'
    >>> "".join(make_tile_list("b1b0"))
    Traceback (most recent call last):
    ...
    ParseException: Unexpected character '0' at pos=3
    >>> "".join(make_tile_list("123"))
    Traceback (most recent call last):
    ...
    ParseException: Missing character at pos 3 in string 123
    >>> "".join(make_tile_list("123zb"))
    Traceback (most recent call last):
    ...
    ParseException: Unexpected character 'z' at pos=3
    """
    ts = []
    pre_ranks = []
    type_pos = None
    for i, c in enumerate(s):
        if c in "bcdDWF":
            type_pos = (c, i)
            if len(pre_ranks) > 0:
                ts.extend(make_tiles(type_pos, pre_ranks))
                del pre_ranks[:]
                type_pos = None
        else:
            if type_pos == None:
                pre_ranks.append((c, i))
            else:
                ts.extend(make_tiles(type_pos, [(c, i)]))
    if len(pre_ranks) > 0:
        raise ParseException("Missing character at pos %d in string %s" % (len(s), s))
    return sort_tiles(ts)

def make_tiles(type_pos, ranks_pos):
    """
    >>> "".join(make_tiles(('b', 0), [('1', 1), ('2', 2), ('3', 3)]))
    'b1b2b3'
    """
    accepted_ranks = {
	'b': '123456789',
	'c': '123456789',
	'd': '123456789',
	'D': 'rgw',
	'W': 'eswn',
	'F': '12345678'
    }
    ts = []
    (type, type_pos) = type_pos
    if type not in accepted_ranks.keys():
	raise ParseException("Unexpected character '"+type+"' at pos="+str(type_pos))
    for r, rp in ranks_pos:
        if r in accepted_ranks[type]:
            ts.append(type+r)
        else:
            raise ParseException("Unexpected character '"+r+"' at pos="+str(rp))
    return ts

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

