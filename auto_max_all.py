from informat import *
from maxpoints import *
import pprint

def main():
    sit_lines = []
    for file_name in ['inex.txt', 'extra_inex.txt']:
        f = open(file_name)
        sit_lines.extend(get_sits_from_file(f))
    for sit_line in sit_lines:
        sit = parse_command_line(sit_line)
        print "\n Situation line: %s" % sit_line
        opts = get_options(sit)
        for i, option in enumerate(opts):
            print 'Option #%d' % i
            pprint.pprint(option)
            selected_fans = option_max_points(option)
            print 'Selected fans: '
            pprint.pprint(selected_fans)
            print 'Points: %d' % get_total_points(selected_fans)

def get_sits_from_file(f):
    sits = []
    try:
        for line in f:
            if not line.startswith('#'):
                line = line[:-1]
                sits.append(line)
    finally:
        f.close()
    return sits

if __name__ == "__main__":
    main()

