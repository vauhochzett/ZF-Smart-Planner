import pandas as pd
from collections import namedtuple
import numpy as np


class ZFDataHandler:
    def __init__(self):
        self.ZF_DATA = pd.read_csv("../Data/Export_data_ZF_ts.csv")
        self.ZF_KEYS = namedtuple("ZF_KEYS", self.ZF_DATA.keys())
        self.KEYS = self.ZF_KEYS( **{k:k for k in self.ZF_DATA.keys()} )

        categorical_columns = [
            'DriverID', 'VehicleID', 'VehicleSegmentID', 'TripID', 'Driver_Cluster', 'Trip_Cluster',
            'TotalFuel', 'TimeGear13_norm', 'TimeGear15_norm', 'TimeGear16_norm',
            'start', 'name', 'plate']  # 'TotalDistance', 'TimeDriving'

        time_gear = [k for k in list(self.KEYS) if "TimeGear" in k]



    def generate_timestamps_(self, driver_zf_data):
        current_time = pd.Timestamp.now()
        driver_zf_start = []
        for i in driver_zf_data['TimeDriving'].iloc[::-1]:
            current_time -= pd.Timedelta(i, unit='s')
            noise = pd.Timedelta( np.random.randn(1)[0] * 2, unit='s' )
            current_time = current_time - pd.Timedelta(i, unit='s') + noise - pd.Timedelta(1, unit='d')
            driver_zf_start.append(str(current_time))

        return driver_zf_start[::-1]


    def get_best_avgs(self, attributes, group_by, normalize=True, weights = None):
        ZF_DATA = self.ZF_DATA
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


    def get_vehicle(self, selection_criteria, weights=None):
        best_id = self.get_best_avgs(selection_criteria, group_by=self.KEYS.VehicleID, weights=weights)
        return best_id

    def get_driver(self, selection_criteria, weights=None):
        best_id = self.get_best_avgs(selection_criteria, group_by=self.KEYS.DriverID, weights=weights)
        return best_id

    def get_best_avgs(self, attributes, group_by, normalize=True, weights=None):
        ZF_DATA = self.ZF_DATA
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

        return avg_values.keys()[avg_values.argmax()]

    def get_vehicle(self, selection_criteria, weights=None):
        #     selection_criteria = [KEYS.AvgFuelConsumption_per100km, KEYS.TotalDistance]
        best_id = self.get_best_avgs(selection_criteria, group_by=self.KEYS.VehicleID, weights=weights)
        return best_id

    def get_driver(self, selection_criteria, weights=None):
        best_id = self.get_best_avgs(selection_criteria, group_by=self.KEYS.DriverID, weights=weights)
        return best_id

    def get_feature(key, id_, df):
        return df[df[key] == id_].mean()

    def get_user_feat(self, user_id):
        return self.pca_user.transform(
            self.user_trunc_data_normalized_aggregated[self.user_trunc_data_normalized_aggregated.index == user_id])

    def get_vehicle_drivers(self, vehicle_id):
        return list(set(self.select_vehicle(vehicle_id)['DriverID']))

    def get_expected_avgfuel100(self, selected_driver_id, vehicle_id):
        driver_ids = self.get_vehicle_drivers(vehicle_id)

        driver_feat = np.concatenate([self.get_user_feat(driver_id) for driver_id in driver_ids])
        selected_driver_feat = self.get_user_feat(selected_driver_id)

        similarity = ([pearsonr(selected_driver_feat[0], vehicle_driver_feat)[0] for vehicle_driver_feat in driver_feat])
        similarity_sum = sum(similarity)

        expected_avgfuel100 = 0
        for driver_id, sim in zip(driver_ids, similarity):
            mask = (self.ZF_DATA[self.KEYS.DriverID] == driver_id) & (
                        self.ZF_DATA[self.KEYS.VehicleID] == vehicle_id)
            expected_avgfuel100 += sim * self.ZF_DATA_timestamped['AvgFuelConsumption_per100km'][mask].mean()

        return expected_avgfuel100 / similarity_sum



