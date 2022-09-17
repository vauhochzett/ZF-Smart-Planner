import random
import pandas as pd
from collections import namedtuple

ZF_KEYS = namedtuple("ZF_KEYS", ZF_DATA.keys())
KEYS = ZF_KEYS( **{k:k for k in ZF_DATA.keys()} )
ZF_DATA = pd.read_csv("Data/Export_data_ZF_ts.csv")


def generate_timestamps_(driver_zf_data):
    current_time = pd.Timestamp.now()
    driver_zf_start = []
    for i in driver_zf_data['TimeDriving'].iloc[::-1]:
        current_time -= pd.Timedelta(i, unit='s')
        noise = pd.Timedelta( np.random.randn(1)[0] * 2, unit='s' )
        current_time = current_time - pd.Timedelta(i, unit='s') + noise - pd.Timedelta(1, unit='d')
        driver_zf_start.append(str(current_time))

    return driver_zf_start[::-1]


def get_best_avgs(attributes, group_by, normalize=True, weights = None):
    if normalize:
        normalized_attributes = (ZF_DATA[attributes] - ZF_DATA[attributes].mean()) / ZF_DATA[attributes].std()
    else:
        normalized_attributes = ZF_DATA[attributes].copy()
        
    for i, k in enumerate(attributes):
        if weights is not None:
            normalized_attributes[k] = normalized_attributes[k] * weights[i]
            
    normalized_attributes['ACC'] = normalized_attributes.sum(axis=1)
    normalized_attributes[group_by] = ZF_DATA[group_by]
    
    avg_values = normalized_attributes.groupby(group_by)['ACC'].mean()
    
    return avg_values.keys()[avg_values.argmax() ]


def get_vehicle(selection_criteria, weights=None):
    best_id = get_best_avgs(selection_criteria, group_by=KEYS.VehicleID, weights=weights)
    return best_id

def get_driver(selection_criteria, weights=None):
    best_id = get_best_avgs(selection_criteria, group_by=KEYS.DriverID, weights=weights)
    return best_id


