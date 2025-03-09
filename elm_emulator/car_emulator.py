import numpy as np


class Car:
    RPM = (800, 6000)
    SPEED = (0, 250)  # Max speed in km/h
    BRAKE_FORCE = 5000  # Maximum braking force in N
    DRAG_COEFFICIENT = 0.32
    FRONTAL_AREA = 2.2  # in square meters
    AIR_DENSITY = 1.225  # kg/m^3
    CAR_MASS = 1500  # kg
    GEAR_RATIOS = [3.5, 2.8, 2.0, 1.5, 1.0, 0.8]
    FINAL_DRIVE_RATIO = 3.42
    WHEEL_RADIUS = 0.3  # in meters

    def __init__(self):
        self.rpm = self.RPM[0]
        self.speed = self.SPEED[0]
        self.throttle_position = 0
        self.brake_position = 0
        self.gear = 1
        self.engine_temp = 70
        self.database = {
            "rpm": self.rpm,
            "speed": self.speed,
            "engine_temp": self.engine_temp,
        }

    def update(self, throttle_position, brake_position):
        self.throttle_position = throttle_position
        self.brake_position = brake_position
        self.update_rpm()
        self.update_speed()
        self.update_engine_temp()
    def update_engine_temp(self):
        """Simulate engine temperature changes based on throttle and brake inputs. """
        # Increase temperature with throttle input
        if self.throttle_position > 0:
            self.engine_temp += self.throttle_position * 0.1

        # Decrease temperature with brake input
        if self.brake_position > 0:
            self.engine_temp -= self.brake_position * 0.05

        # Clamp temperature to realistic bounds (e.g., 40°C to 120°C)
        self.engine_temp = max(40, min(self.engine_temp, 120))

    def get_engine_temp(self):
        return self.engine_temp

    def update_rpm(self):
        max_torque = 400  # Max torque in Nm
        torque = max_torque * np.sin(np.pi * (self.rpm - self.RPM[0]) / (self.RPM[1] - self.RPM[0]))

        # Update RPM based on throttle position and torque
        self.rpm += (self.throttle_position * torque) / (
                    self.GEAR_RATIOS[self.gear - 1] * self.FINAL_DRIVE_RATIO * self.WHEEL_RADIUS)
        self.rpm = min(max(self.rpm, self.RPM[0]), self.RPM[1])

    def update_speed(self):
        # Calculate the engine power based on RPM and throttle position
        max_power = 200  # Max power in kW
        power = max_power * (self.rpm / self.RPM[1]) * self.throttle_position  # Power in kW

        # Convert power to force (assuming 100% efficiency for simplicity)
        force = (power * 1000) / (self.speed / 3.6 + 0.1)  # Force in N

        # Calculate drag force
        drag_force = 0.5 * self.DRAG_COEFFICIENT * self.FRONTAL_AREA * self.AIR_DENSITY * (self.speed / 3.6) ** 2

        # Calculate braking force
        brake_force = self.brake_position * self.BRAKE_FORCE

        # Calculate acceleration
        net_force = force - drag_force - brake_force
        acceleration = net_force / self.CAR_MASS

        # Update speed
        self.speed += acceleration * 3.6  # Convert m/s^2 to km/h
        self.speed = min(max(self.speed, self.SPEED[0]), self.SPEED[1])

        # Update gear based on speed
        self.update_gear()

    def update_gear(self):
        # Simple gear shifting logic based on speed
        if self.speed > 20 and self.gear < 6:
            self.gear += 1
        elif self.speed < 10 and self.gear > 1:
            self.gear -= 1
