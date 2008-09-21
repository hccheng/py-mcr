from mahjongutil import *
#from xcombinations import xcombinations

def group_7pairs(ts):
    """
    7 pairs (actually 7 shifted pairs)
    >>> group_7pairs(make_tile_list("b1b2b3b4b5b6b7b1b2b3b4b5b6b7"))
    [[('b1', 'b1'), ('b2', 'b2'), ('b3', 'b3'), ('b4', 'b4'), ('b5', 'b5'), ('b6', 'b6'), ('b7', 'b7')]]

    7 pairs with two identical pairs
    >>> group_7pairs(make_tile_list("b1b2b3b4b5b6b6b1b2b3b4b5b6b6"))
    [[('b1', 'b1'), ('b2', 'b2'), ('b3', 'b3'), ('b4', 'b4'), ('b5', 'b5'), ('b6', 'b6'), ('b6', 'b6')]]

    """

    if len(ts) != 14:
        return []
    if all([ts[i] == ts[i+1] for i in xrange(0, len(ts), 2)]):
        return [[(ts[i], ts[i+1]) for i in xrange(0, len(ts), 2)]]
    else:
        return []

def group_thirteen_orphans(ts):
    """
    >>> group_thirteen_orphans(make_tile_list("19b19c19dWeswnDrgwr"))
    [[('c1',), ('d1',), ('b1',), ('c9',), ('d9',), ('b9',), ('Dr', 'Dr'), ('Dg',), ('Dw',), ('We',), ('Ws',), ('Ww',), ('Wn',)]]
    """
    orphans = make_tile_list("19b19c19dWeswnDrgw")
    if (len(ts) == 14 # They are thirteen (and an extra one)
        and all([t in orphans for t in ts]) # All are orphans
        and all([o in ts for o in orphans])): # There is at least one of each
        return [[tuple(ts.count(o)*[o]) for o in orphans]]
    return []


def group_knitted_and_honors(ts):
    if len(ts) != 14 or len(set(ts)) != len(ts): # some tiles are not unique
        return []
    #if any rank is represented more than once 
    if any([sum([t[1] == r for t in ts]) > 1 for r in list("123456789")]):
	return []
    suits = set([t[0] for t in ts if t[0].islower()])
    maybe_knitted = [t for t in ts if t[0] in suits]
    honors = tuple(sort_tiles([t for t in ts if t[0] not in suits]))
    low = ([t for t in maybe_knitted if int(t[1]) % 3 == 1])
    middle = ([t for t in maybe_knitted if int(t[1]) % 3 == 2])
    high = ([t for t in maybe_knitted if int(t[1]) % 3 == 0])
    #if there are more than one suit in any of the low, middle or high groups
    if any([len(set([t[0] for t in part])) >1 for part in [low, middle, high]]):
	return []
    
    return [[tuple(low + middle + high), honors]]

def group_knitted_straight_and_normal(ts):
    """
    knitted straight 
    >>> group_knitted_straight_and_normal(make_tile_list("b1b4b7c2c5c8d3d6d9"))
    [[('b1', 'c2', 'd3', 'b4', 'c5', 'd6', 'b7', 'c8', 'd9')]]
    >>> group_knitted_straight_and_normal(make_tile_list("b1c4b7c2c5c8d3d6d9"))
    []
    >>> group_knitted_straight_and_normal(make_tile_list("b1b7c2c5c8d3d6d9"))
    []
    >>> group_knitted_straight_and_normal(make_tile_list("b1b2b3b4b5b6b7b8b9"))
    []
    >>> group_knitted_straight_and_normal(make_tile_list("b1b4b7d2d5d8c3c6c9WeWe"))
    [[('b1', 'd2', 'c3', 'b4', 'd5', 'c6', 'b7', 'd8', 'c9'), ('We', 'We')]]
    """

    knitted = get_knitted_straight_tiles(ts)
    if not knitted:
        return []
    the_rest = ts[:]
    for t in knitted:
        the_rest.remove(t)
    rest_alternatives = group_normal(the_rest)
    if len(rest_alternatives) == 0:
        return []
    else:
        return [[tuple(knitted)] + rest_alternatives[0]]

def all_triplets_pos_old(ts):
    """
    Really very slow and unecessary
    There should be much better ways. The tiles are ordered, and we know how triples look... 
    >>> all_triplets_pos([])
    []
    >>> all_triplets_pos(['b1', 'b1', 'b1'])
    [(0, 1, 2)]
    >>> all_triplets_pos(['b1', 'b1', 'b1', 'b1'])
    [(1, 2, 3)]
    >>> all_triplets_pos(['b3', 'b4', 'b5'])
    [(0, 1, 2)]
    >>> all_triplets_pos(['b3', 'b4', 'b5', 'b6'])
    [(0, 1, 2), (1, 2, 3)]
    >>> all_triplets_pos(['b3', 'b4', 'b5', 'b5', 'b5'])
    [(0, 1, 4), (2, 3, 4)]
    """
    trips = {}
    for trip_idxs in xcombinations(range(len(ts)), 3):
        trip = [ts[i] for i in trip_idxs]
        if is_triplet(trip):
            trips[tuple(trip)] = trip_idxs
    vals = trips.values()
    # If more than one combination (indexes) made the same tiles, only one remain
    vals.sort()
    return vals

def all_triplets_pos(ts):
    trips = {}
    tc = len(ts)
    for t1 in range(0, tc - 2):
        for t2 in range(t1 + 1, tc - 1):
            if is_start_of_triplets([ts[t1], ts[t2]]):
                for t3 in range(t2 + 1, tc):
                    trip_idxs = (t1, t2, t3)
                    trip = [ts[i] for i in trip_idxs]
                    if is_triplet(trip):
                        trips[tuple(trip)] = trip_idxs
    vals = trips.values()
    vals.sort()
    return vals

def group_normal(ts):
    """
    >>> group_normal([])
    [[]]
    >>> group_normal(['b1', 'b1'])
    [[('b1', 'b1')]]
    >>> group_normal(['b1', 'b1', 'b1'])
    [[('b1', 'b1', 'b1')]]
    >>> group_normal(['b1', 'b1', 'b1', 'b2', 'b2'])
    [[('b1', 'b1', 'b1'), ('b2', 'b2')]]
    >>> group_normal(['b1', 'b1', 'b1', 'b2', 'b3', 'b4', 'b4', 'b4'])
    [[('b1', 'b1', 'b1'), ('b2', 'b3', 'b4'), ('b4', 'b4')], [('b1', 'b1'), ('b1', 'b2', 'b3'), ('b4', 'b4', 'b4')]]
    
    """
    if ts == []:
        return [[]]
    if len(ts) % 3 == 1:
        return []
    types = [t[0] for t in ts]
    if 'F' in types:
        return []
    type_count = [types.count(type) for type in "bcdDW"]
    if 1 in type_count:
        return []
    not_divisable_by_three = [c for c in type_count if c%3 != 0]
    if len(not_divisable_by_three) > 1:
        return []
    if len(not_divisable_by_three) == 1 and not_divisable_by_three[0] % 3 != 2:
        return []
    if is_eye(ts):
        return [[tuple(ts)]]
    if len(ts) == 2:
        return []
    alternatives = set()
    for trip_pos in all_triplets_pos(ts):
        (i, j, k) = trip_pos
        trip = tuple([ts[n] for n in trip_pos])
        left = [t for c, t in enumerate(ts) if c not in trip_pos]
        for rest_alternatives in group_normal(left):
            triples = [trip] + rest_alternatives
            triples.sort() # sort to find doubles
            alternatives.add(tuple(triples))
    #if len(alternatives) == 0:
        #print "no_alt "+str(len(ts)), ts
    return [list(alt) for alt in alternatives]

def group_tiles(tiles):
    """ Groups tiles
    >>> group_tiles(make_tile_list("b1"))
    []

    Eyes
    >>> group_tiles(make_tile_list("b1b1"))
    [[('b1', 'b1')]]

    Not eyes
    >>> group_tiles(make_tile_list("b1b2"))
    []

    Pure triple chow or pure shifted pung
    >>> group_tiles(make_tile_list("b1b2b3b1b2b3b1b2b3"))
    [[('b1', 'b1', 'b1'), ('b2', 'b2', 'b2'), ('b3', 'b3', 'b3')], [('b1', 'b2', 'b3'), ('b1', 'b2', 'b3'), ('b1', 'b2', 'b3')]]
    
    Pure straight, half flush
    >>> group_tiles(make_tile_list("b1b2b3b4b5b6b7b8b9DrDrDrWeWe"))
    [[('Dr', 'Dr', 'Dr'), ('We', 'We'), ('b1', 'b2', 'b3'), ('b4', 'b5', 'b6'), ('b7', 'b8', 'b9')]]
    
    >>> group_tiles(make_tile_list("b1b1b1b2b3b4b4b4DrDrDrWeWeWe"))
    [[('Dr', 'Dr', 'Dr'), ('We', 'We', 'We'), ('b1', 'b1'), ('b1', 'b2', 'b3'), ('b4', 'b4', 'b4')], [('Dr', 'Dr', 'Dr'), ('We', 'We', 'We'), ('b1', 'b1', 'b1'), ('b2', 'b3', 'b4'), ('b4', 'b4')]]

    7 pairs
    >>> group_tiles(make_tile_list("b1b2b4b5b6b7Wwb1b2b4b5b6b7Ww"))
    [[('Ww', 'Ww'), ('b1', 'b1'), ('b2', 'b2'), ('b4', 'b4'), ('b5', 'b5'), ('b6', 'b6'), ('b7', 'b7')]]

    7 pairs, but with flowers
    >>> group_tiles(make_tile_list("b1b2b3b4b5b6b1b2b3b4b5b6F1F1"))
    []

    6 pairs and two non matching tiles
    >>> group_tiles(make_tile_list("b1b2b3b4b5b6b7b1b2b3b4b5b6b8"))
    []

    9 gates
    >>> group_tiles(make_tile_list("b1b1b1b2b3b4b5b6b7b8b9b9b9b5"))
    [[('b1', 'b1', 'b1'), ('b2', 'b3', 'b4'), ('b5', 'b5'), ('b6', 'b7', 'b8'), ('b9', 'b9', 'b9')]]
    >>> group_tiles(['b1', 'b1', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b9', 'b9', 'b5'])
    [[('b1', 'b1', 'b1'), ('b2', 'b3', 'b4'), ('b5', 'b5'), ('b6', 'b7', 'b8'), ('b9', 'b9', 'b9')]]
    
    
    almost 9 gates, but one tile doesn't match
    >>> group_tiles(make_tile_list("b1b1b1b2b3b4b5b6b7b8b9b9b9c5"))
    []
    
    lesser honors with knitted tiles (5 honors), and knitted straight
    >>> group_tiles(make_tile_list("b1b4b7c2c5c8d3d6d9WeWsWwWnDg"))
    [[('b1', 'b4', 'b7', 'c2', 'c5', 'c8', 'd3', 'd6', 'd9'), ('Dg', 'We', 'Ws', 'Ww', 'Wn')]]
    
    lesser honors with knitted tiles (6 honors)
    >>> group_tiles(make_tile_list("b1b4b7c2c5c8d3d6WeWsWwWnDgDw"))
    [[('b1', 'b4', 'b7', 'c2', 'c5', 'c8', 'd3', 'd6'), ('Dg', 'Dw', 'We', 'Ws', 'Ww', 'Wn')]]
    
    greater honors with knitted tiles (all 7 honors)
    >>> group_tiles(make_tile_list("b1b4b7c2c5d3d6WeWsWwWnDgDwDr"))
    [[('b1', 'b4', 'b7', 'c2', 'c5', 'd3', 'd6'), ('Dr', 'Dg', 'Dw', 'We', 'Ws', 'Ww', 'Wn')]]
    
    not greater honors with knitted tiles (two fives of different suits)
    >>> group_tiles(make_tile_list("b1b5b7c2c5d3d6WeWsWwWnDgDwDr"))
    []
    
    not greater honors with knitted tiles (five and four of wrong suits)
    >>> group_tiles(make_tile_list("b1b5b7c2c4d3d6WeWsWwWnDgDwDr"))
    []
    
    knitted straight 
    >>> group_tiles(make_tile_list("b1b4b7c2c5c8d3d6d9"))
    [[('b1', 'c2', 'd3', 'b4', 'c5', 'd6', 'b7', 'c8', 'd9')]]
    

    """
    candidates = []
    ts = list(tiles)
    if (not any(flower in ts for flower in make_tile_list("12345678F"))):
        ts.sort()
        candidates.extend(group_normal(ts))
        candidates.extend(group_7pairs(ts))
        candidates.extend(group_thirteen_orphans(ts))
        candidates.extend(group_knitted_and_honors(ts))
        candidates.extend(group_knitted_straight_and_normal(ts))
    return candidates

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

