points_to_fans = \
     {1:  ['Pure Double Chow', 'Mixed Double Chow', 'Short Straight',
           'Two Terminal Chows', 'Pung of Terminals or Honors', 'Melded Kong',
           'One Voided Suit', 'No Honors',
           'Edge Wait', 'Closed Wait', 'Single Wait', 'Self-draw',
           'Flower Tiles'],
     2:  ['Dragon Pung', 'Prevalent Wind', 'Seat Wind',
          'All Chows', 'Double Pung', 'Two Concealed Pungs',
          'Concealed Kong', 'All Simples', 'Concealed Hand',
          'Tile Hog'],
     4:  ['Two Melded Kongs', 'Outside Hand', 'Fully Concealed Hand', 'Last Tile'],
     6:  ['Two Dragon Pungs', 'Mixed Shifted Chows', 'All Pungs',
          'Half Flush', 'All Types', 'Melded Hand'],
     8:  ['Mixed Triple Chows', 'Mixed Straight', 'Mixed Shifted Pungs',
          'Two Concealed Kongs', 'Last Tile Draw', 'Last Tile Claim',
          'Out With Replacement Tile', 'Robbing the Kong', 'Reversible Tiles', 
          'Chicken Hand'],
     12: ['Big Three Winds', 'Knitted Straight',
          'Upper Four', 'Lower Four', 'Lesser Honors and Knitted Tiles'],
     16: ['Pure Shifted Chows', 'Pure Straight', 'Three Suited Terminal Chows',
          'Triple Pung', 'Three Concealed Pungs', 'All Fives'],
     24: ['Pure Triple Chow', 'All Even Pungs', 'Pure Shifted Pungs',
          'Seven Pairs', 'Full Flush',
          'Upper Tiles', 'Middle Tiles', 'Lower Tiles',
          'Greater Honors and Knitted Tiles'],
     32: ['Four Pure Shifted Chows', 'All Terminals and Honors', 'Three Kongs'],
     48: ['Quadruple Chow', 'Four Pure Shifted Pungs'],
     64: ['Little Four Winds', 'Little Three Dragons', 'All Honors',
          'Pure Terminal Chows', 'All Terminals', 'Four Concealed Pungs'],
     88: ['Big Four Winds', 'Big Three Dragons', 'Four Kongs',
          'Seven Shifted Pairs', 'All Green', 'Nine Gates',
          'Thirteen Orphans']
     }
        

fans_to_points = dict([(f, p) for (p, fs) in points_to_fans.items() for f in fs])

def get_points(fan_name):
    """
    """
    global fans_to_points
    return fans_to_points[fan_name]

def _test():
    import doctest
    doctest.testmod()
    #import cProfile
    #cProfile.run("import doctest; doctest.testmod()")

if __name__ == "__main__":
    _test()

