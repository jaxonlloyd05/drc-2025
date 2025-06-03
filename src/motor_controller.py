from gpiozero import PWMOutputDevice, Servo, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory

class DRCMotorController:
    def __init__(self, motorPin, servoPin):
        # GPIO13 & GPIO12 preferable
        Device.pin_factory = RPiGPIOFactory()
        # self.motor = PWMOutputDevice(motorPin, frequency=50)
        self.servo = Servo(servoPin) 
        pass

    def setDrivingMotor(self, speed):
        # speed taken in between 0 and 1 - still to decide how to do this
        # self.motor.value = speed
        pass

    def setServoMotor(self, angle):
        # angle from -1 to 1 for servo class
        self.servo.value = angle
        pass

    def off (self):
        self.motor.off()
        self.servo.off()
        pass
    
    def on (self):
        self.motor.on()
        self.servo.on()
        pass


