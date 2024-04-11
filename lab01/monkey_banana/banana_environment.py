from dataclasses import dataclass
from enum import Enum
import numpy as np


# Parameters for the reward

ACTION_PENALTY = .1
GRAB_BANANA_REWARD = 5
GRAB_ORANGE_REWARD = 2


# Parameters for partial observability

SMELL_ALPHA = 0.8



@dataclass
class MonkeyBananaState:
    """
    Class describing states of the environment. A state is given by the
    position of the box, the position of the banana and the position of
    the monkey. 
    """
    box_position: int
    banana_position: int
    is_monkey_up: bool
    
    def vector_representation(self):
        return (self.box_position, self.banana_position, self.is_monkey_up)
    

@dataclass
class MonkeyBananaPartialObservation:
    """
    Class describing the perceived state of the environment, when the position
    of the banana is not visible by the monkey. Only the position of the box 
    and of the monkey are visible. But the monkey can smell the banana
    """
    box_position: int
    is_monkey_up: bool
    smells_banana: bool



class MonkeyBananaAction(Enum):
    GRAB           = 0
    CLIMB          = 1
    GO_DOWN        = 2
    MOVE_BOX_LEFT  = 3
    MOVE_BOX_RIGHT = 4



class MonkeyBananaEnvironmentTask:
    """
    Description of the general environment of the monkey and banana problem
    """
    
    
    def __init__(self, initial_banana_position: int, initial_box_position: int, room_size: int = 5):
        
        assert (initial_banana_position >= 0 and initial_banana_position < room_size), \
            "Banana position must be between 0 and the room size"
            
        assert (initial_box_position >= 0 and initial_box_position < room_size), \
            "Box position must be between 0 and the room size"
        
        self.score = 0
        self.state = MonkeyBananaState(initial_box_position, initial_banana_position, False)
        self.room_size = room_size
    
    
    def _is_box_under_banana(self):
        return self.state.banana_position == self.state.box_position
    
    def visualize(self):
        level_2 = [" "] * (self.room_size * 2 - 1)
        level_2[self.state.banana_position * 2] = '🍌'


        if self.state.is_monkey_up:
            level_1 = [" "] * (self.room_size * 2 - 1)
            level_1[self.state.box_position * 2] = '🐒'
        else: 
            level_1 = [" "] * (self.room_size * 2)
        
        if not self.state.is_monkey_up:
            level_0 = [" "] * (self.room_size * 2 - 2)
            level_0[max(self.state.box_position * 2 - 1, 0)] = '▅▅'
        else:
            level_0 = [" "] * (self.room_size * 2 - 1)
            level_0[self.state.box_position * 2] = '▅▅'
        
           
        if not(self.state.is_monkey_up):
            if self.state.box_position == 0:
                level_0[1] = '🐒'
            else:
                level_0[0] = '🐒'
        
        box_top =    ["─" * self.room_size * 2]
        box_bottom = ['─' * self.room_size * 2]
        
        box_top =    ['┌'] + box_top +    ['┐']
        level_2 =    ['|'] + level_2 +    ['|']
        level_1 =    ['|'] + level_1 +    ['|']
        level_0 =    ['|'] + level_0 +    ['|']
        box_bottom = ['└'] + box_bottom + ['┘']

        print('\n')
        print('   ', ''.join(box_top))
        print('   ', ''.join(level_2))
        print('   ', ''.join(level_1))
        print('   ', ''.join(level_0))
        print('   ', ''.join(box_bottom))
        print('\n')
    
    
    def performance(self):
        return self.score
    
    
    def available_actions(self):
        if self.state.is_monkey_up:
            return [MonkeyBananaAction.GO_DOWN, 
                    MonkeyBananaAction.GRAB]
        else:
            return [MonkeyBananaAction.MOVE_BOX_LEFT, 
                    MonkeyBananaAction.MOVE_BOX_RIGHT,
                    MonkeyBananaAction.GRAB,
                    MonkeyBananaAction.CLIMB]
    
    
    
    def perform_action(self, action: MonkeyBananaAction):
        if action == MonkeyBananaAction.GRAB:
            if self.state.is_monkey_up and self._is_box_under_banana():
                self.score += GRAB_BANANA_REWARD
                return True
            else:
                self.score -= ACTION_PENALTY
            
        elif action == MonkeyBananaAction.CLIMB:
            self.score -= ACTION_PENALTY
            self.state.is_monkey_up = True
            
        elif action == MonkeyBananaAction.GO_DOWN:
            self.score -= ACTION_PENALTY
            self.state.is_monkey_up = False
            
        elif action == MonkeyBananaAction.MOVE_BOX_LEFT:
            self.score -= ACTION_PENALTY
            if self.state.box_position > 0:
                self.state.box_position = self.state.box_position - 1
        
        elif action == MonkeyBananaAction.MOVE_BOX_RIGHT:
            self.score -= ACTION_PENALTY
            if self.state.box_position < self.room_size - 1:
                self.state.box_position = self.state.box_position + 1
            
        return False
    
    
    def perceive(self):
        pass
    
    
    
class MonkeyBananaFOEnvironmentTask(MonkeyBananaEnvironmentTask):
    """
    Fully observable environment
    """
    
    def perceive(self):
        """
        In the fully observable environment, the agent observes the whole state
        """
        return self.state
    
    
class MonkeyBananaPOEnvironmentTask(MonkeyBananaEnvironmentTask):
    """
    Partially observable environment
    """
    
    def perceive(self):
        """
        In the partially observable environment, the agent does not observe the 
        position of the banana, but can smell the banana. 
        """
        smells_banana = False
        
        proba_smell =  1 / (1 + SMELL_ALPHA * (self.state.banana_position - self.state.box_position)**2)
        
        if self.state.is_monkey_up and np.random.rand() < proba_smell:
            smells_banana = True
            
            
        return MonkeyBananaPartialObservation(self.state.box_position, 
                                              self.state.is_monkey_up, 
                                              smells_banana)

        

