import os
import time

def do_tests():
    tests = ["mahjongutil.py",
             "mahjonggrouping.py", 
             "informat.py", 
             "xcombinations.py", 
             "fanimplications.py", 
             "identifan.py", 
             "HTMLTags.py", 
             "fanpoints.py"]
    for t in tests:
        print "-- Starting %s --" % t
        start_time = time.time()
        r = os.system("python %s" % t)
        s_duration = time.time() - start_time
        print "-- Result of %s: %d - time %f --" % (t, r, s_duration)

if __name__ == "__main__":
    do_tests()
