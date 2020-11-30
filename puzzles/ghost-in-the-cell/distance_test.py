from main import DistanceCalculator, Factory

def test_calculate_distance():
   factory1 = Factory(['1', 'FACTORY', '2', '3', '4', '', ''])
   factory2 = Factory(['2', 'FACTORY', '2', '3', '4', '', ''])

   dist_map = {(1,2): 123}

   calc = DistanceCalculator(dist_map)

   assert 123 == calc.get_distance(factory1, factory2) 
   assert 123 == calc.get_distance(factory2, factory1)


def test_calculate_distance():
    factory1 = Factory(['1', 'FACTORY', '2', '3', '4', '', ''])
    factory2 = Factory(['2', 'FACTORY', '2', '3', '4', '', ''])
    factory3 = Factory(['3', 'FACTORY', '2', '3', '4', '', ''])
    factory4 = Factory(['4', 'FACTORY', '2', '3', '4', '', ''])

    dist_map = {
       (1,2): 123,
       (1,3): 124,
       (1,4): 122
    }

    calc = DistanceCalculator(dist_map)

    assert factory3 == calc.get_nearest(factory1, [factory2, factory3, factory4])