import sys
import math
from enum import Enum
import functools
from typing import List

class Types(Enum):
    FACTORY = 1
    TROOP = 2
    BOMB = 3

LOG_LEVEL = 3

def log_debug(topic, message):
    if LOG_LEVEL >= 3:
        print(f'[DEBUG][{topic}]', message, file=sys.stderr, flush=True)

def log_info(topic, message):
    if LOG_LEVEL >= 2:
        print(f'[INFO][{topic}]', message, file=sys.stderr, flush=True)


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

    def get_nearest(self, source: Factory, targets: List[Factory]) -> Factory:
        nearest = None

        for target in targets:
            dist = self.get_distance(source, target)
            if not nearest or dist > nearest[0]:
                nearest = (dist, target)

        return nearest[1]

class Strategy:

    def __init__(self, owned: List[Factory], neutral: List[Factory], enemy: List[Factory], distances):
        self.owned = owned
        self.neutral = neutral
        self.enemy = enemy
        self.distances = distances
        self.distance_calculator = DistanceCalculator(distances)


    def run(self) -> List[Action]:
        raise NotImplementedError

class StrategyMoveSwarmNeutral(Strategy):

    def run(self):
        print('[STRATEGY] StrategyMoveSwarmNeutral', file=sys.stderr, flush=True)

        targeted = []

        actions = []
        for source in sorted(self.owned, key=lambda f: f.cyborg_count):
            log_debug('handling source', source)
            
            # @todo more for high prod
            att_per_target = math.floor(source.cyborg_count / len(self.neutral))
            # @todo sort by production

            for target in sorted(self.neutral, key=(lambda f : (f.production, f.cyborg_count)), reverse=True):
                if target.entity_id in targeted:
                    continue

                if source.cyborg_count < 4:
                    break
                log_debug('handling target', target)
                # if source.cyborg_count > att_per_target + 1:
                if source.cyborg_count > target.cyborg_count + 4:
                    action = MoveAction(source, target, target.cyborg_count + 1)
                    log_info(f'[ATTACK]', action)
                    
                    actions.append(action)
                    source.cyborg_count -= target.cyborg_count + 1
                    targeted.append(target.entity_id)

            
            if source.cyborg_count < 4:
                break

        return actions

class StrategyBombFirstTarget(Strategy):
    
    def run(self):
        for source in sorted(self.owned, key=lambda f: f.cyborg_count):
            log_debug('handling source', source)
            for target in self.enemy:
                log_debug('handling enemy', target)
                return [BombAction(source, target)]

class StrategyMoveEasyTargets(Strategy):

    def run(self):
        actions = []
        for source in sorted(fact_map_own, key=lambda f: f.cyborg_count):
            log_debug('handling source', source)

            for target in sorted(fact_map_enemy, key=lambda f: (f.cyborg_count, f.production), reverse=True):
                log_debug('handling enemy', target)
                if source.cyborg_count > target.cyborg_count + 2:
                    action = MoveAction(source, target, target.cyborg_count + 1)
                    log_info(f'[ATTACK]', action)
                    actions.append(action)
                    source.cyborg_count -= target.cyborg_count + 1

        return actions





def sort_targets(x, y):
    return x.cyborg_count > y.cyborg_count


def handle_loop_julian_tryouts(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map, turn):
    actions = []

    strategies = []

    if turn == 1:
        strategies.append(StrategyBombFirstTarget(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map))

    if turn <= 3 or len(fact_map_neutral) > 0:
        strategies.append(StrategyMoveSwarmNeutral(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map))
    else:
        strategies.append(StrategyMoveEasyTargets(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map))
    
    for s in strategies:
        actions += s.run()
    return actions

if __name__ == "__main__":
    factory_count = int(input())  # the number of factories
    link_count = int(input())  # the number of links between factories

    link_dist_map = {}

    for _ in range(link_count):
        factory_1, factory_2, distance = [int(j) for j in input().split()]
        link_dist_map[tuple(sorted([factory_1, factory_2]))] = distance
    
    turn = 0
    # game loop
    while True:
        turn += 1
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

        actions = handle_loop_julian_tryouts(fact_map_own, fact_map_neutral, fact_map_enemy, link_dist_map, turn)

        if len(actions) > 0:
            print('; '.join([str(a) for a in actions]))
        else:
            print(str(WaitAction()))