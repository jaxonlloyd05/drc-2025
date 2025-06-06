from gpiozero import Servo, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep

servoRanges = [

]

class DRCMotorController:
    def __init__(self, motorPin, servoPin):
        Device.pin_factory = RPiGPIOFactory()
        # GPIO13 - MOTOR & GPIO12 - SERVO preferable
        self.motor = Servo(motorPin, min_pulse_width=1/1000, max_pulse_width=2/1000)
        self.servo = Servo(servoPin, min_pulse_width=1/1000, max_pulse_width=2/1000)

        for i in range(-10, 11):
            self.motor.value = i / 10
            print(i / 10)
            sleep(1)



    def setDrivingMotor(self, speed):
        """
        Speed: -1 (reverse full) to 0 (neutral) to 1 (forwards full)
        """
        self.motor.value = max(0, min(1, speed))

    def setServoMotor(self, angle):
        """
        Angle: -1 to 1
        """
        self.servo.value = max(-1, min(1, angle))

    def off(self):
        self.motor.detach()
        self.servo.detach()

    def on(self):
        # re-attach if needed
        pass  # gpiozero handles reattachment if value is set again
