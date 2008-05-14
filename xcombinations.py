def xcombinations(items, n):
    """
    >>> combgen = xcombinations(list("abcd"), 3)
    >>> print [c for c in combgen]
    [('a', 'b', 'c'), ('a', 'b', 'd'), ('a', 'c', 'd'), ('b', 'c', 'd')]
    >>> print len([c for c in xcombinations(range(14), 3)]) == 14*13*12/6
    True
    >>> combgen = xcombinations(list(""), 2)
    >>> print [c for c in combgen]
    []
    >>> combgen = xcombinations(list("1234"), 2)
    >>> print [c for c in combgen]
    [('1', '2'), ('1', '3'), ('1', '4'), ('2', '3'), ('2', '4'), ('3', '4')]
    """
    if n==0: 
        yield (())
    else:
        for i in xrange(len(items)):
            for tailcomb in xcombinations_inner(list(items[i + 1:]), n-1):
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
    doctest.testmod()
    
