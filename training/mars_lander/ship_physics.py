import math


class NoMoreFuelException(Exception):
    pass


class ShipPhysics:

    def __init__(self, x, y, h_speed=0, v_speed=0, fuel=500, rotation=0, power=0):
        """

        :param x:
        :param y:
        :param h_speed:
        :param v_speed:
        :param fuel:
        :param rotation:
        :param power:
        """
        self.x = x
        self.y = y
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self._rotation = rotation
        self._power = power
        self.init_state = (x, y, h_speed, v_speed, fuel, rotation, power)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, target_rotation):
        delta_rotation = min(15, max(-15, target_rotation - self._rotation))
        _r = self._rotation + delta_rotation
        self._rotation = min(90, max(_r, -90))

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, target_power):
        # _power = 1 if _power > 1 else -1 if _power < -1 else _power
        delta_power = min(1, max(-1, target_power - self.power))
        _p = self._power + delta_power
        self._power = min(4, max(_p, 0))

    def update(self, delta_time=1):
        """
        Update ship speed and position according requested power and rotation
        :param delta_time:
        """
        self.fuel -= self.power * delta_time
        h_acc = math.sin(math.radians(-self.rotation)) * self.power
        v_acc = math.cos(math.radians(-self.rotation)) * self.power - 3.711
        _t = 0.5 * delta_time * delta_time
        self.x += (self.h_speed * delta_time) + (_t * h_acc)
        self.y += (self.v_speed * delta_time) + (_t * v_acc)
        self.h_speed += h_acc * delta_time
        self.v_speed += v_acc * delta_time

    def __str__(self):
        return "x: {:.0f} m | y: {:.0f} m | fuel: {} l | hs: {:.2f} m/s | vs: {:.2f} m/s" \
            .format(self.x, self.y, self.fuel, self.h_speed, self.v_speed)

# ship = ShipPhysics(x=2500, y=2500, h_speed=0, v_speed=0, fuel=500, rotation=0, power=0)
# for i in range(10):
#     ship.update(-20, 4)
#     print(ship)