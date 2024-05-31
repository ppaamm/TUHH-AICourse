from typing import Dict, Set, List
from itertools import product
import time

def parenthesis(string):
    return "(" + string + ")"


class Sentence:
    
    def __init__(self):
        self.name = ""
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def value(interpretation: Dict[str, bool]) -> bool:
        pass
    
    def variables(self) -> Set[str]:
        pass
    
    def get_models(self) -> List[Dict[str, bool]]:
        models = []
        variables = self.variables()
        n_variables = len(variables)
        
        for config in product((True, False), repeat=n_variables):
            interpretation = dict(zip(variables, config))
            if self.value(interpretation): models.append(interpretation)
        return models
    
    
    def is_tautology(self) -> bool:
        # TODO: Question 4
        return False
    


class sVariable(Sentence):
    def __init__(self, name: str):
        self.name = name
    
    def value(self, interpretation: Dict[str, bool]) -> bool:
        return interpretation[self.name]
    
    def variables(self) -> Set[str]:
        return { self.name }



class sNeg(Sentence):
    def __init__(self, s: Sentence):
        self.name = parenthesis("not " + s.name)
        self.s = s
        
    def value(self, interpretation: Dict[str, bool]) -> bool:
        return not(self.s.value(interpretation))
    
    def variables(self) -> Set[str]:
        return self.s.variables()



class CompoundSentence(Sentence):
    def __init__(self, s1: Sentence, s2: Sentence):
        self.s1 = s1
        self.s2 = s2
        
    def variables(self) -> Set[str]:
        return self.s1.variables().union(self.s2.variables())


class sOr(CompoundSentence):
    def __init__(self, s1: Sentence, s2: Sentence):
        super().__init__(s1, s2)
        self.name = parenthesis(s1.name + " or " + s2.name)

    def value(self, interpretation: Dict[str, bool]) -> bool:
        return self.s1.value(interpretation) or self.s2.value(interpretation)
    

class sAnd(CompoundSentence):
    def __init__(self, s1: Sentence, s2: Sentence):
        super().__init__(s1, s2)
        self.name = parenthesis(s1.name + " and " + s2.name)

    def value(self, interpretation: Dict[str, bool]) -> bool:
        return self.s1.value(interpretation) and self.s2.value(interpretation) 
    

class sImplies(CompoundSentence):
    def __init__(self, s1: Sentence, s2: Sentence):
        super().__init__(s1, s2)
        self.name = parenthesis(s1.name + " -> " + s2.name)

    def value(self, interpretation: Dict[str, bool]) -> bool:
        return not(self.s1.value(interpretation)) or self.s2.value(interpretation)
    
class sIfOnlyIf(CompoundSentence):
    def __init__(self, s1: Sentence, s2: Sentence):
        super().__init__(s1, s2)
        self.name = parenthesis(s1.name + " <-> " + s2.name)

    def value(self, interpretation: Dict[str, bool]) -> bool:
        return self.s1.value(interpretation) == self.s2.value(interpretation)
    

class sDisjunction(Sentence):
    def __init__(self, S: List[Sentence]):
        self.S = S
        self.name = parenthesis(" or ".join([s.name for s in self.S]))
        
    def variables(self) -> Set[str]:
        return set.union(*[s.variables() for s in self.S])
    
    def value(self, interpretation: Dict[str, bool]) -> bool:
        return any([s.value(interpretation) for s in self.S])

    
class sConjunction(Sentence):
    def __init__(self, S: List[Sentence]):
        self.S = S
        self.name = parenthesis(" and ".join([s.name for s in self.S]))
        
    def variables(self) -> Set[str]:
        return set.union(*[s.variables() for s in self.S])
    
    def value(self, interpretation: Dict[str, bool]) -> bool:
        return all([s.value(interpretation) for s in self.S])



##############################################################################


def bruteForceSAT(sentence: Sentence) -> Dict[str, bool]:
    variables = sentence.variables()
    n_variables = len(variables)
    
    for config in product((True, False), repeat=n_variables):
        interpretation = dict(zip(variables, config))
        if sentence.value(interpretation): return interpretation
    return dict()



def entails(s1: Sentence, s2: Sentence) -> bool:
    # TODO: Question 6
    # Implementation of the enumeration method
    return True
    









