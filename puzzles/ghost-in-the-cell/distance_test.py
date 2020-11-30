from main import DistanceCalculator, Factory

def test_calculate_distance():
   factory1 = Factory(['1', 'FACTORY', '2', '3', '4', '', ''])
   factory2 = Factory(['2', 'FACTORY', '2', '3', '4', '', ''])

   dist_map = {(1,2): 123}

   calc = DistanceCalculator(dist_map)

   assert 123 == calc.get_distance(factory1, factory2) 
   assert 123 == calc.get_distance(factory2, factory1) 