from informat import *
from identifan import *
from fanpoints import *
from fanimplications import *
from maxpoints import *
from HTMLTags import *
import pprint
import sys

def getTileImages(ts):
    fragment = TEXT()
    for t in ts:
        fragment += IMG(src='images/%s.png' % t, alt=':%s: ' % t, 
                        width = 36, height = 50, title=t)
    return fragment

def makeTable(header, cells):
    fragment = TR(sum((TH(h) for h in header), TEXT()))
    for r in cells:
        fragment += TR(sum((TD(c) for c in r), TEXT()))
    return TABLE(fragment)

def makeIdTable(header, cells):
    fragment = TR(sum((TH(h) for h in header), TH('Id')))
    for i, r in enumerate(cells):
        fragment += TR(sum((TD(c) for c in r), TD(str(i))))
    return TABLE(fragment)

def getSituationFragment(sit):
    fragment = TEXT()
    if len(sit['m']) > 0:
        fragment += TR(TH("Melded") + TD(Sum([getTileImages(ts) for ts in sit['m']], TEXT(" "))))
    if len(sit['c']) > 0:
        fragment += TR(TH("Concealed") + TD(Sum([getTileImages(ts) for ts in sit['c']], TEXT(" "))))
    if len(sit['h']) > 0:
        if 'h_wait' in sit: # This is an arranged hand, an option
            fragment += TR(TH("Hand") + TD(Sum([getTileImages(ts) for ts in sit['h']], TEXT(" "))))
        else:
            fragment += TR(TH("Hand") + TD(getTileImages(sit['h'])))
    if len(sit['w']) > 0:
        fragment += TR(TH("Winning Tile") + TD(getTileImages([sit['w']])))
    if len(sit['v']) > 0:
        fragment += TR(TH("Visible Tiles") + TD(getTileImages(sit['v'])))
    if len(sit['f']) > 0:
        fragment += TR(TH("Flowers") + TD(getTileImages(sit['f'])))
    if sit['rw']:
        fragment += TR(TH("Round Wind") + TD(getTileImages([sit['rw']])))
    if sit['sw']:
        fragment += TR(TH("Seat Wind") + TD(getTileImages([sit['sw']])))
    self_draw = sit['self_draw']
    last_turn = sit['last_turn']
    kong_replacement = sit['kong_replacement']
    robbing = sit['robbing']
    if any([self_draw, last_turn, kong_replacement, robbing]):
        circum_text = TEXT()
        if self_draw: circum_text += TEXT('Self draw. ')
        if last_turn: circum_text += TEXT('Last turn. ')
        if kong_replacement: circum_text += TEXT('Out on Kong replacement. ')
        if robbing: circum_text += TEXT('Out by robbing a Kong')
        fragment += TR(TH('Winning circumstances') + TD(circum_text))
    return TABLE(fragment)

def getWaitAnalysisFragment(sit):
    return H4('Possible going out tiles') + getTileImages(sit['waits'])

def getAnswerOrError(in_line):
    indata_fragment = H3("Situation string")+TEXT(in_line if in_line != "" else "(Empty)")
    try:
        f = getAnswer(in_line)
    except ParseException, e:
        f = H3("Error")+TEXT(str(e))
    return DIV(indata_fragment+f)

def getOptionFragment(i, option):
    this_fragment = H4('Grouping %d' % (i+1)) + getSituationFragment(option)
    fans = get_fans(option)
    point_fans = make_one_fan_per_line(fans)
    sets = option['sets']
    exclusion_fans = add_exclusion_columns(point_fans, sets)
    #this_fragment += PRE(pprint.pformat(point_fans))
    this_fragment += makeIdTable(["Score", "Name", "Sets", 
                                  "Implied", "Identical", "Exceptions", "Account Once"],
                                  exclusion_fans)
    claimed_fans = optimal_claimed_fans(exclusion_fans)
    this_fragment += PRE("Claimed fans: " + pprint.pformat(claimed_fans))
    this_fragment += PRE("Total points: %d" % score_of_claimed(exclusion_fans, claimed_fans) )
    return this_fragment

ENTIRE_HAND = "ENTIRE_HAND"

def tileStringContents(sets, winning_tile, hand_sets):
    """
    >>> print tileStringContents([2],'b7',[('m', ('b1', 'b2', 'b3')), ('m', ('b4', 'b5', 'b6')), ('c', ('b9', 'b9', 'b9', 'b9')), ('h', ('b1', 'b1')), ('h', ('b5', 'b6', 'b7'))])
    [('b9', 'b9', 'b9', 'b9')]
    >>> print tileStringContents([0,1,2,3,4],'b7',[('m', ('b1', 'b2', 'b3')), ('m', ('b4', 'b5', 'b6')), ('c', ('b9', 'b9', 'b9', 'b9')), ('h', ('b1', 'b1')), ('h', ('b5', 'b6', 'b7'))])
    ENTIRE_HAND
    >>> print tileStringContents([True],'b7',[('m', ('b1', 'b2', 'b3')), ('m', ('b4', 'b5', 'b6')), ('c', ('b9', 'b9', 'b9', 'b9')), ('h', ('b1', 'b1')), ('h', ('b5', 'b6', 'b7'))])
    [('b7',)]
    >>> print tileStringContents([0,1],'b7',[('m', ('b1', 'b2', 'b3')), ('m', ('b4', 'b5', 'b6')), ('c', ('b9', 'b9', 'b9', 'b9')), ('h', ('b1', 'b1')), ('h', ('b5', 'b6', 'b7'))])
    [('b1', 'b2', 'b3'), ('b4', 'b5', 'b6')]
    >>> print tileStringContents(['F6'],'b7',[('m', ('b1', 'b2', 'b3')), ('m', ('b4', 'b5', 'b6')), ('c', ('b9', 'b9', 'b9', 'b9')), ('h', ('b1', 'b1')), ('h', ('b5', 'b6', 'b7'))])
    [('F6',)]
    """
    if len(sets) == 1 and type(sets[0]) == str:
            # A single tile (Flower case)
            contents = [(sets[0], )]
    elif len(sets) == 1 and type(sets[0]) == bool:
            # A boolean like for single wait
            contents = [(winning_tile, )]
    elif len(sets) >= 5:
        contents = ENTIRE_HAND
    else:
        tiles = []
        for s in sets:
            set_type, set_tiles = hand_sets[s]
            tiles.append(set_tiles)
        contents = tiles
    return contents

def makeTileString(sets,winning_tile,hand_sets):
    contents = tileStringContents(sets, winning_tile, hand_sets)
    if contents == ENTIRE_HAND:
      return 'Entire hand'
    else:
      return Sum([getTileImages(ts) for ts in contents], TEXT(" "))

def getMaximumPointFragment(option):
    fans = get_fans(option)
    point_fans = make_one_fan_per_line(fans)
    sets = option['sets']
    exclusion_fans = add_exclusion_columns(point_fans, sets)
    claimed_fans = optimal_claimed_fans(exclusion_fans)
    points = score_of_claimed(exclusion_fans, claimed_fans) 

    this_fragment = H2('Maximum %d points' % points) + getSituationFragment(option) + H3('Scoring')
    fan_table = TR(TH('Points') + TH('Scoring Element') + TH('Tiles'))
    for fan_index in claimed_fans:
        fan_points, fan_name, sets, _, _, _, _ = exclusion_fans[fan_index]
	tile_string = makeTileString(sets,option['w'],option['sets'])
        fan_table += TR(TD('%d' % fan_points) +
                        TD('%s' % fan_name) +
                        TD('%s' % tile_string))
        
    this_fragment += TABLE(fan_table)
    this_fragment += P("Total points: %d" % points)

    return this_fragment

def getAnswer(in_line):
    sit = parse_command_line(in_line)
    opts = get_options(sit)
    opts.sort(key = max_points_of_option)
    opts.reverse()

    if len(opts) > 0:
        maximum_point_fragment = getMaximumPointFragment(opts[0])
    else:
        maximum_point_fragment = TEXT()

    normal_form_in_line = make_normal_inline(sit)
    normal_form_in_fragment = H3("Normal form situation string")+TEXT(normal_form_in_line)
    situation_fragment = H3("Situation")+getSituationFragment(sit) 
    wait_fragment = H3("Wait Analysis")+getWaitAnalysisFragment(sit)
    arrangement_count_fragment = (H3("Hand arrangements") +
                                  TEXT('Number of possible hand arrangements: %d' % len(opts)))
    option_fragments = [getOptionFragment(i, option) for i, option in enumerate(opts)]

    return (maximum_point_fragment + 
            H2('Details') + 
            normal_form_in_fragment + situation_fragment + 
            wait_fragment + 
            arrangement_count_fragment + sum(option_fragments, TEXT()))

def main():
    print getAnswerOrError(sys.argv[1] if len(sys.argv) > 1 else "")

def _test():
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run("import doctest; doctest.testmod()")

if __name__ == '__main__':
    main()
