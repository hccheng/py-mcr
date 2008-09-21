from mahjongutil import *
from mahjonggrouping import *

def get_options(sit):
    """
    >>> import pprint
    >>> s = parse_command_line('m b1b2b3 m b4b5b6 c 9999b h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')
    >>> os = get_options(s)
    >>> pprint.pprint(os)
    [{'c': [('b9', 'b9', 'b9', 'b9')],
      'f': ['F3', 'F5', 'F6'],
      'h': [('b1', 'b1'), ('b5', 'b6', 'b7')],
      'h_wait': ['b1', 'b1', 'b5', 'b6'],
      'kong_replacement': False,
      'last_turn': False,
      'm': [('b1', 'b2', 'b3'), ('b4', 'b5', 'b6')],
      'robbing': False,
      'rw': None,
      'self_draw': False,
      'sets': [('m', ('b1', 'b2', 'b3')),
               ('m', ('b4', 'b5', 'b6')),
               ('c', ('b9', 'b9', 'b9', 'b9')),
               ('h', ('b1', 'b1')),
               ('h', ('b5', 'b6', 'b7'))],
      'sw': None,
      'v': ['b7', 'b7', 'b7'],
      'w': 'b7',
      'waits': ['b4', 'b7']}]
    >>> s = parse_command_line('c b9b9b9b9 h b11122233 w b3 f F3F5F6 v b7b7b7 self_draw')
    >>> os = get_options(s)
    >>> pprint.pprint(os)
    [{'c': [('b9', 'b9', 'b9', 'b9')],
      'f': ['F3', 'F5', 'F6'],
      'h': [('b1', 'b1', 'b1'), ('b2', 'b2', 'b2'), ('b3', 'b3', 'b3')],
      'h_wait': ['b1', 'b1', 'b1', 'b2', 'b2', 'b2', 'b3', 'b3'],
      'kong_replacement': False,
      'last_turn': False,
      'm': [],
      'robbing': False,
      'rw': None,
      'self_draw': True,
      'sets': [('c', ('b9', 'b9', 'b9', 'b9')),
               ('h', ('b1', 'b1', 'b1')),
               ('h', ('b2', 'b2', 'b2')),
               ('h', ('b3', 'b3', 'b3'))],
      'sw': None,
      'v': ['b7', 'b7', 'b7'],
      'w': 'b3',
      'waits': ['b3']},
     {'c': [('b9', 'b9', 'b9', 'b9')],
      'f': ['F3', 'F5', 'F6'],
      'h': [('b1', 'b2', 'b3'), ('b1', 'b2', 'b3'), ('b1', 'b2', 'b3')],
      'h_wait': ['b1', 'b1', 'b1', 'b2', 'b2', 'b2', 'b3', 'b3'],
      'kong_replacement': False,
      'last_turn': False,
      'm': [],
      'robbing': False,
      'rw': None,
      'self_draw': True,
      'sets': [('c', ('b9', 'b9', 'b9', 'b9')),
               ('h', ('b1', 'b2', 'b3')),
               ('h', ('b1', 'b2', 'b3')),
               ('h', ('b1', 'b2', 'b3'))],
      'sw': None,
      'v': ['b7', 'b7', 'b7'],
      'w': 'b3',
      'waits': ['b3']}]
    """
    hand_plus_winning = sit['h'] + [sit['w']]
    hand_combination_options = group_tiles(hand_plus_winning)
    situation_options = []
    for ho in hand_combination_options:
        sit_op = dict(sit)
        sit_op['h_wait'] = sit_op['h']
        sit_op['h'] = ho
	sit_op['sets'] = [('m', st) for st in sit_op['m']] + [('c', st) for st in sit_op['c']] + [('h', st) for st in ho]
        situation_options.append(sit_op)
    return situation_options

def make_normal_inline(sit):
    s = []
    for c in "mc":
        if len(sit[c]) > 0:
            s.extend([c] + ["".join(ts) for ts in sit[c]])
    if len(sit['h']) > 0:
        s.extend(['h', "".join(sit['h'])])
    if len(sit['w']) > 0:
        s.extend(['w', sit['w']])
    if len(sit['v']) > 0:
        s.extend(['v', "".join(sit['v'])])
    if len(sit['f']) > 0:
        s.extend(['f', "".join(sit['f'])])
    if sit['rw']:
        s.extend(['rw', sit['rw']])
    if sit['sw']:
        s.extend(['sw', sit['sw']])
    for flag in ['self_draw', 'last_turn', 'kong_replacement', 'robbing']:
        if sit[flag]:
            s.append(flag)
    return " ".join(s)

def parse_command_line(s):
    """
    >>> import pprint
    >>> s = parse_command_line('m b1b2b3 m b4b5b6 c b9b9b9b9 h b1b1b5b6 w b7 f F3F5F6 v b7b7b7')
    >>> pprint.pprint(s)
    {'c': [('b9', 'b9', 'b9', 'b9')],
     'f': ['F3', 'F5', 'F6'],
     'h': ['b1', 'b1', 'b5', 'b6'],
     'kong_replacement': False,
     'last_turn': False,
     'm': [('b1', 'b2', 'b3'), ('b4', 'b5', 'b6')],
     'robbing': False,
     'rw': None,
     'self_draw': False,
     'sw': None,
     'v': ['b7', 'b7', 'b7'],
     'w': 'b7',
     'waits': ['b4', 'b7']}
    >>> s = parse_command_line('m b1b2b3 m b4b5b6 c b9b9b9b9 h b1b5b6 w b7 f F3F5F6 v b7b7b7 last_turn sw We')
    >>> print s['sw']
    We
    >>> print s['last_turn']
    True
    >>> s = parse_command_line('m b1b2b3 m b4b5b6 c b9b9b9b9 h b1b5b6 w b7 f F3F5F6 v b7b7b7 last_turn sw We kong_replacement')
    >>> s = parse_command_line('m b1b2b3 m b4b5b6 h b9b9b9 h b1b5b6 w b7 f F3F5F6 v b7b7b7 sw We kong_replacement')
    Traceback (most recent call last):
    ...
    ParseException: Must have a kong to have kong_replacement
    >>> s = parse_command_line('m b1b2b3 m b5b6b7 h b9b9b9 h b1b5b6 w b7 f F3F5F6 sw We robbing')
    Traceback (most recent call last):
    ...
    ParseException: The winning tile is already in the hand, it can not be robbing the kong
    >>> s = parse_command_line('m b1b2b3 m b5b6b7 h b9b9b9 h b1b5b6 w b7 f F3F5F6 sw We robbing v b9b9')
    Traceback (most recent call last):
    ...
    ParseException: There are only four tiles of each, and one of each flower
    """
    types = list('mchwvf') + ['sw', 'rw']
    booleans = "self_draw last_turn kong_replacement robbing".split()
    ws = s.split()
    boxed = {}
    type = None
    for w in ws:
        if w in booleans:
            boxed[w] = True
        elif w in types:
            type = w
        else:
            l = boxed.get(type, [])
            l.append(w)
            boxed[type] = l
    #print boxed
    melded = [tuple(make_tile_list(mt)) for mt in boxed.get('m', [])]
    concealed = [tuple(make_tile_list(mt)) for mt in boxed.get('c', [])]
    hand = make_tile_list("".join(boxed.get('h', [])))
    winning = make_tile_list("".join(boxed.get('w', [])))
    visible = make_tile_list("".join(boxed.get('v', [])))
    flowers = make_tile_list("".join(boxed.get('f', [])))
    seat_wind = make_tile_list("".join(boxed.get('sw', [])))
    round_wind = make_tile_list("".join(boxed.get('rw', [])))
    self_draw = boxed.get('self_draw', False)
    last_turn = boxed.get('last_turn', False)
    kong_replacement = boxed.get('kong_replacement', False)
    robbing = boxed.get('robbing', False)

    if len(winning) == 0:
        raise ParseException("No winning tile given")
    if len(winning) > 1:
        raise ParseException("More than one winning tile given")
    if len(seat_wind) > 1:
        raise ParseException("More than one seat wind given")
    if len(seat_wind) == 0:
        seat_wind.append(None)
    if len(round_wind) > 1:
        raise ParseException("More than one round wind given")
    if len(round_wind) == 0:
        round_wind.append(None)

    player_tiles_wo_win = sum([list(st) for st in melded + concealed], []) + hand
    used_tiles = player_tiles_wo_win + winning + visible + flowers
    max_tile = max([used_tiles.count(t) 
	            for t in used_tiles if t[0] != "F"] +[0])
    max_flower = max([used_tiles.count(t) 
	              for t in used_tiles if t[0] == "F"] +[0])
    if max_tile > 4 or max_flower > 1:
        raise ParseException("There are only four tiles of each, and one of each flower")

    if kong_replacement and not any([is_kong(st) for st in melded+concealed]):
        raise ParseException("Must have a kong to have kong_replacement")

    if robbing:
	if winning[0] in player_tiles_wo_win:
            raise ParseException("The winning tile is already in the hand, it can not be robbing the kong")

    ts = all_non_flower_tile_types()
    tile_count = {}
    for t in hand:
        tile_count[t] = tile_count.get(t, 0) + 1
    all_in_hand = [t for t, c in tile_count.items() if c == 4]
    ts = list(set(ts).difference(set(all_in_hand)))
    ts.sort()
    # ts is now a sorted list of all tile types (except flowers) that there 
    # are at least one left of (i.e. not all 4 are already in the hand). 

    waits = [t for t in ts if len(group_tiles(hand + [t])) != 0]

    situation = {
            'm': melded,
            'c': concealed,
            'h': hand,
            'w': winning[0],
            'waits' : waits, 
            'v': visible,
            'f': flowers,
            'rw': round_wind[0], 
            'sw': seat_wind[0], 
            'self_draw': self_draw,
            'last_turn': last_turn,
            'kong_replacement': kong_replacement,
            'robbing': robbing,
    }

    #if len(get_options(situation)) > 0:
        #fileHandle = open ( 'inex.txt', 'a' )
        #fileHandle.write (s + '\n')
        #fileHandle.close() 
        
    return situation

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

