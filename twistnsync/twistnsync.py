"""Main module."""

import numpy as np
import logging

from scipy.signal import correlate as cor
from scipy.interpolate import interp1d, CubicSpline

__all__ = ["TimeSync2_1", "TimeSyncException"]


class TimeSyncException(Exception):
    """
    Base exception for TimeSync class
    """

    def __init__(self, msg):
        self.msg = msg


class TimeSync:
    """
    A class used to get time delay between two clocks by gyroscope measurements
    ...
    Attributes
    ----------
    xx1 : numpy array of shape (N,3)
        3D angular velocities of the first gyro. for N timestamps
    xx2 : numpy array of shape (M,3)
        3D angular velocities of the second gyro. for M timestamps
    t1 : numpy array of shape (N,)
        timestamps of the first gyro. measurements
    t2 : numpy array of shape (N,)
        timestamps of the second gyro. measurements
    do_resample : bool
        flag to do resampling of angular velocities to equal and constant time grids
        If False then timestamps are used only for estimation of sampling period
    Methods
    -------
    #TOBEDONE
    """

    def __init__(
        self,
        xx1,
        xx2,
        t1,
        t2,
        do_resample=True,
    ):
        self.xx1 = xx1
        self.xx2 = xx2
        self.t1 = t1
        self.t2 = t2
        self.do_resample = do_resample
        self.M = None

        self._dt = None
        self._t1_new = None
        self._t2_new = None
        self._xx1_new = None
        self._xx2_new = None

        self._cor = None
        self._time_delay = None

        self._resample_complete = False
        self._calibration_is_succeeded = False

    @staticmethod
    def __interp(t_old, f_old, t_new, kind="cubic"):
        interp_func = interp1d(
            t_old, f_old, kind=kind, axis=0, bounds_error=False, fill_value=(0, 0)
        )
        return interp_func(t_new)

    @property
    def cor(self):
        return self._cor

    @property
    def time_delay(self):
        return self._time_delay

    @property
    def resample_complete(self):
        return self._resample_complete

    @property
    def calibration_is_succeeded(self):
        return self._calibration_is_succeeded

    def _get_initial_index(self):
        x1_temp = np.linalg.norm(self._xx1_new, axis=1)
        x2_temp = np.linalg.norm(self._xx2_new, axis=1)
        cross_cor = cor(x2_temp, x1_temp)
        index_init = np.argmax(cross_cor)
        return cross_cor, index_init

    def _rearrange_data(self, index_init):
        xx1_temp = self._xx1_new
        xx2_temp = self._xx2_new

        if index_init > 0:
            xx1_temp = self._xx1_new[:-index_init]
            xx2_temp = self._xx2_new[index_init:]
        elif index_init < 0:
            xx1_temp = self._xx1_new[-index_init:]
            xx2_temp = self._xx2_new[:index_init]

        size = min(xx1_temp.shape[0], xx2_temp.shape[0])

        return xx1_temp[:size], xx2_temp[:size]

    def __make_calibration(self, xx1_temp, xx2_temp):
        try:
            pseudoinverse = np.linalg.inv(np.matmul(xx1_temp.T, xx1_temp))
        except np.linalg.LinAlgError:
            logging.error(
                "Can't calibrate. Pseudoinverse is not defined. Keeping data the same"
            )
            self._calibration_is_succeeded = False
            return self._calibration_is_succeeded

        self.M = np.matmul(np.matmul(xx2_temp.T, xx1_temp), pseudoinverse)
        self.xx1_new = np.matmul(self.M, self._xx1_new.T).T
        self._calibration_is_succeeded = True

        return self._calibration_is_succeeded

    @staticmethod
    def __get_equation(cross_cor, index_init):
        cubic_spline = CubicSpline(
            np.arange(cross_cor.shape[0]), cross_cor, bc_type="natural"
        )
        coefs = cubic_spline.c[:, index_init]
        order = coefs.shape[0] - 1
        derivative = coefs[-2]

        if derivative < 0:
            index_init -= 1
            coefs = cubic_spline.c[:, index_init]

        return order, coefs

    @staticmethod
    def __calculate_result(order, coefs):
        # Solve qudratic equation to obtain roots
        res = np.roots([(order - i) * coefs[i] for i in range(order)])
        # Choose solution from roots.
        if (
            sum(
                (order - i) * coefs[i] * ((res[0] + res[1]) / 2) ** (order - i - 1)
                for i in range(order)
            )
            < 0
        ):
            res = np.min(res)
        else:
            res = np.max(res)

        return res

    def resample(self, step=None):
        self._dt = step or np.min(
            [np.mean(np.diff(self.t1)), np.mean(np.diff(self.t2))]
        )

        if self.do_resample:
            self._t1_new = np.arange(self.t1[0], self.t1[-1] + self._dt, self._dt)
            self._t2_new = np.arange(self.t2[0], self.t2[-1] + self._dt, self._dt)

            self._xx1_new = self.__interp(self.t1, self.xx1, self._t1_new)
            self._xx2_new = self.__interp(self.t2, self.xx2, self._t2_new)
        else:
            self._t1_new = self.t1
            self._t2_new = self.t2
            self._xx1_new = self.xx1
            self._xx2_new = self.xx2

        self._resample_complete = True

    def obtain_delay(self):
        if not self._resample_complete:
            raise TimeSyncException("resample() has not called yet")

        shift = -self._xx1_new.shape[0] + 1
        cross_cor, index_init = self._get_initial_index()
        index_init += shift

        xx1_temp, xx2_temp = self._rearrange_data(index_init)

        self.__make_calibration(xx1_temp=xx1_temp, xx2_temp=xx2_temp)
        cross_cor, index_init = self._get_initial_index()

        order, coefs = self.__get_equation(cross_cor, index_init)
        result = self.__calculate_result(order, coefs)

        self._cor = cross_cor
        self._time_delay = (index_init + shift + result) * self._dt
