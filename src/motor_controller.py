from gpiozero import Servo, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep

class DRCMotorController:
    def __init__(self, motorPin, servoPin):
        Device.pin_factory = RPiGPIOFactory()
        # GPIO13 - MOTOR & GPIO12 - SERVO preferable
        self.motor = Servo(motorPin, min_pulse_width=1/1000, max_pulse_width=2/1000)
        self.servo = Servo(servoPin, min_pulse_width=1/1000, max_pulse_width=2/1000)



    def setDrivingMotor(self, speed):
        """
        Speed: -1 (reverse full) to 0 (neutral) to 1 (forwards full)
        """
        self.motor.value = max(0, min(1, speed))

    def setServoMotor(self, angle):
        """
        Angle: -1 to 1
        """
        if 0 <= angle <= 0.4:
            angle = angle + 0.2

        self.servo.value = max(-1, min(1, angle))

    def off(self):
        self.motor.detach()
        self.servo.detach()

    def on(self):
        # re-attach if needed
        pass  # gpiozero handles reattachment if value is set again


# configure motor controller #
if __name__ == "__main__":
    mcrtl = DRCMotorController(13, 12)
    userin = input("config or test or servo (c/t/s)")
    if (userin == "c"):
        print("Setting Throttle Ranges:")
        mcrtl.setDrivingMotor(speed=0)

        input("Ready? (Neutral)")
        mcrtl.setDrivingMotor(speed=0)

        input("Ready? (Forward)")
        mcrtl.setDrivingMotor(speed=1)

        input("Ready? (Backwards)")
        mcrtl.setDrivingMotor(speed=-1)

        input("Ready? (End)")
        mcrtl.off()
    elif (userin == "s"):
        val = 0.0
        while val >= -1 and val <= 1:
            mcrtl.setServoMotor(angle=val)
            val = float(input("angle: "))
        mcrtl.setServoMotor(angle=0)
        mcrtl.off()
    else:
        val = 0.0
        while val >= 0 and val <= 1:
            mcrtl.setDrivingMotor(speed=val)
            val = float(input("speed: "))
        mcrtl.setDrivingMotor(speed=0)
        mcrtl.off()
    
    
