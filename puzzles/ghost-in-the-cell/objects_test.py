from main import Factory

def test_create_factory():
   factory = Factory(['1', 'FACTORY', '2', '3', '4', '', ''])

   assert factory.entity_id ==  1
   assert factory.owner == 2
   assert factory.cyborg_count == 3
   assert factory.production == 4