def xcombinations(items, n):
    """
    >>> print list(xcombinations(list("abcd"), 3))
    [('a', 'b', 'c'), ('a', 'b', 'd'), ('a', 'c', 'd'), ('b', 'c', 'd')]
    >>> print len(list(xcombinations(range(14), 3))) == 14*13*12/6
    True
    >>> print len(list(xcombinations(range(14), 8))) == 14*13*12*11*10*9*8*7/40320
    True
    >>> print len(list(xcombinations(range(24), 8))) == 24*23*22*21*20*19*18*17/40320
    True
    >>> print list(xcombinations(list(""), 2))
    []
    >>> print list(xcombinations(list("1234"), 2))
    [('1', '2'), ('1', '3'), ('1', '4'), ('2', '3'), ('2', '4'), ('3', '4')]
    """
    if n==0: 
        yield (())
    else:
        for i in xrange(len(items)):
            for tailcomb in xcombinations_inner(items[i + 1:], n-1):
                yield tuple((items[i],) + tailcomb)

def xcombinations_inner(items, n):
    if n==0: 
        yield (())
    else:
        for i in xrange(len(items)):
            for tailcomb in xcombinations_inner(items[i + 1:], n-1):
                yield tuple((items[i],) + tailcomb)

if __name__ == "__main__":
    import doctest
    import cProfile
    cProfile.run('doctest.testmod()')
    #doctest.testmod()
    
