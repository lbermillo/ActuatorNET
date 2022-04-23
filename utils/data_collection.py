import utime
import numpy as np
from machine import Pin, PWM, ADC


def calc_error(actual, desired):
    return actual - desired


def calc_velocity(x1, x2, t1, t2):
    # v = dx / dt
    return (x2 - x1) / (t2 - t1)


def calc_power(voltage, current):
    # W = V * i
    return voltage * current


def read_data():
    # TODO: time (t), actual position (theta), desired position (u_theta), and power (W)
    t = utime.time()
    u_theta = None
    theta = None
    voltage = None
    current = None
    power = calc_power(voltage, current)

    return t, u_theta, theta, power


def sample(freq=1/400., data_size=1e6):
    # initialize list to store data
    data = []

    while len(data) < data_size:
        data.append(read_data())

        # sample data at given frequency
        utime.sleep(freq)

    return np.array(data)


if __name__ == "__main__":
    # input (history of inputs t, t-0.01, t-0.02):
    #   -> position errors (theta - u_theta)
    #   -> velocities

    # output
    #   -> torque(N/m)? power(W)

    # hardware needed
    #   -> motor
    #   -> position sensor
    #   -> microcontroller

    # Pico PINS for ADC are GP26, GP27, GP28
    # User needs to specify pins for motor and position sensor
    pos_sensor = ADC(28)
    motor = PWM(PIN(0, Pin.OUT, value=0))
    motor.freq(100000)

    # sample at 400Hz
    # read time (t), actual position (theta), desired position (u_theta), and power (W)
    # calculate position error and velocity
    # log data to a file
    pass
