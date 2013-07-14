from informat import *
from identifan import *
from fanpoints import *
from fanimplications import *
from mahjongutil import *

NOT_CLAIMED = 0
CLAIMED = 1
IMPOSSIBLE = 2

def fan_claim_plan(fan_status, accountOnce, dirty_sets, sets):
    if fan_status == IMPOSSIBLE or fan_status == CLAIMED:
        return False, False
    elif not accountOnce:
        return True, False
    elif len(dirty_sets) == 0:
        return True, False # This is the first accountOnce hand
    elif len(dirty_sets.intersection(set(sets))) == 1:
        return True, False # Perfect, only one sets already dirty
    elif len(dirty_sets.intersection(set(sets))) > 1:
        return False, False # This would break the account once principle
    else:
        return False, True # It's account once, not first, but no dirty sets used -> wait
            
    """
    If an account once hand comes along when some tiles are already dirty, and it does not have any
    tiles in common with the dirty tiles, then put it 'on hold' until another account once hand is added, 
    or when there are no more hands to add. 
    """

def claim_fan(i, fan_status, accountOnce, dirty_sets, sets, excluded_fans):
    fan_status[i] = CLAIMED
    if accountOnce:
        dirty_sets.update(set(sets))
    for j in excluded_fans:
        fan_status[j] = IMPOSSIBLE

def optimal_claimed_fans(exclusion_fans):
    fan_status = [NOT_CLAIMED] * len(exclusion_fans)
    dirty_sets = set()
    for be_greedy in [False, True]:
        progress = True
        while progress:
            progress = False
            for i, line in enumerate(exclusion_fans):
                score, name, sets, implied, identical, exceptions, accountOnce = line
                claim_now, claim_later = fan_claim_plan(fan_status[i], accountOnce, dirty_sets, sets)
                if claim_now or (be_greedy and claim_later):
                    claim_fan(i, fan_status, accountOnce, dirty_sets, sets, implied+identical+exceptions)
                    progress = True
                    break
                if not claim_now and not claim_later and fan_status[i] == NOT_CLAIMED: 
                    # This is a fan that would break the account once princ.
                    fan_status[i] = IMPOSSIBLE
                    progress = True
                    break

    assert(sum([1 for v in fan_status if v == NOT_CLAIMED]) == 0) # All must be either claimed or impossible
    return [i for i, v in enumerate(fan_status) if v == CLAIMED]
        
def score_of_claimed(exclusion_fans, claimed_fans):
    total = 0
    for i in claimed_fans:
        score, name, sets, implied, identical, exceptions, accountOnce = exclusion_fans[i]
        total += score
    return total

def make_one_fan_per_line(fans):
    point_fans = [(get_points(fan), fan, s) 
                  for fan, sets in fans.items()
                  for s in sets]
    point_fans.sort()
    point_fans.reverse()
    return point_fans

def get_implied(name, sets_used, scoring_elements):
    """
    >>> get_implied("Quadruple Chow", [1, 2, 3, 4], [(48, 'Quadruple Chow', [1, 2, 3, 4]), (24, 'Pure Triple Chow', [2, 3, 4]), (24, 'Pure Triple Chow', [1, 3, 4]), (24, 'Pure Triple Chow', [1, 2, 4]), (24, 'Pure Triple Chow', [1, 2, 3]), (6, 'Half Flush', [0, 1, 2, 3, 4]), (4, 'Outside Hand', [0, 1, 2, 3, 4]), (2, 'Tile Hog', ['b3']), (2, 'Tile Hog', ['b2']), (2, 'Tile Hog', ['b1']), (2, 'Concealed Hand', [0, 1, 2, 3, 4]), (1, 'Single Wait', [True]), (1, 'Pure Double Chow', [3, 4]), (1, 'Pure Double Chow', [2, 4]), (1, 'Pure Double Chow', [2, 3]), (1, 'Pure Double Chow', [1, 4]), (1, 'Pure Double Chow', [1, 3]), (1, 'Pure Double Chow', [1, 2])])
    [1, 2, 3, 4, 7, 8, 9, 12, 13, 14, 15, 16, 17]
    """

    implied = []
    implied_names = get_implied_map()[name]
    for i, (p, checked_name, checked_sets) in enumerate(scoring_elements):
        if checked_name in implied_names:
            if set(checked_sets).issubset(set(sets_used)):
                implied.append(i)
            elif checked_name == "Tile Hog":
                # Only Quadruple Chow implies Tile Hog, and it includes 12 of the 14 tiles, so there
                # cannot be any Tile Hogs in the hand. 
                implied.append(i)
                
    return implied

def get_identical(name, sets_used, scoring_elements):
    identical = []
    for i, (p, checked_name, checked_sets) in enumerate(scoring_elements):
        if (checked_name == name and 
            checked_sets != sets_used and 
            len(set(checked_sets).intersection(set(sets_used))) != 0):
            identical.append(i)
    return identical

def get_exceptional_exclusions(name, sets_used, scoring_elements):
    excluded = []
    waits = ['Closed Wait', 'Edge Wait', 'Single Wait']
    does_not_combine_with_waits = ['Seven Pairs']
    for i, (p, checked_name, checked_sets) in enumerate(scoring_elements):
        # Not needed, since the waits are defined like waiting for a pair, or tile in chow
        #if name == "Thirteen Orphans" and checked_name == "Single Wait":
        #    excluded.append(i)        

        # Waits excludes each other
        if name in waits and checked_name in waits and name != checked_name: 
            excluded.append(i)        

        # Seven pairs does not combine with any wait
        if name in does_not_combine_with_waits and checked_name in waits:
            excluded.append(i)
    return excluded

def account_once_applies(sets_used, sets_in_hand):
    if sets_used == [True]:
        return False # The non set elements are not account once elements (i.e. self draw, waits...)
    if len(sets_used) == 1 and isinstance(sets_used[0], str):
        return False # The list is just one element long, and it's a string -> Tile hog
    tile_sets = [sets_in_hand[i][1] for i in sets_used] 
    return all(is_sorted_chow(s) for s in tile_sets)

def add_exclusion_columns(se, sets_in_hand): 
    return [[p, n, sets, 
             get_implied(n, sets, se), 
             get_identical(n, sets, se), 
             get_exceptional_exclusions(n, sets, se), 
             account_once_applies(sets, sets_in_hand)] 
             for p, n, sets in se]

def max_points_of_option(option):
    fans = get_fans(option)
    point_fans = make_one_fan_per_line(fans)
    sets = option['sets']
    exclusion_fans = add_exclusion_columns(point_fans, sets)
    claimed_fans = optimal_claimed_fans(exclusion_fans)
    return score_of_claimed(exclusion_fans, claimed_fans)

def max_points(sit):
    """
    >>> max_points(parse_command_line('m 333d h 1116667772d w 2d')) # Hand 1
    47
    >>> max_points(parse_command_line('m 657b h 345678d4456c w 4c self_draw')) # Hand 2
    12
    >>> max_points(parse_command_line('m 234b 234d h 567b567dDg w gD self_draw')) # Hand 3
    6
    >>> max_points(parse_command_line('h 11d99brrDssWggD11c1d w 1d')) # Hand 4
    64
    >>> max_points(parse_command_line('h 1c258d369bwsenWgrD w Dw')) # Hand 5
    24
    >>> max_points(parse_command_line('m 123b 456b 789b h 45bDgg w 6b')) # Hand 6
    23
    >>> max_points(parse_command_line('m 345b 567b 789b h 456bWw w Ww')) # Hand 7
    24
    >>> max_points(parse_command_line('m b222 h c333 d444 b567 b8 w b8')) # Hand 8
    12
    >>> max_points(parse_command_line('m 345c h 111222333bWs w Ws')) # Hand 9
    43
    >>> max_points(parse_command_line('h d1d1d1d1c2c2c2d2d2d2d2d3d3 w d3 self_draw')) # Hand 10
    52
    >>> max_points(parse_command_line('m 234b h 567b345678c3d w d3 self_draw')) # Hand 11
    8

    Examples from "Beyond the Green Book"
    >>> max_points(parse_command_line('h 123123b123123bWe w We')) # Quadruple chows should imply tile hogs
    61
    >>> #If a combination of two scoring elements implies a third, that one is still claimable
    >>> max_points(parse_command_line('m 888b 234b h 234b666b2b w 2b'))
    117
    >>> #Strange exception from Beyond the Green
    >>> max_points(parse_command_line('h 222233446688bDg w Dg'))
    118
    Strange exception from Beyond the Green (All green does not get for One Voided)
    >>> #Strange exception from Beyond the Green
    >>> max_points(parse_command_line('h 1199b1199c11999d w 9d self_draw'))
    Strange exception from Beyond the Green (All terminals does not get for One Voided)
    92
    >>> #Reversable does not combine with One Voided, even though it is not implied by def. 
    >>> max_points(parse_command_line('m 222b h 456b12345d99d w 3d'))
    9

    >>> #Have reached 3.5 in "Beyond the Green Book"

    New tests for version 1.1, all the fixed bugs

    Chicken Hand should be 8 points, used to be 12. (Lasker 2009-10-18)
    >>> max_points(parse_command_line('m 345d 444b 978c h 3d4d DrDr w d2')) 
    8

    Outside Hand can include kongs. (Lasker 2009-10-18)
    >>> max_points(parse_command_line('h b789 c9 m DwDwDw DrDrDrDr WsWsWs w c9')) 
    14

    West Wind and White Dragon does not have the same tile value, pungs of them will not be
    a Double Pung. (Lasker 2009-10-18)
    >>> max_points(parse_command_line('m DwDwDw WwWwWw h d999 d88 c67 w c8 rw Ww sw Ww')) 
    8

    Quadruple chows should imply tile hogs (From Beyond the Green Book)
    >>> max_points(parse_command_line('h 123123123123bWe w We')) 
    61

    All Types should not block all Pung of Terminals or Honors. (Dick-mt, 2012-12-24)
    >>> max_points(parse_command_line('v Dgg m c999 Wnnn h b666 d999 Dg w Dg')) 
    20


    Not fixed yet:

    The pung of the winning tile does not count for concealed pungs. (Lasker 2009-10-18)
    >>> max_points(parse_command_line('m c78c9 h b333 c555 d88 DwDw w d8')) 
    2

    Reported, but not yet verified as an error: 

    Is it possible to get Last Tile, when two are visible, and the winning tile completes the eye? 
    >>> max_points(parse_command_line('v Dgg h Dg Wss d1122448899 w Dg self_draw')) 
    38
"""

    options = get_options(sit)
    return max(max_points_of_option(option) for option in options)

def _test():
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run("import doctest; doctest.testmod()")

if __name__ == "__main__":
    _test()

