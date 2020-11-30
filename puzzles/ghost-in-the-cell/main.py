import sys
import math
from enum import Enum
import functools

class Types(Enum):
    FACTORY = 1
    TROOP = 2
    BOMB = 3


class Factory:
    def __init__(self, inputs):
        self.entity_id = int(inputs[0])

        if inputs[1] == Types.TROOP:
            raise Exception('Factory got troop')

        self.owner = int(inputs[2])
        self.cyborg_count = int(inputs[3])
        self.production = int(inputs[4])
        self.arg_4 = inputs[5]
        self.arg_5 = inputs[6]

    def __str__(self):
        return f'id: {self.entity_id}, owned: {self.owner}, count: {self.cyborg_count}'

class HasAttackedException(Exception):
    def __init__(self, source, target, number, message='has attacked'):
        self.source = source
        self.target = target
        self.number = number
        self.message = message
        super().__init__(self.message)

class Action:
    
    def __str__(self):
        raise NotImplementedError

class MoveAction(Action):

    def __init__(self, source: Factory, target: Factory, number: int):
        self.source = source
        self.target = target
        self.number = number
        print('[QUEUE ATTACK]', f'{source.entity_id} -> {target.entity_id} with {number}', file=sys.stderr, flush=True)

    def __str__(self):
        return f'MOVE {self.source.entity_id} {self.target.entity_id} {self.number}'
 
class BombAction(Action):

    def __init__(self, source: Factory, target: Factory):
        self.source = source
        self.target = target
        print('[QUEUE BOMB]', f'{source.entity_id} -> {target.entity_id}', file=sys.stderr, flush=True)

    def __str__(self):
        return f'BOMB {self.source.entity_id} {self.target.entity_id}'
 
class WaitAction(Action):

    def __str__(self):
        print('[DO WAIT]', file=sys.stderr, flush=True)
        return 'WAIT'

class DistanceCalculator:

    def __init__(self, distance_map: dict) -> int:
        self.distance_map = distance_map

    def get_distance(self, source: Factory, target: Factory):
        return self.distance_map[tuple(sorted([source.entity_id, target.entity_id]))]
        
def sort_targets(x, y):
    return x.cyborg_count > y.cyborg_count

def build_factory_maps(input_list):
    fact_map_own = []
    fact_map_neutral = []
    fact_map_enemy = []

    for i in input_list:
        m_entity_type = i[1]
        if m_entity_type != Types.FACTORY:
            continue

        cur_fact = Factory(i)
        if cur_fact.owner == 1:
            fact_map_own.append(cur_fact)
        elif cur_fact.owner == 0:
            fact_map_neutral.append(cur_fact)
        else:
            fact_map_enemy.append(cur_fact)

    return fact_map_own, fact_map_neutral, fact_map_enemy



def handle_loop_julian(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map):
    actions = []

    for source in fact_map_own:
        print('[INFO] handling source', source, file=sys.stderr, flush=True)

            # print('looking for target', file=sys.stderr, flush=True)
        if source.cyborg_count <= 5:
            # print('[SKIP] source is empty', source.cyborg_count, file=sys.stderr, flush=True)
            continue

        for target in fact_map_neutral + fact_map_enemy:
            attackers = 0
            print('[INFO] handling target', target, file=sys.stderr, flush=True)

            if target.cyborg_count >= source.cyborg_count:
                print('[SKIP] target is stronger', f'{target.cyborg_count} vs {source.cyborg_count}', file=sys.stderr, flush=True)
                continue

            if target.cyborg_count == 0:
                attackers = 5 if source.cyborg_count > 10 else 1 if source.cyborg_count > 2 else 0
            else:
                attackers = int(target.cyborg_count) + 1

            if attackers > 0:
                actions.append(MoveAction(source, target, attackers))
                break

    return actions
 

if __name__ == "__main__":
    factory_count = int(input())  # the number of factories
    link_count = int(input())  # the number of links between factories

    link_dist_map = {}

    for _ in range(link_count):
        factory_1, factory_2, distance = [int(j) for j in input().split()]
        link_dist_map[tuple(sorted([factory_1, factory_2]))] = distance
       
    # game loop
    while True:
        entity_count = int(input())  # the number of entities (e.g. factories and troops)

        inputs = []

        for _ in range(entity_count):
            inputs.append(input().split())

        fact_map_own = []
        fact_map_neutral = []
        fact_map_enemy = []

        for i in inputs:
            m_entity_type = i[1]
            if m_entity_type != Types.FACTORY.name:
                continue

            cur_fact = Factory(i)
            if cur_fact.owner == 1:
                fact_map_own.append(cur_fact)
            elif cur_fact.owner == 0:
                fact_map_neutral.append(cur_fact)
            else:
                fact_map_enemy.append(cur_fact)

        actions = handle_loop_julian(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map)

        if len(actions) > 0:
            print('; '.join([str(a) for a in actions]))
        else:
            print(str(WaitAction()))
