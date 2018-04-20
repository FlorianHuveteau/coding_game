import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time


class GameWindow:

    def __init__(self, ship):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes(
            [0.1, 0.22, 0.8, 0.7],
            xlim=(0, 7000),
            ylim=(0, 3000))
        self.ship_gizmo, = self.ax.plot(ship.x, ship.y, 'bo', ms=6)
        self.ui = Ui(self.ax)
        # Holds ship state @ every turn
        self.record = []

    def init(self):
        """
        function nécessaire pour blint ou je sais pas quoi
        """
        self.ship_gizmo.set_data(0, 0)

    def draw(self, ship):
        """

        :param terrain:
        :param ship:
        :return:
        """
        elapsed_time = 0
        sum_dt = 0
        prev = time()

        def animate(i):
            """
            update scene
            :param i: frame number
            """
            nonlocal elapsed_time, prev, sum_dt
            now = time()
            dt = now - prev
            sum_dt += dt
            prev = now
            elapsed_time += dt
            ship.update(dt)
            if sum_dt >= 0.9999:
                sum_dt = 0
                ship.rotation = self.ui.slider_rotation.val
                ship.power = self.ui.slider_power.val
                self.record.append(ship)

            self.ui.update(ship, elapsed_time)
            ship.update(dt)
            self.ship_gizmo.set_data(ship.x, ship.y)
            return self.ship_gizmo,

        self.ui.update(ship, elapsed_time)
        ani = animation.FuncAnimation(self.fig, animate, interval=50)
        plt.show()

    def terrain(self, terrain):
        x, y = zip(*terrain)
        self.ax.plot(x, y)


class Ui:

    def __init__(self, ax):
        self.time_lbl = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        self.power_lbl = ax.text(0.02, 0.90, '', transform=ax.transAxes)
        self.rotation_lbl = ax.text(0.02, 0.85, '', transform=ax.transAxes)
        self.hs_lbl = ax.text(0.02, 0.80, '', transform=ax.transAxes)
        self.vs_lbl = ax.text(0.02, 0.75, '', transform=ax.transAxes)
        self.fuel_lbl = ax.text(0.02, 0.70, '', transform=ax.transAxes)
        # BUTTONS
        # TODO: Reset
        # TODO: run,pause, next/prev frame
        # SLIDERS
        ax_power = plt.axes([0.2, 0.02, 0.5, 0.02])
        ax_rotation = plt.axes([0.2, 0.08, 0.5, 0.02])
        self.slider_power = plt.Slider(ax_power, 'Power', valmin=0, valmax=4, valinit=0, valstep=1)
        self.slider_rotation = plt.Slider(ax_rotation, 'Rotation', valmin=-90, valmax=90, valinit=0, valstep=1)


    def update(self, ship, elapsed_time):
        """
        This function update UI every frame
        :param ship:
        :param elapsed_time:
        :return:
        """
        self.time_lbl.set_text("time: {:.2f} s".format(elapsed_time))
        self.hs_lbl.set_text("hs: {:.2f}".format(ship.h_speed))
        self.vs_lbl.set_text("vs: {:.2f}".format(ship.v_speed))
        self.power_lbl.set_text("power: {}".format(ship.power))
        self.rotation_lbl.set_text("rotation: {}".format(ship.rotation))
        self.fuel_lbl.set_text("fuel: {:.0f} l".format(ship.fuel))
