import machine


def main():
    motor_speed_pot = machine.ADC(26)
    motor_control = machine.PWM(machine.Pin(16))
    motor_control.freq(500)

    while True:
        motor_control.duty_u16(motor_speed_pot.read_u16())
