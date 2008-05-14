from informat import *
from identifan import *
from fanpoints import *
from fanimplications import *
import pprint

def remove_implied(selected, point_fans):
    selected_points, selected_fan, selected_set = selected
    left = []
    implied = get_implied_map()[selected_fan]
    # all_used_sets are all sets used for this type of fan. 
    # Only implied fans that do not use any of these sets can be kept
    for (point, fan, sets) in point_fans:
        if fan == selected_fan:
            # A set can not be part of the same fan twice
            if all([s not in selected_set for s in sets]):
                left.append((point, fan, sets))
        elif fan in implied:
            # Keep it if at least one set is not in the selected fan
            if any([s not in selected_set for s in sets]):
                left.append((point, fan, sets))
        else:
            left.append((point, fan, sets))
    point_fans[:] = left[:]

def select_max_point_fans(point_fans):
    selected_fans = []
    while len(point_fans) > 0:
        max_fan = point_fans.pop()
        selected_fans.append(max_fan)
        remove_implied(max_fan, point_fans)
    return selected_fans

def get_total_points(point_fans):
    return sum([point*len(set_list) for (point, fan, set_list) in point_fans])

def make_one_fan_per_line(fans):
    point_fans = [(get_points(fan), fan, s) 
                  for fan, sets in fans.items()
                  for s in sets]
    point_fans.sort()
    return point_fans

def option_max_points(option):
    fans = get_fans(option)
    point_fans = make_one_fan_per_line(fans)
    print "All possible individual fans: "
    pprint.pprint(point_fans)
    return select_max_point_fans(point_fans)

def max_points(sit):
    """
    >>> s = parse_command_line('m Weee m Wsss m Wwww h WnnDrr w Wn')
    >>> print get_total_points(max_points(s)[0])
    152
    >>> pprint.pprint(max_points(s))
    [[(88, 'Big Four Winds', [[0, 1, 2, 4]]),
      (64, 'All Honors', [[0, 1, 2, 3, 4]])]]
    >>> inline = 'm 123b 456b 789b 789b h We w We'
    >>> print inline
    >>> s = parse_command_line(inline)
    >>> selected_fans = max_points(s)
    >>> pprint.pprint(selected_fans)
    
    """
    opts = get_options(sit)
    counted_fans = []
    #pprint.pprint(opts)
    for option in opts:
        fans = get_fans(option)
        counted_fans.append(option_max_points(option))
    return counted_fans

def _test():
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run("import doctest; doctest.testmod()")

if __name__ == "__main__":
    _test()

