from leotoolbox.signalsfunc import *
import numpy as np

data = np.array([6, 7, 7, 12, 13, 13, 15, 16, 19, 22])

def test_zscore():
    assert np.round(np.sum(z_score(data))) == np.round(np.sum(np.array(
        [-1.394, -1.195, -1.195, -0.199, 0, 0, 0.398, 0.598, 1.195, 1.793])))

def test_find_nearest():
    assert find_nearest(data, 1) == 0
