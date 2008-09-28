from informat import *
from identifan import *
from fanpoints import *
from fanimplications import *
from mahjongutil import *
import pprint

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
    implied = []
    implied_names = get_implied_map()[name]
    for i, (p, checked_name, checked_sets) in enumerate(scoring_elements):
        if checked_name in implied_names:
            if set(checked_sets).issubset(set(sets_used)):
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
        if name in waits and checked_name in waits and name != checked_name: 
            excluded.append(i)        
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
    >>> max_points(parse_command_line('h 123123b123123bWe w We')) # Quadrople chows should imply tile hogs
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
    Obs! Reversible should not imply One Voided, it should be an exception
    >>> #Har kommit till 3.5 i Beyond the Green Book
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

