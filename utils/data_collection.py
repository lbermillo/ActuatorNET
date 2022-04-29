import utime
from random import randint
from math import sin, radians
from machine import Pin, PWM, ADC


def calc_error(actual, desired):
    return actual - desired


def calc_velocity(x1, x2, t1, t2):
    # v = dx / dt
    return (x2 - x1) / (t2 - t1)


def calc_power(voltage, current):
    # W = V * i
    return voltage * current


# Will return an integer between out_min and out_max (https://forum.micropython.org/viewtopic.php?f=2&t=7615)
def map_values(x, in_min, in_max, out_min, out_max):
    return int(max(min(out_max, (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min), out_min))


def set_motor_position(motor, pos):
    # convert given position in degrees to microseconds and set motor position
    motor.duty_u16(map_values(sin(radians(pos)), in_min=-1, in_max=1, out_min=1000, out_max=9000))


def read_data():
    # TODO: time (t), actual position (theta), desired position (u_theta), and power (W)
    t = utime.time()
    u_theta = None
    theta = None
    voltage = None
    current = None
    power = calc_power(voltage, current)

    return t, u_theta, theta, power


def sample(motor, sample_freq=1/400., data_size=1e6, random_pos=False):
    # initialize list to store data
    data = []

    for step in range(int(data_size)):
        # set the motor position
        set_motor_position(motor, pos=randint(0, 360) if random_pos else step)

        # sample data
        data.append(read_data())

        # sample data at given frequency
        utime.sleep(sample_freq)

    return data


def setup(motor_pin, encoder_pin=None, power_pin=None, motor_freq=50):
    # setup motor
    motor = PWM(Pin(motor_pin), Pin.OUT, value=0)
    motor.freq(motor_freq)

    # setup encoder if provided
    if encoder_pin is not None:
        encoder = ADC(Pin(encoder_pin))

    # TODO: setup power sensor if provided
    power = None

    return motor, encoder, power


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
    # User needs to specify pins for motor, encoder, and power sensor
    motor, _, _ = setup(motor_pin=0)

    # start sampling data
    motor_data = sample(motor)

    # TODO: write data out to file
