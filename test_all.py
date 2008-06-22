import os
import time
import doctest

def do_tests():
    tests = [
             "fanimplications", 
             "fanpoints",
             "xcombinations", 
             "HTMLTags", 
             "mahjongutil", 
             "informat", 
             "mahjonggrouping", 
             "maxpoints",
             "identifan", 
            ]
    for t in tests:
        print "%s: " % t
        start_time = time.time()
        module = __import__(t)
        r = doctest.testmod(module)
        s_duration = time.time() - start_time
        tests_failed, tests_performed = r
        print ("%d tests, %d failed in %.2fs --\n" % 
              (tests_performed, tests_failed, s_duration))

if __name__ == "__main__":
    do_tests()
