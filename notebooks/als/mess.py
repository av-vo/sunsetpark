import numpy as np
import pandas as pd

def get_points_by_time_brute_force(pcloud, t, tolerance = 1/1e6):
    full_idx = np.arange(len(pcloud))
    if isinstance(t, list):
        mask = (pcloud.gps_time >= t[0]) & (pcloud.gps_time < t[1])
    else:
        diff =  np.abs(pcloud.gps_time - t)
        diff_min = np.min(diff)
        if diff_min > tolerance:
            return None
        mask = diff == diff_min
    
    idx = full_idx[mask]
    
    x = pcloud.get_x_scaled()
    y = pcloud.get_y_scaled()
    z = pcloud.get_z_scaled()
    
    result = pd.DataFrame( 
        {
            'point' : [pcloud[i] for i in idx],
            'x' : [x[i] for i in idx],
            'y' : [y[i] for i in idx],
            'z' : [z[i] for i in idx]
        }, index = idx
    )
           
    return result