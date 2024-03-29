#!/usr/bin/env python
import roslib
import sys
import rospy
import cv2 as cv
import time

from sensor_msgs.msg import LaserScan
import sensor_msgs.msg
import math
from geometry_msgs.msg import Twist

import select
import termios
import tty


publisher = rospy.Publisher('/revised_scan', LaserScan, queue_size=10)
scann = LaserScan()



# print("kuba")


def LiczenieSredniejLewo(datas):
    x = 0
    n = len(datas.ranges)
    c_suma = 2
    kat = n/360
    for i in range(n/8, n*2/8):
        a = datas.ranges[i-1]
        b = datas.ranges[i]
        c = b*a*math.sin(math.radians(kat)) / \
            (math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
        if math.isnan(c) == False:
            c_suma = c_suma+c
            x = x+1

    c_avr = c_suma/x
    return c_avr


def LiczenieSredniejPrawo(datas):
    x = 0
    n = len(datas.ranges)
    c_suma = 2
    kat = n/360
    for i in range(n*6/8, n*7/8):
        a = datas.ranges[i-1]
        b = datas.ranges[i]
        c = b*a*math.sin(math.radians(kat)) / \
            (math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
        if math.isnan(c) == False:
            c_suma = c_suma+c
            x = x+1

    c_avr = c_suma/x
    return c_avr


def LiczenieSredniejSrodek(datas):
    x = 1
    n = len(datas.ranges)
    c_suma = 2
    kat = n/360
    for i in range(n*(-1)/20, n*1/20):
        a = datas.ranges[i-1]
        b = datas.ranges[i]
        c = b*a*math.sin(math.radians(kat)) / \
            (math.sqrt(a*a+b*b-2*a*b*math.cos(math.radians(kat))))
        if math.isnan(c) == False:
            c_suma = c_suma+c
            x = x+1
    print(x)
    c_avr = c_suma/x
    return c_avr


def callback(data):
    # n=len(data.ranges)
    x = 1.0/8.0
    odleglosc_lewo = LiczenieSredniejLewo(data)
    odleglosc_prawo = LiczenieSredniejPrawo(data)  # //albo -1/8 i -3/8
    odleglosc_przod = LiczenieSredniejSrodek(data)
    main_maxx = find_max_distance(data)  # // albo -1/8 i -3/8
    print("odleglosc maksymalna:")
    print(main_maxx)
    # print("lewo:")
    # print (odleglosc_lewo)
    # print("prawo:")
    # print (odleglosc_prawo)
    print("przod:")
    print (odleglosc_przod)
    Peide(odleglosc_prawo, odleglosc_lewo, odleglosc_przod, main_maxx)


def dane():
    rospy.init_node('revised_scan', anonymous=True)
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    rospy.spin()


def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value


def find_max_distance(datas):
    maxx = -99999999
    n = len(datas.ranges)
    kat = n/360
    for i in range(n*(-1)/8, n*1/8):
        a = datas.ranges[i-1]
        # print(a, i)
        if a > maxx and a < 10 and i >= -144 and i <= 142 and a is not None:
            maxx = a
    return maxx


class PID(object):
    """A simple PID controller."""

    def __init__(
        self,
        Kp=1.0,
        Ki=0.0,
        Kd=0.0,
        setpoint=0,
        sample_time=0.01,
        output_limits=(None, None),
        auto_mode=True,
        proportional_on_measurement=False,
        differential_on_measurement=True,
        error_map=None,
        time_fn=None,
        starting_output=0.0,
    ):
        """
        Initialize a new PID controller.
        :param Kp: The value for the proportional gain Kp
        :param Ki: The value for the integral gain Ki
        :param Kd: The value for the derivative gain Kd
        :param setpoint: The initial setpoint that the PID will try to achieve
        :param sample_time: The time in seconds which the controller should wait before generating
            a new output value. The PID works best when it is constantly called (eg. during a
            loop), but with a sample time set so that the time difference between each update is
            (close to) constant. If set to None, the PID will compute a new output value every time
            it is called.
        :param output_limits: The initial output limits to use, given as an iterable with 2
            elements, for example: (lower, upper). The output will never go below the lower limit
            or above the upper limit. Either of the limits can also be set to None to have no limit
            in that direction. Setting output limits also avoids integral windup, since the
            integral term will never be allowed to grow outside of the limits.
        :param auto_mode: Whether the controller should be enabled (auto mode) or not (manual mode)
        :param proportional_on_measurement: Whether the proportional term should be calculated on
            the input directly rather than on the error (which is the traditional way). Using
            proportional-on-measurement avoids overshoot for some types of systems.
        :param differential_on_measurement: Whether the differential term should be calculated on
            the input directly rather than on the error (which is the traditional way).
        :param error_map: Function to transform the error value in another constrained value.
        :param time_fn: The function to use for getting the current time, or None to use the
            default. This should be a function taking no arguments and returning a number
            representing the current time. The default is to use time.monotonic() if available,
            otherwise time.time().
        :param starting_output: The starting point for the PID's output. If you start controlling
            a system that is already at the setpoint, you can set this to your best guess at what
            output the PID should give when first calling it to avoid the PID outputting zero and
            moving the system away from the setpoint.
        """
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.sample_time = sample_time

        self._min_output, self._max_output = None, None
        self._auto_mode = auto_mode
        self.proportional_on_measurement = proportional_on_measurement
        self.differential_on_measurement = differential_on_measurement
        self.error_map = error_map

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = None
        self._last_output = None
        self._last_error = None
        self._last_input = None

        if time_fn is not None:
            # Use the user supplied time function
            self.time_fn = time_fn
        else:
            import time

            try:
                # Get monotonic time to ensure that time deltas are always positive
                self.time_fn = time.monotonic
            except AttributeError:
                # time.monotonic() not available (using python < 3.3), fallback to time.time()
                self.time_fn = time.time

        self.output_limits = output_limits
        self.reset()

        # Set initial state of the controller
        self._integral = _clamp(starting_output, output_limits)

    def __call__(self, input_, dt=None):
        """
        Update the PID controller.
        Call the PID controller with *input_* and calculate and return a control output if
        sample_time seconds has passed since the last update. If no new output is calculated,
        return the previous output instead (or None if no value has been calculated yet).
        :param dt: If set, uses this value for timestep instead of real time. This can be used in
            simulations when simulation time is different from real time.
        """
        if not self.auto_mode:
            return self._last_output

        now = self.time_fn()
        if dt is None:
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError(
                'dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            # Only update every sample_time seconds
            return self._last_output

        # Compute error terms
        error = self.setpoint - input_
        d_input = input_ - \
            (self._last_input if (self._last_input is not None) else input_)
        d_error = error - \
            (self._last_error if (self._last_error is not None) else error)

        # Check if must map the error
        if self.error_map is not None:
            error = self.error_map(error)

        # Compute the proportional term
        if not self.proportional_on_measurement:
            # Regular proportional-on-error, simply set the proportional term
            self._proportional = self.Kp * error
        else:
            # Add the proportional error on measurement to error_sum
            self._proportional -= self.Kp * d_input

        # Compute integral and derivative terms
        self._integral += self.Ki * error * dt
        # Avoid integral windup
        self._integral = _clamp(self._integral, self.output_limits)

        if self.differential_on_measurement:
            self._derivative = -self.Kd * d_input / dt
        else:
            self._derivative = self.Kd * d_error / dt

        # Compute final output
        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        # Keep track of state
        self._last_output = output
        self._last_input = input_
        self._last_error = error
        self._last_time = now

        return output

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r}, '
            'setpoint={self.setpoint!r}, sample_time={self.sample_time!r}, '
            'output_limits={self.output_limits!r}, auto_mode={self.auto_mode!r}, '
            'proportional_on_measurement={self.proportional_on_measurement!r}, '
            'differential_on_measurement={self.differential_on_measurement!r}, '
            'error_map={self.error_map!r}'
            ')'
        ).format(self=self)

    @property
    def components(self):
        """
        The P-, I- and D-terms from the last computation as separate components as a tuple. Useful
        for visualizing what the controller is doing or when tuning hard-to-tune systems.
        """
        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):
        """The tunings used by the controller as a tuple: (Kp, Ki, Kd)."""
        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):
        """Set the PID tunings."""
        self.Kp, self.Ki, self.Kd = tunings

    @property
    def auto_mode(self):
        """Whether the controller is currently enabled (in auto mode) or not."""
        return self._auto_mode

    @auto_mode.setter
    def auto_mode(self, enabled):
        """Enable or disable the PID controller."""
        self.set_auto_mode(enabled)

    def set_auto_mode(self, enabled, last_output=None):
        """
        Enable or disable the PID controller, optionally setting the last output value.
        This is useful if some system has been manually controlled and if the PID should take over.
        In that case, disable the PID by setting auto mode to False and later when the PID should
        be turned back on, pass the last output variable (the control variable) and it will be set
        as the starting I-term when the PID is set to auto mode.
        :param enabled: Whether auto mode should be enabled, True or False
        :param last_output: The last output, or the control variable, that the PID should start
            from when going from manual mode to auto mode. Has no effect if the PID is already in
            auto mode.
        """
        if enabled and not self._auto_mode:
            # Switching from manual mode to auto, reset
            self.reset()

            self._integral = last_output if (last_output is not None) else 0
            self._integral = _clamp(self._integral, self.output_limits)

        self._auto_mode = enabled

    @property
    def output_limits(self):
        """
        The current output limits as a 2-tuple: (lower, upper).
        See also the *output_limits* parameter in :meth:`PID.__init__`.
        """
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        """Set the output limits."""
        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if (None not in limits) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        self._last_output = _clamp(self._last_output, self.output_limits)

    def reset(self):
        """
        Reset the PID controller internals.
        This sets each term to 0 as well as clearing the integral, the last output and the last
        input (derivative calculation).
        """
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._integral = _clamp(self._integral, self.output_limits)

        self._last_time = self.time_fn()
        self._last_output = None
        self._last_input = None






def Peide(odl_p, odl_l, odl_przod, odl_max):
    pid = PID(5, 0.7, 0.15, setpoint=odl_max)
    delta = 0.1
    settings = termios.tcgetattr(sys.stdin)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    twist = Twist()

    twist.linear.x = 0.3
    

    if twist.angular.z >20:
        twist.angular.z = 20
    if twist.angular.z < -20:
        twist.angular.z = -20

    if odl_p > odl_l:
        twist.angular.z = -pid(odl_przod)
    else:
        twist.angular.z = pid(odl_przod)

    if abs(odl_l - odl_p) <= delta:
        twist.angular.z = 0

    print(twist.angular.z)
    

   # if odl_przod <= 1 and odl_p <= 1:

    #    twist.linear.x= 0.1

    #if odl_przod <= 1 and odl_l <=1:

     #   twist.linear.x= 0.1

    pub.publish(twist)


def main(args):

    dane()
    print("kuba")


if __name__ == '__main__':
    main(sys.argv)