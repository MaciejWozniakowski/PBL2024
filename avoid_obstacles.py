#!/usr/bin/env python
import sys
import rospy
from sensor_msgs.msg import LaserScan
import math
from geometry_msgs.msg import Twist

publisher = rospy.Publisher('/revised_scan', LaserScan, queue_size=10)
scann = LaserScan()


def count_average_distance_left(datas):
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


def count_average_distance_right(datas):
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


def count_average_distance_ahead(datas):
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
    distance_left = count_average_distance_left(data)
    distance_right = count_average_distance_right(data)  # -1/8 and -3/8
    distance_ahead = count_average_distance_ahead(data)
    max_distance = find_max_distance(data)  # -1/8 and -3/8
    print("max_distance:")
    print(max_distance)
    print("left:")
    print (distance_left)
    print("right:")
    print (distance_right)
    print("ahead:")
    print (distance_ahead)
    move(distance_right, distance_left, distance_ahead, max_distance)


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
    maxx = float('-inf')
    n = len(datas.ranges)
    kat = n/360
    for i in range(n*(-1)/8, n*1/8):
        a = datas.ranges[i-1]
        # print(a, i)
        if a > maxx and a < 10 and i >= -144 and i <= 142 and a is not None:
            maxx = a
    return maxx


class PID(object):
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
            self.time_fn = time_fn
        else:
            import time

            try:
                self.time_fn = time.monotonic
            except AttributeError:
                self.time_fn = time.time

        self.output_limits = output_limits
        self.reset()

        self._integral = _clamp(starting_output, output_limits)

    def __call__(self, input_, dt=None):
        
        if not self.auto_mode:
            return self._last_output

        now = self.time_fn()
        if dt is None:
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError(
                'dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            return self._last_output

        error = self.setpoint - input_
        d_input = input_ - \
            (self._last_input if (self._last_input is not None) else input_)
        d_error = error - \
            (self._last_error if (self._last_error is not None) else error)
        if self.error_map is not None:
            error = self.error_map(error)

        if not self.proportional_on_measurement:
            self._proportional = self.Kp * error
        else:
            self._proportional -= self.Kp * d_input

        self._integral += self.Ki * error * dt
        self._integral = _clamp(self._integral, self.output_limits)

        if self.differential_on_measurement:
            self._derivative = -self.Kd * d_input / dt
        else:
            self._derivative = self.Kd * d_error / dt

        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        self._last_output = output
        self._last_input = input_
        self._last_error = error
        self._last_time = now

        return output


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


def move(distance_right, distance_left, distance_ahead, odl_max):
    pid = PID(5, 1, 0.15, setpoint=odl_max)
    delta = 0.1
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    twist = Twist()
    twist.linear.x = 0.6
    

    if twist.angular.z >15:
        twist.angular.z = 15
    if twist.angular.z < -15:
        twist.angular.z = -15

    if distance_right > distance_left:
        twist.angular.z = -pid(distance_ahead)
    elif distance_right < distance_left:
        twist.angular.z = pid(distance_ahead)

    if abs(distance_left - distance_right) <= delta:
        twist.angular.z = 0

    if distance_ahead <= 0.5:
        twist.linear.x = -0.2
        twist.angular.z = 0

 #   if distance_left < 0.25:
#	twist.angular.z = pid(distance_ahead)
 #   if distance_right < 0.25:
#	twist.angular.z = -pid(distance_ahead)


 #   if distance_ahead <= 0.4 and distance_right <=0.5:
#	twist.linear.x = -0.2
#	twist.angular.z = 0
	#twist.angular.z = -pid(distance_ahead)
    #elif distance_right <=0.25:
	#twist.linear.x = 0.1
	#twist.angular.z = pid(distance_ahead)
	


  ##  if distance_ahead <= 0.4 and distance_left <=0.5:
#	twist.linear.x = -0.2
#	twist.angular.z = 0
	#twist.angular.z = pid(distance_ahead)
    #elif distance_left <=0.25:
	#twist.linear.x = 0.1
	#twist.angular.z = -pid(distance_ahead)
 
    print("twist:")
    print(twist.angular.z)
    

    pub.publish(twist)


def main(args):
    dane()


if __name__ == '__main__':
    main(sys.argv)
