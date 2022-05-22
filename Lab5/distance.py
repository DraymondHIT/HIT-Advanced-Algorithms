import numpy as np 

def l2(u, v):
    return np.linalg.norm(u - v)

def jaccard(u, v):
    return len(u & v) / len(u | v) 
