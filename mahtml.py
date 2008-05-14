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
        fragment += IMG(src='tiles/%s.png' % t)
    return fragment


def getSituationFragment(sit):
    fragment = TEXT()
    if len(sit['m']) > 0:
        #fragment += H4("Melded") + Sum([getTileImages(ts) for ts in sit['m']], TEXT(" "))
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
    return str(DIV(indata_fragment+f))

def getOptionFragment(option):
    return getSituationFragment(option)

def getAnswer(in_line):
    sit = parse_command_line(in_line)
    normal_form_in_line = make_normal_inline(sit)
    normal_form_in_fragment = H3("Normal form situation string")+TEXT(normal_form_in_line)
    situation_fragment = H3("Situation")+getSituationFragment(sit) #+PRE(pprint.pformat(sit))
    wait_fragment = H3("Wait Analysis")+getWaitAnalysisFragment(sit)
    opts = get_options(sit)
    wait_fragment = H3("Hand arrangements")+TEXT('Number of possible hand arrangements: %d' % len(opts))
    option_fragments = []
    for option in opts:
        this_fragment = getOptionFragment(option)
        fans = get_fans(option)
        point_fans = make_one_fan_per_line(fans)
        point_fans.reverse()
        this_fragment += PRE(pprint.pformat(point_fans))
        option_fragments.append(LI(this_fragment))
    """
    for i, option in enumerate(opts):
        fans = get_fans(option)
        r.append("Fans:\n %s" % pprint.pformat(fans))
        point_fans = make_one_fan_per_line(fans)
        point_fans.reverse()
        r.append("One per line:\n %s" % pprint.pformat(point_fans))

    return "\n".join(r)
    """
    return normal_form_in_fragment + situation_fragment + wait_fragment + OL(Sum(option_fragments))

def main():
    print getAnswerOrError(sys.argv[1] if len(sys.argv) > 1 else "")

if __name__ == '__main__':
    main()
