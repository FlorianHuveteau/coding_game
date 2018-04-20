import itertools
import math
import random

MAX_V_SPEED = -40  # ( ≤ 40m/s in absolute value)
MAX_H_SPEED = 20  # ( ≤ 20m/s in absolute value)
DELTA_TIME = 5

# Creating population - Avec random, tu prends le risque d'avoir des valeurs trop disparates dès le départ
_values = itertools.product([e for e in range(-80, 80, 20)], [e for e in range(0, 5)])
population = [{"rotate": e[0], "power": e[1], "fitness": 0} for e in _values]
POPULATION_SIZE = len(population)
min_close = max_close = 0
random.randint
# Hack - TO REMOVE
t = 0
h_speed = v_speed = rotate = power = n_h_speed = n_v_speed = h_acc = v_acc = 0
xx = (0, 800, 1400, 2000, 3200, 4000, 5000, 7000)
yy = (100, 400, 1150, 800, 400, 150, 150, 600)
x = y = 2500
to_print = []


def add_to_print(**kwargs):
    to_print.append(kwargs)


def excel_print(o="fitness", n=POPULATION_SIZE):
    titles = " | ".join(k for k in to_print[0].keys())
    print(titles)
    to_print.sort(key=lambda x: x[o], reverse=True)
    for i in range(n):
        for k, v in to_print[i].items():
            l = len(k)
            print("{0:>{1}.{1}s} | ".format(str(v), l), end="")
        print()


def fitness(entity):
    dx = target_x - x
    dy = target_y - y
    # Horizontal acceleration
    h_acc = math.sin(math.radians(-entity["rotate"])) * entity["power"]
    v_acc = math.cos(math.radians(-entity["rotate"])) * entity["power"] - 3.711
    # speed after DELTA_TIME if acceleration remain constant
    h_speed_dt = h_speed + (h_acc * DELTA_TIME)
    v_speed_dt = v_speed + (v_acc * DELTA_TIME)
    # Horizontal displacement if acceleration remain constant
    dx_in_dt = (h_speed_dt + h_speed) * 0.5 * DELTA_TIME
    dy_in_dt = (v_speed_dt + v_speed) * 0.5 * DELTA_TIME
    # Does the spaceship is getting closer to its target
    close_x = 1 - abs((dx - dx_in_dt) / (dx + 1))
    close_y = 1 - abs((dy - dy_in_dt) / (dy + 1))
    close_x = 1 / (1 + math.exp(-close_x))
    close_y = 1 / (1 + math.exp(-close_y))
    # Does acceleration lead to a too high vertical speed ?
    max_h = math.log(((abs(dx)) / 500) + 1, 10) * (MAX_H_SPEED ** 1.4)
    max_v = math.log(abs(dy / 1000) + 1, 10) * 50 + 20

    h_speed_limiter =  (((max_h - (h_speed_dt)) / max_h))
    v_speed_limiter = 1 - ((abs(max_v - abs(v_speed_dt)) / max_v))

    h_speed_limiter = 1 / (1 + math.exp(-h_speed_limiter))
    v_speed_limiter = 1 / (1 + math.exp(-v_speed_limiter))

    fitness = (close_x * close_y) * (v_speed_limiter) * h_speed_limiter
    add_to_print(rota=entity["rotate"],
                 po=entity["power"],
                 fitness=fitness,
                 dx_dt=dx_in_dt,
                 close_x=close_x,
                 h_acc=h_acc,
                 dy_dt=dy_in_dt,
                 # nxt_dy=dy - dy_in_dt,
                 close_y=(close_y),
                 hs_dt=int(h_speed_dt),
                 vs_dt=int(v_speed_dt),
                 max_h=int(max_h),
                 max_v=(max_v),
                 h_lim=h_speed_limiter,
                 v_lim=v_speed_limiter
                 )
    return fitness


# FOR TESTING PURPOSE
h_speed = 4
v_speed = 0
x = 2000
y = 2300
target_x = 4500
target_y = 200
for e in population:
    e["fitness"] = fitness(e)
chief = max(population, key=lambda e: e["fitness"])
print(target_x - x, "|", target_y - y, "|", h_speed, "|", v_speed)
print(chief)
excel_print(o="fitness")


# test = [(0, 0, 2500, 2500),
#         (80, 0, 2500, 2500),
#         (-30, -20, 3800, 900),
#         (30, 20, 4500, 500),
#         ]
# for t in test:
#     h_speed, v_speed, x, y = t
#     # print("h_speed: {}, v_speed: {}, x: {}, y: {}".format(h_speed, v_speed,x,y))
#     print(t)
#     for e in population:
#         e["fitness"] = fitness(e)
#     chief = max(population, key=lambda e: e["fitness"])
#     print(chief)
#     excel_print()
#     print()

def pid():
    # http://brettbeauregard.com/blog/2011/04/improving-the-beginner%e2%80%99s-pid-derivative-kick/
    pass


def mutate(population):
    # TODO: mutation en fonction de fitness
    _population = list(population)
    _sample = random.sample(range(POPULATION_SIZE), k=random.randrange(0, POPULATION_SIZE))
    for i in _sample:
        _d = {"rotate": random.randint(-90, 90), "power": random.randint(0, 4), "fitness": 0}
        population[i] = _d
    return population


def crossover(population):
    max_rotate = -91
    min_rotate = 91
    max_power = -1
    min_power = 5
    population.sort(key=lambda e: e.get("fitness"), reverse=True)
    parents = population[:POPULATION_SIZE // 2]
    for e in parents:
        max_rotate = max(e.get("rotate"), max_rotate)
        min_rotate = min(e.get("rotate"), min_rotate)
        max_power = max(e.get("power"), max_power)
        min_power = min(e.get("power"), min_power)
        # print("{:>2} | {} | {:>4}"
        #       .format(e["rotate"],e["power"],e["fitness"]))

    kids = [{"rotate": random.randint(min_rotate, max_rotate),
             "power": random.randint(min_power, max_power),
             "fitness": 0} for i in range(len(population) - POPULATION_SIZE // 2)]
    parents.extend(kids)
    return parents


def game_loop():
    global x, y, h_speed, v_speed, rotate, power
    v_acc = math.cos(math.radians(-rotate)) * power - 3.711
    h_acc = math.sin(math.radians(-rotate)) * power
    n_h_speed = h_speed + h_acc
    n_v_speed = v_speed + v_acc
    x = x + (n_h_speed + h_speed) / 2
    y = y + (n_v_speed + v_speed) / 2
    h_speed = n_h_speed
    v_speed = n_v_speed
    return x, y, h_speed, v_speed, 0, rotate, power


topo = []
_y = -1
_x = 0
for tx, ty in zip(xx, yy):
    # land_x, land_y = [int(j) for j in input().split()]
    topo.append((tx, ty))
    if ty == _y:
        target_y = ty
        target_x = int((tx + _x) / 2)
    _y = ty
    _x = tx

# while y > target_y and t < 200 and x < 7000:
#     t += 1
#     x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in game_loop()]
#
#     for e in population:
#         e["fitness"] = fitness(e)
#
#     if target_y + 150 > y:
#         power = 3 if v_speed < 10 else 4
#         chief = {"rotate": 0, "power": power, "fitness": 1}
#     else:
#         chief = max(population, key=lambda e: e["fitness"])
#     rotate = chief["rotate"]
#     power = chief["power"]
#
#     population = crossover(population)
#     population = mutate(population)
#
#     print("{:>2} | rotate: {:>3} | power: {} | h speed:{:>4} | v speed:{:>4} | x:{:>4} | y:{:>5} |fit:{:4f}"
#           .format(t, rotate, power, int(h_speed), int(v_speed), x, y, chief.get("fitness")))
