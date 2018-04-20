from matplotlib import pyplot as plt, animation, style
import numpy as np
from collections import namedtuple
import math

# Point data structure
_point = np.zeros(4, dtype=[("x", "i2"),
                           ("y", "i2"),
                           ("fuel", "i2"),
                           ("h_speed", "i2"),
                           ("v_speed", "i2"),
                           ("rotation", "i1"),
                           ("power", "u1")
                           ])

# _point[0] = (2500,2500,550,0,0,0,0)
print(_point)
print("*"*50)


Point = namedtuple('Point', ["x", "y", "fuel", "h_speed", "v_speed", "rotation", "power"])
init_point = Point(2500, 2500, 550, 0, 0, 0, 0)


def animate(i):
    y_text = 2900
    data = open("data.txt").read()
    plt.cla()
    for inputs in data.split("|"):
        point = init_point
        xs, ys, point_data = input(point, inputs)
        data = point_data[-1]
        output = "x: {:.0f} | y: {:.0f} | hs:{:.2f} | vs: {:.2f} | rot:{} | fuel:{}".format(data.x, data.y,
                                                                                            data.h_speed,
                                                                                            data.v_speed,
                                                                                            data.rotation,
                                                                                            data.fuel)

        line = 'go-'
        if abs(data.h_speed) > 20 or abs(data.v_speed) > 40 or data.fuel < 0:
            line = "ro-"
        plt.plot(xs, ys, line)
        plt.plot([0, 7000], [150, 150])
        plt.annotate(output, xy=(20, y_text), xycoords='data', fontsize=8)
        plt.xlim(0, 7000)
        plt.ylim(0, 3000)
        y_text -= 50


def input(point, inputs):
    points = []
    xs = []
    ys = []
    coordinates = np.zeros(shape=[2, 8], dtype=np.int8)
    previous_point = point
    points.append(init_point)
    xs.append(init_point.x)
    ys.append(init_point.y)
    power = 0

    # Lit les inputs
    # inputs = open("data.txt").read()
    # Pour chaque input
    for line in inputs.split():
        if len(line) > 1:
            target_rotation, target_power, delta_time = list(map(int, line.split(',')))
        else:
            break

        # Calcul de la position après que rotation/power aient été appliqués pendant dt
        for i in range(delta_time):
            # Hack pour le changement d'angle de max(abs(15)) et de power de max(abs(1))
            delta_power = target_power - previous_point.power
            if delta_power != 0:
                power = previous_point.power + 1 if delta_power > 0 else previous_point.power - 1
                # power += delta_power / abs(delta_power)

            # TODO: trouver un hack pour la rotation
            rotation = target_rotation
            # Calcul la position (et les autres infos) pour chaque triplets rotation/power/dt dans la liste des inputs
            point = compute_point_data(previous_point, rotation, power, 1)
            previous_point = point
        points.append(point)
        xs.append(point.x)
        ys.append(point.y)
    # Calcul de la trajectoire finale à partir du dernier input
    while 150 < point.y < 3000 and 0 < point.x < 7000 and point.fuel > 0:
        point = compute_point_data(previous_point, point.rotation, point.power, 1)
        previous_point = point
    points.append(point)
    xs.append(point.x)
    ys.append(point.y)

    return xs, ys, points


def compute_point_data(previous_point, rotation, power, delta_time):
    fuel = previous_point.fuel - (power * delta_time)

    v_acc = math.cos(math.radians(-rotation)) * power - 3.711
    h_acc = math.sin(math.radians(-rotation)) * power
    v_speed = (previous_point.v_speed + (v_acc * delta_time))
    h_speed = previous_point.h_speed + (h_acc * delta_time)

    x = previous_point.x + (delta_time * ((h_speed + previous_point.h_speed) / 2))
    y = previous_point.y + (delta_time * ((v_speed + previous_point.v_speed) / 2))

    return Point(x=x, y=y, fuel=fuel, rotation=rotation, power=power, h_speed=h_speed, v_speed=v_speed)


fig = plt.figure()
plt.xlim(0, 7000)
plt.ylim(0, 3000)
# ax = fig.add_subplot(111)
# ax.set_autoscale_on(False)
#
anim = animation.FuncAnimation(fig, animate, interval=1000)
# ax.set_xbound(lower =0, upper=7000)
# ax.set_xbound(lower =0, upper=7000)
plt.show()

