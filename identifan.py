from informat import *
from xcombinations import *
from mahjongutil import *

def get_one_option(s, index = 0):
    sit = parse_command_line(s)
    return get_options(sit)[index]

def all_set_indexes(sets):
    return range(len(sets))

def get_only_sets(sets):
    """
    Gets the tile sets out of a structure like this: [('m', X), ('c', X), ('h', X), ('h', X), ('h', X)]
    """
    return [ts for (type, ts) in sets]

def all_represented_types(sets):
    """
    >>> all_represented_types([('c7', 'c8', 'c9'), ('b1', 'b2', 'b3'), ('We', 'We')])
    set(['c', 'b', 'W'])
    """
    types = sum([[t[0] for t in s] for s in sets], [])
    return set(types)

def is_all_tiles_in_group(sets, group):
    tiles = sum([list(s) for s in sets], [])
    return all([t in group for t in tiles])

def is_all_pure_chow(*ss):
    return all([is_sorted_chow(s) and s[0]==ss[0][0] for s in ss])

def is_mixed_double_chow(sa, sb):
    return (is_sorted_chow(sa) and is_sorted_chow(sb) and sa[0] != sb[0] and sa[0][1] == sb[0][1])

def is_short_straight(sa, sb):
    return (sa[0][0] == sb[0][0] and is_sorted_chow(sa) and is_sorted_chow(sb) and abs(int(sb[0][1]) - int(sa[0][1])) == 3)

def is_two_terminal_chows(sa, sb):
    return (is_sorted_chow(sa) and is_sorted_chow(sb) and sa[0][0] == sb[0][0] and
            abs(int(sb[0][1]) - int(sa[0][1])) == 6)

def is_same_rank_pungs(*ss):
    rank = ss[0][0][1]
    if rank not in "123456789":
      # This is to handle that Ww and Dw is not the same rank
      return False
    else:
      return all([(is_pung(s) or is_kong(s)) and (s[0][1] == rank) for s in ss])

def is_all_different_suits(*ss):
    suits = [s[0][0] for s in ss]
    return len(suits) == len(set(suits)) and all([s in "bcd" for s in suits])

def is_only_pungs(*ss):
    return all([is_pung(s) or is_kong(s) for s in ss])

def is_only_kongs(*ss):
    return all([is_kong(s) for s in ss])

def is_only_chows(*ss):
    return all([is_sorted_chow(s) for s in ss])

def is_all_concealed_pungs(*ss):
    return all([type != 'm' and (is_pung(set) or is_kong(set)) for type, set in ss])

def is_two_melded_kongs(sa, sb):
    a_type, a_set = sa
    b_type, b_set = sb
    # Count all kongs as 'at least' melded
    #return a_type == 'm' and b_type == 'm' and is_kong(a_set) and is_kong(b_set)
    return is_kong(a_set) and is_kong(b_set)

def is_only_dragon_pungs(*ss):
    return all([is_pung_of('Drgw', s) for s in ss])

def is_only_wind_pungs(*ss):
    return all([is_pung_of('Weswn', s) for s in ss])

def is_only_dragon_eye_and_dragon_pungs(*ss):
    return (sum([is_eye_of('Drgw', s) for s in ss]) == 1
           and sum([is_pung_of('Drgw', s) for s in ss]) == len(ss) - 1)

def is_only_wind_eye_and_wind_pungs(*ss):
    return (sum([is_eye_of('Weswn', s) for s in ss]) == 1
           and sum([is_pung_of('Weswn', s) for s in ss]) == len(ss) - 1)

def is_mixed_shifted_chows(*ss):
    if not is_only_chows(*ss):
        return False # One (or more) is not a chow
    if not is_all_different_suits(*ss):
        return False # Some were of the same suit
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    return ranks[1] == ranks[0] + 1 and ranks[2] == ranks[0] + 2

def is_mixed_triple_chows(sa, sb, sc):
    if not is_sorted_chow(sa) or not is_sorted_chow(sb) or not is_sorted_chow(sc):
        return False # One (or more) is not a chow
    if sa[0][0] == sb[0][0] or sa[0][0] == sc[0][0] or sb[0][0] == sc[0][0]:
        return False # Some were of the same suit
    ranks = [int(r) for r in [sa[0][1], sb[0][1], sc[0][1]]]
    ranks.sort()
    return ranks[1] == ranks[0] and ranks[2] == ranks[0] 

def is_mixed_straight(*ss):
    if len(ss) != 3 or not is_only_chows(*ss):
        return False # One (or more) is not a chow
    if not is_all_different_suits(*ss):
        return False # Some were of the same suit
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    return ranks == [1, 4, 7]

def is_mixed_shifted_pungs(*ss):
    if not is_only_pungs(*ss):
        return False # One (or more) is not a pung (or kong)
    if not is_all_different_suits(*ss):
        return False # Some were of the same suit
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    return all([r == ranks[0]+i for i, r in enumerate(ranks)])

def is_pure_shifted_chows(*ss):
    if not is_only_chows(*ss):
        return False # One (or more) is not a chow
    suit = list(all_represented_types(ss))
    if len(suit) != 1 or suit[0] not in 'bcd':
        return False # Not suited
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    one_step = all([r == ranks[0] + i for i, r in enumerate(ranks)])
    two_step = all([r == ranks[0] + 2*i for i, r in enumerate(ranks)])
    return one_step or two_step

def is_pure_shifted_pungs(*ss):
    if not is_only_pungs(*ss):
        return False # One (or more) is not a pung (or kong)
    suit = list(all_represented_types(ss))
    if len(suit) != 1 or suit[0] not in 'bcd':
        return False # Not suited
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    return all([r == ranks[0] + i for i, r in enumerate(ranks)])

def is_pure_straight(*ss):
    if len(ss) != 3 or not is_only_chows(*ss):
        return False # One (or more) is not a chow
    if len(all_represented_types(ss)) != 1:
        return False # Not all were of the same suit
    ranks = [int(s[0][1]) for s in ss]
    ranks.sort()
    return ranks == [1, 4, 7]

def find_combinations(seq, n, f):
    """
    Returns a list of the combinations of n indexes (i1, i2, ..., in) in seq that make f(seq[e1], seq[e2], ..., seq[en]) evaluate to True
    >>> find_combinations(list('abc'), 2, lambda x, y: True)
    [[0, 1], [0, 2], [1, 2]]
    """
    return [list(c) for c in xcombinations(range(len(seq)), n) 
                    if f(*tuple([seq[i] for i in c]))]

def is_pung_of(ts, s):
   """
   >>> is_pung_of("WeswnDrgw", ('We', 'We', 'We'))
   True
   """
   tiles = make_tile_list(ts)
   return ( is_pung(s) or is_kong(s) ) and s[0] in tiles

def is_eye_of(ts, s):
   """
   >>> is_eye_of("WeswnDrgw", ('We', 'We'))
   True
   """
   tiles = make_tile_list(ts)
   return is_eye(s) and s[0] in tiles

def is_only_concealed_kongs(*ss):
    return all([type == 'c' and is_kong(set) for type, set in ss])

def find_single_sets(sets, f):
    return [[i] for i, s in enumerate(sets) if f(s)]

# 1 point
def get_pure_double_chow(sit):
    """
    >>> get_pure_double_chow(get_one_option('m b123 m b123 c 9999b h b1156 w b7 f F356 v b777'))
    ('Pure Double Chow', [[0, 1]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_all_pure_chow)
    return ('Pure Double Chow', poss)

def get_mixed_double_chow(sit):
    """
    >>> get_mixed_double_chow(get_one_option('m b123 m c123 c 9999b h b1156 w b7 f F356 v b777'))
    ('Mixed Double Chow', [[0, 1]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_mixed_double_chow)
    return ('Mixed Double Chow', poss)

def get_short_straight(sit):
    """
    >>> get_short_straight( get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Short Straight', [[0, 1]])
    >>> get_short_straight( get_one_option('m b1b2b3 m c4c5c6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Short Straight', [])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_short_straight)
    return ('Short Straight', poss)

def get_two_terminal_chows(sit):
    """
    >>> get_two_terminal_chows( get_one_option('m b1b2b3 m b7b8b9 h b999b11b56 w b7 f F3F5F6') )
    ('Two Terminal Chows', [[0, 1]])
    >>> get_two_terminal_chows( get_one_option('m b1b2b3 m b7b8b9 h b999b567We w We') )
    ('Two Terminal Chows', [[0, 1]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_two_terminal_chows)
    return ('Two Terminal Chows', poss)

def get_pung_of_terminals_or_honors(sit):
    """
    >>> get_pung_of_terminals_or_honors( get_one_option('m Weee m Drrr h b999b11b56 w b7 f F3F5F6 v b7b7b7') )
    ('Pung of Terminals or Honors', [[0], [1], [4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_single_sets(sets, lambda s: is_pung_of("b19c19d19WeswnDrgw", s))
    return ('Pung of Terminals or Honors', poss)

def get_melded_kong(sit):
    """
    >>> get_melded_kong( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Melded Kong', [[1], [2]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_single_sets(sets, lambda s: is_kong(s))
    return ('Melded Kong', poss)
    #sets = sit['sets']
    #return ('Melded Kong', [[i] for (i, (type, ts)) in enumerate(sets) if type == 'm' and is_kong(ts)])

def get_one_voided_suit(sit):
    """
    >>> get_one_voided_suit( get_one_option('m b1b2b3 m b4b4b4b4 c 9999c h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('One Voided Suit', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []
    types = all_represented_types(sets)
    if sum([t in types for t in "bcd"]) == 2:
        poss.append(all_set_indexes(sets))
    return ('One Voided Suit', poss)

def get_no_honors(sit):
    """
    >>> get_no_honors( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('No Honors', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []
    types = all_represented_types(sets)
    if not 'D' in types and not 'W' in types:
        poss.append(all_set_indexes(sets))
    return  ("No Honors", poss)

def get_edge_wait(sit):
    """
    >>> get_edge_wait( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b2b5b5 w b3 f F3F5F6') )
    ('Edge Wait', [[True]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    winning_tile = sit['w']
    waits = sit['waits']
    if len(waits) == 1:
        if winning_tile[1] == '3':
            if any([s[2] == winning_tile
                    for s in sets if is_sorted_chow(s)]):
                poss.append([True])
	elif winning_tile[1] == '7':
            if any([s[0] == winning_tile
                    for s in sets if is_sorted_chow(s)]):
                poss.append([True])
    return ('Edge Wait', poss)

def get_closed_wait(sit):
    """
    >>> get_closed_wait( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b3b8b8 w b2 f F3F5F6') )
    ('Closed Wait', [[True]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    winning_tile = sit['w']
    waits = sit['waits']
    if (len(waits) == 1 and 
        any([s[1] == winning_tile
            for s in sets if is_sorted_chow(s)])):
        poss.append([True])
    return ('Closed Wait', poss)

def get_single_wait(sit):
    """
    >>> get_single_wait( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b2b3b8 w b8 f F3F5F6') )
    ('Single Wait', [[True]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    winning_tile = sit['w']
    waits = sit['waits']
    if (len(waits) == 1 and 
        any([(winning_tile, winning_tile) == s for s in sets])):
        poss.append([True])
    return ('Single Wait', poss)

def get_self_drawn(sit):
    """
    >>> get_self_drawn( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Self-draw', [])
    >>> get_self_drawn( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7 self_draw') )
    ('Self-draw', [[True]])
    """
    poss = []
    if sit['self_draw']:
        poss = [[True]]
    return ('Self-draw', poss)

def get_flower_tiles(sit):
    """
    >>> get_flower_tiles( get_one_option('m b1b2b3 m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Flower Tiles', [['F3'], ['F5'], ['F6']])
    """
    return ("Flower Tiles", [[f] for f in sit["f"]])

# 2 points
def get_dragon_pung(sit):
    """
    >>> get_dragon_pung( get_one_option('m Drrr m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7') )
    ('Dragon Pung', [[0]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_single_sets(sets, is_only_dragon_pungs)
    return ('Dragon Pung', poss)

def get_prevalent_wind(sit):
    """
    >>> get_prevalent_wind( get_one_option('m Weee m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7 rw We') )
    ('Prevalent Wind', [[0]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if sit['rw']:
        poss = find_single_sets(sets, lambda s: is_pung_of(sit['rw'], s))
    return ('Prevalent Wind', poss)

def get_seat_wind(sit):
    """
    >>> get_seat_wind( get_one_option('m Weee m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7 sw We') )
    ('Seat Wind', [[0]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if sit['sw']:
        poss = find_single_sets(sets, lambda s: is_pung_of(sit['sw'], s))
    return ('Seat Wind', poss)

def get_all_chows(sit):
    """
    >>> get_all_chows( get_one_option('m b1b2b3 m b2b3b4 h b3b4b5b6b8b9b9 w b7 f F3F5F6') )
    ('All Chows', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    eyes = sum([is_eye(s) for s in sets])
    chows = sum ([is_sorted_chow(s) for s in sets])
    types = all_represented_types(sets)
    if chows == 4 and eyes == 1 and not 'D' in types and not 'W' in types:
        poss.append(all_set_indexes(sets))
    return ('All Chows', poss)

def get_double_pung(sit):
    """
    >>> get_double_pung( get_one_option('m b1b1b1 m c1c1c1 h b3b4b5b6b8b9b9 w b7 f F3F5F6') )
    ('Double Pung', [[0, 1]])
    >>> get_double_pung( get_one_option('m DwDwDw WwWwWw h c6c7d8d8d9d9d9 w c8 rw Ww sw Ww') )
    ('Double Pung', [])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_same_rank_pungs)
    return ('Double Pung', poss)

def get_two_concealed_pungs(sit):
    """
    >>> get_one_option('h b1b1b1c1c1c1b3b4b5b6b8b9b9 w b7 f F3F5F6')['sets']
    [('h', ('b1', 'b1', 'b1')), ('h', ('b3', 'b4', 'b5')), ('h', ('b6', 'b7', 'b8')), ('h', ('b9', 'b9')), ('h', ('c1', 'c1', 'c1'))]

    >>> get_two_concealed_pungs( get_one_option('h b1b1b1c1c1c1b3b4b5b6b8b9b9 w b7 f F3F5F6') )
    ('Two Concealed Pungs', [[0, 4]])
    """
    sets_with_type = sit['sets']
    poss = find_combinations(sets_with_type, 2, is_all_concealed_pungs)
    return ('Two Concealed Pungs', poss)

def get_concealed_kong(sit):
    """
    >>> get_concealed_kong( get_one_option('m Weee m b4b4b4b4 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7 sw We') )
    ('Concealed Kong', [[2]])
    """
    poss = []
    sets_with_type = sit['sets']
    poss = find_single_sets(sets_with_type, is_only_concealed_kongs)
    return ('Concealed Kong', poss)

def get_all_simples(sit):
    """
    >>> get_all_simples( get_one_option('m b2b3b4 m d4d5d6 c 8888b h b2b2c3c5 w c4 f F3F5F6') )
    ('All Simples', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    not_simple = make_tile_list('b1b9c1c9d1d9WeswnDgrw')
    if all([t not in not_simple for t in tiles]):
        poss.append(all_set_indexes(sets))
    return ('All Simples', poss)

def get_concealed_hand(sit):
    """
    >>> get_concealed_hand( get_one_option('h b1b1b1c1c1c1b3b4b5b6b8b9b9 w b7 f F3F5F6') )
    ('Concealed Hand', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if all(type != 'm' for type, s in sit['sets']):
        poss.append(all_set_indexes(sets))
    return ('Concealed Hand', poss)

def get_tile_hog(sit):
    """
    >>> get_tile_hog( get_one_option('h b1b1b1c1c1c1b1b2b3b6b8b9b9 w b7 f F3F5F6') )
    ('Tile Hog', [['b1']])
    """
    sets = get_only_sets(sit['sets'])
    uses = {}
    for i, s in enumerate(sets):
        for t in s:
            ul = uses.get(t, [])
            ul.append(i)
            uses[t] = ul
    # Can't put the sets in the list, the identical set checks later wouldn't allow two tile hogs then
    #poss = [list(set(ul)) for t, ul in uses.items() if len(ul) == 4 and len(set(ul)) > 1]

    # Just put a list of just one of the tiles, if four are used, but is not in a kong
    poss = [[t] for t, ul in uses.items() if len(ul) == 4 and len(set(ul)) > 1]
    return ('Tile Hog', poss)

# 4 points
def get_two_melded_kongs(sit):
    """
    >>> get_two_melded_kongs( get_one_option('m Weee m b4b4b4b4 m 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7 sw We') )
    ('Two Melded Kongs', [[1, 2]])
    """
    sets_with_type = sit['sets']
    poss = find_combinations(sets_with_type, 2, is_two_melded_kongs)
    return ('Two Melded Kongs', poss)

def get_outside_hand(sit):
    """
    >>> get_outside_hand( get_one_option('m Weee m b1b2b3 m c1c1c1 h d7d8d9b9 w b9 f F3F5F6') )
    ('Outside Hand', [[0, 1, 2, 3, 4]])
    >>> get_outside_hand( get_one_option('m c2c3c4 m b1b2b3 m c1c1c1 h d7d8d9b9 w b9 f F3F5F6') )
    ('Outside Hand', [])
    >>> get_outside_hand( get_one_option('h b789 c9 m DwDwDw DrDrDrDr WsWsWs w c9') )
    ('Outside Hand', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if all([(any([is_terminal(t) or is_honor(t) for t in s]) 
             and len(s) <= 4)
            for s in sets]):
        poss.append(all_set_indexes(sets))
    return ('Outside Hand', poss)

def get_fully_concealed_hand(sit):
    """
    >>> get_fully_concealed_hand( get_one_option('h b1b1b1c1c1c1b3b4b5b6b8b9b9 w b7 f F3F5F6 self_draw') )
    ('Fully Concealed Hand', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if sit['self_draw'] and all(type != 'm' for type, s in sit['sets']):
        poss.append(all_set_indexes(sets))
    return ('Fully Concealed Hand', poss)

def get_last_tile(sit):
    """
    >>> get_last_tile( get_one_option('m Weee m b1b2b3 m c1c1c1 h d7d9b9b9 w d8 f F3F5F6 v d8d8d8') )
    ('Last Tile', [[True]])
    """
    poss = []
    melded = sit['m']
    visible = sit['v']
    tiles = sum([[t for t in s] for s in melded], []) + visible
    if tiles.count(sit['w']) == 3:
        poss.append([True])
    return ('Last Tile', poss)

# 6 points
def get_two_dragon_pungs(sit):
    """
    >>> get_two_dragon_pungs( get_one_option('m Drrr m b1b2b3 m Dggg h d7d9b9b9 w d8 f F3F5F6 v d8d8d8') )
    ('Two Dragon Pungs', [[0, 2]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 2, is_only_dragon_pungs)
    return ('Two Dragon Pungs', poss)

def get_mixed_shifted_chows(sit):
    """
    >>> get_mixed_shifted_chows( get_one_option('m 123b m 234c m Dggg h d3d5b9b9 w d4 f F3F5F6 v d8d8d8') )
    ('Mixed Shifted Chows', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_mixed_shifted_chows)
    return ('Mixed Shifted Chows', poss)

def get_all_pungs(sit):
    """
    >>> get_all_pungs( get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7'))
    ('All Pungs', [])
    >>> get_all_pungs( get_one_option('m b111 m b222 c 9999b h b3334 w b4 f F3F5F6 v b7b7b7'))
    ('All Pungs', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []
    eyes = sum([is_eye(s) for s in sets])
    pungs_and_kongs = sum ([is_pung(s) or is_kong(s) for s in sets])
    if eyes == 1 and pungs_and_kongs == 4:
        poss.append(all_set_indexes(sets))
    return  ("All Pungs", poss)

def get_half_flush(sit):
    """
    >>> get_half_flush(get_one_option('m b1b2b3 m b4b5b6 c Weeee h b1b1b5b6 w b7 f F3F5F6 v b7b7b7'))
    ('Half Flush', [[0, 1, 2, 3, 4]])
    >>> get_half_flush(get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7'))
    ('Half Flush', [])
    """
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    poss = []
    honors = [t for t in tiles if t[0] in "DW"]
    not_honors = [t for t in tiles if t[0] not in "DW"]
    # A hand formed by tiles for any one of the three suits, in combination with Honor tiles
    if len(not_honors) >= 2 and is_suited(not_honors) and len(honors) >= 2:
        poss.append(all_set_indexes(sets))
    return  ("Half Flush", poss)

def get_all_types(sit):
    """
    >>> get_all_types( get_one_option('m 123b m 234c m Dggg h d3d5WeWe w d4 f F3F5F6 v d8d8d8') )
    ('All Types', [[0, 1, 2, 3, 4]])
    >>> get_all_types( get_one_option('m 123b m 234c m 555c h d3d5WeWe w d4 f F3F5F6 v d8d8d8') )
    ('All Types', [])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if len(all_represented_types(sets)) == 5:
        poss.append(all_set_indexes(sets))
    return ('All Types', poss)

def get_melded_hand(sit):
    """
    >>> get_melded_hand( get_one_option('m 123b m 234c m Dggg m d3d4d5 h b9 w b9 f F3F5F6 v d8d8d8') )
    ('Melded Hand', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if len(sit['m']) == 4 and not sit['self_draw']:
        poss.append(all_set_indexes(sets))
    return ('Melded Hand', poss)

# 8 points
def get_mixed_triple_chows(sit):
    """
    >>> get_mixed_triple_chows( get_one_option('m 123b m 123c m Dggg h d1d2b9b9 w d3 f F3F5F6 v d8d8d8') )
    ('Mixed Triple Chows', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_mixed_triple_chows)
    return ('Mixed Triple Chows', poss)

def get_mixed_straight(sit):
    """
    >>> get_mixed_straight( get_one_option('m 123b m 456c m Dggg h d7d8b9b9 w d9 f F3F5F6 v d8d8d8') )
    ('Mixed Straight', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_mixed_straight)
    return ('Mixed Straight', poss)

def get_mixed_shifted_pungs(sit):
    """
    >>> import pprint
    >>> get_mixed_shifted_pungs( get_one_option('m 222b m 333c m Dggg h d4d4b9b9 w d4 f F3F5F6 v d8d8d8') )
    ('Mixed Shifted Pungs', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_mixed_shifted_pungs)
    return ('Mixed Shifted Pungs', poss)

def get_two_concealed_kongs(sit):
    """
    >>> get_two_concealed_kongs( get_one_option('m Weee m b4b4b4b4 c 9999b c b1b1b1b1 h b6 w b6 f F3F5F6 v b7b7b7 sw We') )
    ('Two Concealed Kongs', [[2, 3]])
    """
    sets_with_type = sit['sets']
    poss = find_combinations(sets_with_type, 2, is_only_concealed_kongs)
    return ('Two Concealed Kongs', poss)

def get_last_tile_draw(sit):
    """
    >>> get_last_tile_draw( get_one_option('m Weee m b4b4b4b4 c 9999b c b1b1b1b1 h b6 w b6 f F3F5F6 v b7b7b7 sw We self_draw last_turn') )
    ('Last Tile Draw', [[True]])
    """
    poss = []
    if sit["last_turn"] and sit["self_draw"]:
        poss.append([True])
    return ('Last Tile Draw', poss)

def get_last_tile_claim(sit):
    """
    >>> get_last_tile_claim( get_one_option('m Weee m b4b4b4b4 c 9999b c b1b1b1b1 h b6 w b6 f F3F5F6 v b7b7b7 sw We last_turn') )
    ('Last Tile Claim', [[True]])
    """
    poss = []
    if sit["last_turn"] and not sit["self_draw"]:
        poss.append([True])
    return ('Last Tile Claim', poss)

def get_out_with_replacement_tile(sit):
    """
    >>> get_out_with_replacement_tile( get_one_option('m Weee m b4b4b4b4 c 9999b c b1b1b1b1 h b6 w b6 f F3F5F6 v b7b7b7 sw We kong_replacement') )
    ('Out With Replacement Tile', [[True]])
    """
    poss = []
    if sit["kong_replacement"]:
        poss.append([True])
    return ('Out With Replacement Tile', poss)

def get_robbing_the_kong(sit):
    """
    >>> get_robbing_the_kong( get_one_option('m b1b2b3 b4b5b6 h d2d4b9b9b9b8b8 w d3 robbing') )
    ('Robbing the Kong', [[True]])
    """
    poss = []
    if sit["robbing"]:
        poss.append([True])
    return ('Robbing the Kong', poss)

def get_reversible_tiles(sit):
    """
    >>> get_reversible_tiles( get_one_option('m d1d2d3 m d2d3d4 h d3d4d5b9b9b9Dw w Dw f F3F5F6') )
    ('Reversible Tiles', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    reversible = make_tile_list('1234589d245689bwD')
    if all([t in reversible for t in tiles]):
        poss.append(all_set_indexes(sets))
    return ('Reversible Tiles', poss)

# 12 points
def get_big_three_winds(sit):
    """
    >>> get_big_three_winds( get_one_option('m Weee m Wnnn m c7c8c9 h WsWsd3d3 w Ws f F3F5F6') )
    ('Big Three Winds', [[0, 1, 3]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_only_wind_pungs)
    return ('Big Three Winds', poss)

def get_knitted_straight(sit):
    """
    >> import pprint
    >> pprint.pprint(get_one_option('m Weee h d1d4d7c2c5c8b3b6b9Ws w Ws f F3F5F6'))

    >>> get_knitted_straight( get_one_option('m Weee h d1d4d7c2c5c8b3b6b9Ws w Ws f F3F5F6') )
    ('Knitted Straight', [[1]])
    >>> get_knitted_straight( get_one_option('h 147b258c369d55d55b w 5b') )
    ('Knitted Straight', [[0]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    poss = find_single_sets(sets, get_knitted_straight_tiles)
    return ('Knitted Straight', poss)

def get_upper_four(sit):
    """
    >>> get_upper_four( get_one_option('m 666b m 888c 999b h d6789 w d6 f F3F5F6') )
    ('Upper Four', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    upper_four = [s+r for s in "bcd" for r in "6789"]
    if all([t in upper_four for t in tiles]):
        poss.append(all_set_indexes(sets))
    return ('Upper Four', poss)



def get_lower_four(sit):
    """
    >>> get_lower_four( get_one_option('m 222b m 333c 444b h d1234 w d4 f F3F5F6') )
    ('Lower Four', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    lower_four = [s+r for s in "bcd" for r in "1234"]
    if is_all_tiles_in_group(sets, lower_four):
        poss.append(all_set_indexes(sets))
    return ('Lower Four', poss)

def get_lesser_honors_and_knitted_tiles(sit):
    """
    >> import pprint
    >> pprint.pprint(get_one_option('h b1b4b7c2c5c8d3d6WeWsWwDwDg w Dr f F3F5F6'))
    >>> get_lesser_honors_and_knitted_tiles( get_one_option('h b1b4b7c2c5c8d3d6WeWsWwDwDg w Dr f F3F5F6') )
    ('Lesser Honors and Knitted Tiles', [[0, 1]])
    >>> get_lesser_honors_and_knitted_tiles( get_one_option('h b1b4b7c2c5c8d3d6d9WeWsDwDg w Dr f F3F5F6') )
    ('Lesser Honors and Knitted Tiles', [[0, 1]])
    >>> get_lesser_honors_and_knitted_tiles( get_one_option('h b1b7c2c5c8d3d6WeWsWwWnDwDg w Dr f F3F5F6') ) # greater
    ('Lesser Honors and Knitted Tiles', [])
    """
    poss = []
    sets = sit['sets']
    if len(sets) == 2:
        (type_a, set_a) = sets[0]
        (type_b, set_b) = sets[1]
	if (type_a == 'h' and type_b == 'h' and len(set_b) < 7 and 
	    len(set_a) == len(set(set_a)) and len(set_b) == len(set(set_b))):
		if is_knitted_tiles(set_a) and all([is_honor(t) for t in set_b]):
                    poss.append([0, 1])
    return ('Lesser Honors and Knitted Tiles', poss)

# 16 points
def get_pure_shifted_chows(sit):
    """
    >>> get_pure_shifted_chows( get_one_option('m 123d m 234d m Dggg h d3d5b9b9 w d4 f F3F5F6 v d8d8d8') )
    ('Pure Shifted Chows', [[0, 1, 4]])
    >>> get_pure_shifted_chows( get_one_option('m 123c m 345c m Dggg h c5c7b9b9 w c6 f F3F5F6 v d8d8d8') )
    ('Pure Shifted Chows', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_pure_shifted_chows)
    return ('Pure Shifted Chows', poss)

def get_pure_straight(sit):
    """
    >>> get_pure_straight( get_one_option('m 123d m 456d m 456b h d7d8b9b9 w d9 f F3F5F6 v d8d8d8') )
    ('Pure Straight', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_pure_straight)
    return ('Pure Straight', poss)

def get_three_suited_terminal_chows(sit):
    """
    >>> get_three_suited_terminal_chows( get_one_option('m 123d m 789d m 123b h b7b8b9c5 w c5 f F3F5F6') )
    ('Three Suited Terminal Chows', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    eyes = [s for s in sets if is_eye(s)]
    if len(eyes) == 1 and eyes[0][0][1] == '5': 
        eye = eyes[0]
        chows = [s for s in sets if is_sorted_chow(s) and s[0][0] != eye[0][0]]
        if len(chows) == 4:
            first_chow_suit = chows[0][0][0]
            first_suit_chows = [s for s in chows if s[0][0] == first_chow_suit]
            second_suit_chows = [s for s in chows if s[0][0] != first_chow_suit]
	    if (len(first_suit_chows) == 2 and len(second_suit_chows) == 2 and
                is_two_terminal_chows(*first_suit_chows) and is_two_terminal_chows(*second_suit_chows)):
                poss.append(all_set_indexes(sets))
    return ('Three Suited Terminal Chows', poss)

def get_triple_pung(sit):
    """
    >>> get_triple_pung( get_one_option('m b1b1b1 m c1c1c1c1 h d1d1d1b6b8b9b9 w b7 f F3F5F6') )
    ('Triple Pung', [[0, 1, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_same_rank_pungs)
    return ('Triple Pung', poss)

def get_three_concealed_pungs(sit):
    """
    >>> get_three_concealed_pungs( get_one_option('c b1111 h c1c1c1d1d1d1b6b8b9b9 w b7 f F3F5F6') )
    ('Three Concealed Pungs', [[0, 3, 4]])
    """
    sets_with_type = sit['sets']
    poss = find_combinations(sets_with_type, 3, is_all_concealed_pungs)
    return ('Three Concealed Pungs', poss)

def get_all_fives(sit):
    """
    >>> get_all_fives( get_one_option('h 456d456b456c456c5c w 5c f F3F5F6') )
    ('All Fives', [[0, 1, 2, 3, 4]])
    >>> get_all_fives( get_one_option('h 345c456c555d555b5c w 5c f F3F5F6') )
    ('All Fives', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    the_fives = make_tile_list("5b5c5d")
    if all([any([t in the_fives for t in s]) for s in sets]):
        poss.append(all_set_indexes(sets))
    return ('All Fives', poss)

# 24 points
def get_pure_triple_chow(sit):
    """
    >>> get_pure_triple_chow(get_one_option('m b123 m b123 h b12356c88 w b7 f F356 v'))
    ('Pure Triple Chow', [[0, 1, 2]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_all_pure_chow)
    return ('Pure Triple Chow', poss)

def get_all_even_pungs(sit):
    """
    >>> get_all_even_pungs( get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7'))
    ('All Even Pungs', [])
    >>> get_all_even_pungs( get_one_option('m b444 m b222 c 8888b h 666c6b w b6 f F3F5F6'))
    ('All Even Pungs', [[0, 1, 2, 3, 4]])
    >>> get_all_even_pungs( get_one_option('m b444 m b222 h 888b666c6b w b6 f F3F5F6'))
    ('All Even Pungs', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []
    eyes = sum([is_eye(s) for s in sets])
    even_pungs_and_kongs = sum ([(is_pung(s) or is_kong(s)) and s[0][1] in "2468" for s in sets])
    if len(sets)==5 and eyes == 1 and even_pungs_and_kongs == 4:
        poss.append(all_set_indexes(sets))
    return ('All Even Pungs', poss)

def get_pure_shifted_pungs(sit):
    """
    >>> get_pure_shifted_pungs( get_one_option('m 111b m 222b m Dggg h b3b3b9b9 w b3 f F3F5F6 v d8d8d8') )
    ('Pure Shifted Pungs', [[0, 1, 3]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_pure_shifted_pungs)
    return ('Pure Shifted Pungs', poss)

def get_seven_pairs(sit):
    """
    >>> get_seven_pairs( get_one_option('h c3c3c3c3b2b2b5b5b6b6c8c8b7 w b7 f F3F5F6 v d8d8d8') )
    ('Seven Pairs', [[0, 1, 2, 3, 4, 5, 6]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if len(sets) == 7 and all([is_eye(s) for s in sets]):
        poss.append(all_set_indexes(sets))
    return ('Seven Pairs', poss)

def get_full_flush(sit):
    """
    >>> import pprint
    >>> pprint.pprint(get_full_flush(get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    ('Full Flush', [[0, 1, 2, 3, 4]])
    >>> pprint.pprint(get_full_flush(get_one_option('m b1b2b3 m b4b5b6 c Weeee h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    ('Full Flush', [])
    """
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    poss = []
    if is_suited(tiles):
        poss.append(all_set_indexes(sets))
    return ("Full Flush", poss)

def get_upper_tiles(sit):
    """
    >>> get_upper_tiles( get_one_option('m 777b m 888c 999b h d7899 w d9 f F3F5F6') )
    ('Upper Tiles', [[0, 1, 2, 3, 4]])
    >>> get_upper_tiles( get_one_option('m 789b m 789c 789d h d789d9 w d9') )
    ('Upper Tiles', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    upper_tiles = [s+r for s in "bcd" for r in "789"]
    if is_all_tiles_in_group(sets, upper_tiles):
        poss.append(all_set_indexes(sets))
    return ('Upper Tiles', poss)

def get_middle_tiles(sit):
    """
    >>> get_middle_tiles( get_one_option('m 444b m 555c 666b h d4566 w d6 f F3F5F6') )
    ('Middle Tiles', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    middle_tiles = [s+r for s in "bcd" for r in "456"]
    if is_all_tiles_in_group(sets, middle_tiles):
        poss.append(all_set_indexes(sets))
    return ('Middle Tiles', poss)

def get_lower_tiles(sit):
    """
    >>> get_lower_tiles( get_one_option('m 111b m 222c 333b h d1233 w d3 f F3F5F6') )
    ('Lower Tiles', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    lower_tiles = [s+r for s in "bcd" for r in "123"]
    if is_all_tiles_in_group(sets, lower_tiles):
        poss.append(all_set_indexes(sets))
    return ('Lower Tiles', poss)

def get_greater_honors_and_knitted_tiles(sit):
    """
    >>> get_greater_honors_and_knitted_tiles( get_one_option('h b1b7c2c5c8d3d6WeWsWwWnDwDg w Dr f F3F5F6') )  
    ('Greater Honors and Knitted Tiles', [[0, 1]])
    >>> get_greater_honors_and_knitted_tiles( get_one_option('h b1b4b7c2c5c8d3d6WeWsWwDwDg w Dr f F3F5F6') ) #lesser
    ('Greater Honors and Knitted Tiles', [])
    """
    poss = []
    sets = sit['sets']
    if len(sets) == 2:
        (type_a, set_a) = sets[0]
        (type_b, set_b) = sets[1]
	if (type_a == 'h' and type_b == 'h' and len(set_b) == 7 and 
	    len(set_a) == len(set(set_a)) and len(set_b) == len(set(set_b))):
		if is_knitted_tiles(set_a) and all([is_honor(t) for t in set_b]):
                    poss.append([0, 1])
    return ('Greater Honors and Knitted Tiles', poss)

# 32 points
def get_four_pure_shifted_chows(sit):
    """
    >>> get_four_pure_shifted_chows( get_one_option('h 1c2c3c2c3c4c3c4c5c4c5c6c1c w 1c f F3F5F6') )
    ('Four Pure Shifted Chows', [[1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_pure_shifted_chows)
    return ('Four Pure Shifted Chows', poss)

def get_all_terminals_and_honors(sit):
    """
    >>> get_all_terminals_and_honors( get_one_option('h WeWeWec1c1c1d9d9d9b9b9b9Dr w Dr f F3F5F6') )
    ('All Terminals and Honors', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    terminals = make_tile_list('b1b9c1c9d1d9')
    honors = make_tile_list('WeswnDgrw')
    terminal_count = sum([t in terminals for t in tiles])
    honor_count = sum([t in honors for t in tiles])
    if (terminal_count > 0 and honor_count > 0 
       and terminal_count + honor_count == len(tiles)):
        poss.append(all_set_indexes(sets))
    return ('All Terminals and Honors', poss)

def get_three_kongs(sit):
    """
    >>> get_three_kongs( get_one_option('m 2222c m 3333c m 4444c h b2b2c5c5 w c5 f F3F5F6') )
    ('Three Kongs', [[0, 1, 2]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_only_kongs)
    return ('Three Kongs', poss)


# 48 points
def get_quadruple_chow(sit):
    """
    >>> get_quadruple_chow( get_one_option('h c1c2c3c1c2c3c1c2c3c1c2c3c4 w c4 f F3F5F6', 2) )
    ('Quadruple Chow', [[0, 1, 2, 3]])
    >>> get_quadruple_chow( get_one_option('m c1c2c3 c1c2c3 h c1c2c3c2c3b8b8 w c1') )
    ('Quadruple Chow', [[0, 1, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_all_pure_chow)
    return ('Quadruple Chow', poss)

def get_four_pure_shifted_pungs(sit):
    """
    >>> get_four_pure_shifted_pungs( get_one_option('h 111d222d333d444d1b w b1 f F3F5F6') )
    ('Four Pure Shifted Pungs', [[1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_pure_shifted_pungs)
    return ('Four Pure Shifted Pungs', poss)


# 64 points
def get_little_four_winds(sit):
    """
    >>> get_little_four_winds( get_one_option('h WeeeWwwwWnnnWssb1b2 w b3 f F3F5F6') )
    ('Little Four Winds', [[0, 1, 2, 3]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_only_wind_eye_and_wind_pungs)
    return ('Little Four Winds', poss)

def get_little_three_dragons(sit):
    """
    >>> get_little_three_dragons( get_one_option('h DrrrDgggDwwd9d9d9d1d1 w d1 f F3F5F6') )
    ('Little Three Dragons', [[0, 1, 2]])
    >>> get_little_three_dragons( get_one_option('m Drrr h DgggDwwd9d9d9d1d1 w d1 f F3F5F6') )
    ('Little Three Dragons', [[0, 1, 2]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_only_dragon_eye_and_dragon_pungs)
    return ('Little Three Dragons', poss)

def get_all_honors(sit):
    """
    >>> get_all_honors( get_one_option('h DrrrDwwwWeeeWssWnn w Ws f F3F5F6') )
    ('All Honors', [[0, 1, 2, 3, 4]])
    >>> get_all_honors( get_one_option('m Drrr Dwww Weee Wsss h Wn w Wn') )
    ('All Honors', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    honors = make_tile_list('WeswnDgrw')
    if all([t in honors for t in tiles]):
        poss.append(all_set_indexes(sets))
    return ('All Honors', poss)

def get_pure_terminal_chows(sit):
    """
    >>> get_pure_terminal_chows( get_one_option('m 123b h 1235577889b w 9b f F3F5F6') )
    ('Pure Terminal Chows', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []

    suit = sets[0][0][0]
    low = tuple([suit+r for r in "123"])
    high = tuple([suit+r for r in "789"])
    eye = tuple([suit+r for r in "55"])
    if sets.count(low) == 2 and sets.count(high) == 2 and sets.count(eye) == 1:
          poss.append(all_set_indexes(sets))
    return ('Pure Terminal Chows', poss)

"""
    if len(sets) == 2:
       suit = sets[0][0][0]
       if sets == [tuple([suit+r for r in "11223355778899"]), (sit['w'],)]:
          poss.append(all_set_indexes(sets))
"""

def get_all_terminals(sit):
    """
    >>> get_all_terminals( get_one_option('h c1c1c1b1b1b1c9c9c9b9b9b9d1 w d1 f F3F5F6') )
    ('All Terminals', [[0, 1, 2, 3, 4]])
    >>> get_all_terminals( get_one_option('m c1c1c1 h b1b1b1c9c9c9b9b9d1d1 w b9') )
    ('All Terminals', [[0, 1, 2, 3, 4]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    tiles = sum([list(s) for s in sets], [])
    terminals = make_tile_list('b1b9c1c9d1d9')
    if all([t in terminals for t in tiles]):
        poss.append(all_set_indexes(sets))
    return ('All Terminals', poss)

def get_four_concealed_pungs(sit):
    """
    >>> get_four_concealed_pungs( get_one_option('h b2b2b2d3d3d3c4c4c4d2d2d2c3 w c3 f F3F5F6') )
    ('Four Concealed Pungs', [[0, 2, 3, 4]])
    """
    poss = []
    sets_with_type = sit['sets']
    poss = find_combinations(sets_with_type, 4, is_all_concealed_pungs)
    return ('Four Concealed Pungs', poss)

# 88 points
def get_big_four_winds(sit):
    """
    >>> get_big_four_winds( get_one_option('h WeeeWsssWwwwWnnnDr w Dr rw We sw Wn f F3F5F6') )
    ('Big Four Winds', [[1, 2, 3, 4]])
    >>> get_big_four_winds( get_one_option('m Weee Wsss Wwww Wnnn h Dr w Dr rw We sw Wn') )
    ('Big Four Winds', [[0, 1, 2, 3]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_only_wind_pungs)
    return ('Big Four Winds', poss)

def get_big_three_dragons(sit):
    """
    >>> get_big_three_dragons( get_one_option('h DrrrDgggDwwwc111d9 w d9 f F3F5F6') )
    ('Big Three Dragons', [[0, 1, 2]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 3, is_only_dragon_pungs)
    return ('Big Three Dragons', poss)

def get_four_kongs(sit):
    """
    >>> get_four_kongs( get_one_option('m 2222b m 5555c m 7777d c Weeee h Dr w Dr f F3F5F6') )
    ('Four Kongs', [[0, 1, 2, 3]])
    """
    sets = get_only_sets(sit['sets'])
    poss = find_combinations(sets, 4, is_only_kongs)
    return ('Four Kongs', poss)

def get_seven_shifted_pairs(sit):
    """
    >>> get_seven_shifted_pairs( get_one_option('h 11c22c33c44c55c66c7c w 7c', 3) )
    ('Seven Shifted Pairs', [[0, 1, 2, 3, 4, 5, 6]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if (len(sets) == 7 and all([is_eye(s) for s in sets]) 
       and len(all_represented_types(sets)) == 1
       and all([int(s[0][1]) == int(sets[0][0][1])+i for i, s in enumerate(sets)])):
        poss.append(all_set_indexes(sets))
    return ('Seven Shifted Pairs', poss)


def get_all_green(sit):
    """
    >>> get_all_green( get_one_option('h 234b234b666b888bDg w Dg') )
    ('All Green', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    green = make_tile_list("b23468Dg")
    poss = []
    if is_all_tiles_in_group(sets, green):
        poss.append(all_set_indexes(sets))
    return ('All Green', poss)

def get_nine_gates(sit):
    """
    >>> get_nine_gates(get_one_option('h b1112345678999 w b7', 0))
    ('Nine Gates', [[0, 1, 2, 3, 4]])
    """
    sets = get_only_sets(sit['sets'])
    poss = []
    if len(sit['waits']) == 9:
        h_wait = sit['h_wait']
        suit = sit['w'][0]
        if h_wait == [suit+r for r in "1112345678999"]:
            poss.append(all_set_indexes(sets))
    return ('Nine Gates', poss)

def get_thirteen_orphans(sit):
    """
    >>> get_thirteen_orphans(get_one_option('h 19d19b19cDrgwWeswn w Wn', 0))
    ('Thirteen Orphans', [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]])
    """
    poss = []
    sets = get_only_sets(sit['sets'])
    if len(sets) == 13:
        poss.append(all_set_indexes(sets))
    return ('Thirteen Orphans', poss)


#### End of hands ####


def add_key_value(d, kv):
    (key, value) = kv
    if len(value) != 0:
        d[key] = value

def get_fans(sit):
    """
    >> import pprint
    >> #pprint.pprint(get_fans(get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    >> len(get_fans(get_one_option('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    81
    >> #pprint.pprint(get_fans(get_one_option('m b1b2b3 m b4b5b6 c Weeee h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    >> len(get_fans(get_one_option('m b1b2b3 m b4b5b6 c Weeee h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')))
    81
    >> #pprint.pprint(get_fans(get_one_option('h b1112345678999 w b7', 1)))
    >> len(get_fans(get_one_option('h b1112345678999 w b7', 1)))
    81
    >> #pprint.pprint(get_fans(get_one_option('h b222333444888Dg w Dg self_draw')))
    >> len(get_fans(get_one_option('h b222333444888Dg w Dg self_draw')))
    81
    >>> get_fans(get_one_option('m d1d2d3 m b4b4b4 m c7c8c9 h DrDrd3d4 w d5 f F3F5F6'))
    {'Chicken Hand': [[True]], 'Flower Tiles': [['F3'], ['F5'], ['F6']]}
    """
    # print sit['sets']
    fans = {}

    identifiers = [
                   # 1 points
                   get_pure_double_chow, get_mixed_double_chow, get_short_straight, 
                   get_two_terminal_chows, get_pung_of_terminals_or_honors, get_melded_kong, 
                   get_one_voided_suit, get_no_honors, 
                   get_edge_wait, get_closed_wait, get_single_wait, get_self_drawn, 
                   get_flower_tiles, 
                   # 2 points
                   get_dragon_pung, get_prevalent_wind, get_seat_wind, 
                   get_all_chows, get_double_pung, get_two_concealed_pungs, 
                   get_concealed_kong, get_all_simples, get_concealed_hand, 
                   get_tile_hog, 
                   # 4 points
                   get_two_melded_kongs, get_outside_hand, get_fully_concealed_hand, get_last_tile, 
                   # 6 points
                   get_two_dragon_pungs, get_mixed_shifted_chows, get_all_pungs, 
                   get_half_flush, get_all_types, get_melded_hand, 
                   # 8 points
                   get_mixed_triple_chows, get_mixed_straight, get_mixed_shifted_pungs, 
                   get_two_concealed_kongs, get_last_tile_draw, get_last_tile_claim, 
                   get_out_with_replacement_tile, get_robbing_the_kong, get_reversible_tiles, 
                   # Can't put chicken here (in 8 points), 
                   # because it will be identified when nothing in this list is found

                   # 12 points
                   get_big_three_winds, get_knitted_straight, get_upper_four, get_lower_four, 
                   get_lesser_honors_and_knitted_tiles, 
                   # 16 points
                   get_pure_shifted_chows, get_pure_straight, get_three_suited_terminal_chows, 
                   get_triple_pung, get_three_concealed_pungs, get_all_fives, 
                   # 24 points
                   get_pure_triple_chow, get_all_even_pungs, get_pure_shifted_pungs, 
                   get_seven_pairs, get_full_flush, get_upper_tiles, get_middle_tiles, get_lower_tiles, 
                   get_greater_honors_and_knitted_tiles, 
                   # 32 points
                   get_four_pure_shifted_chows, get_all_terminals_and_honors, get_three_kongs, 
                   # 48 points
                   get_quadruple_chow, get_four_pure_shifted_pungs, 
                   # 64 points
                   get_little_four_winds, get_little_three_dragons, get_all_honors, 
                   get_pure_terminal_chows, get_all_terminals, get_four_concealed_pungs, 
                   # 88 points
                   get_big_four_winds, get_big_three_dragons, get_four_kongs, 
                   get_seven_shifted_pairs, get_all_green, get_nine_gates, 
                   get_thirteen_orphans, 
                   ]
    for identifier in identifiers:
        add_key_value(fans, identifier(sit))

    if fans.keys() in [[], ['Flower Tiles']]:
        add_key_value(fans, ("Chicken Hand", [[True]]))
    return fans

def _test():
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run("import doctest; doctest.testmod()")

if __name__ == "__main__":
    _test()

