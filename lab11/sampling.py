import numpy as np



def _sampleBurglaryOne():
    # Burglary:
    b = (np.random.rand() < 0.001)
    
    # Earthquake:
    e = (np.random.rand() < 0.002)
    
    # Alarm:
    if b:
        if e: a = np.random.rand() < 0.95
        else: a = np.random.rand() < 0.94
    else:
        if e: a = np.random.rand() < 0.29
        else: a = np.random.rand() < 0.001
        
    # John:
    if a: j = np.random.rand() < 0.9
    else: j = np.random.rand() < 0.05
    
    # Mary:
    if a: m = np.random.rand() < 0.7
    else: m = np.random.rand() < 0.01
    
    
    return {'burglary': b,
            'earthquake': e,
            'alarm': a, 
            'JohnCalls': j,
            'MaryCalls': m
            }


def sampleBurglaryBN(N):
    return [_sampleBurglaryOne() for _ in range(N)]