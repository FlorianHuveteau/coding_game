import matplotlib.pyplot as plt
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

p0 = Point(80, 80)
p1 = Point(40, 72)
p2 = Point(20, 80)


def bezier_points(points):
    p = lambda a, b, t: Point(b.x + ((a.x - b.x) * t), b.y + ((a.y - b.y) * t))
    xs = [points[-1].x]
    ys = [points[-1].y]
    for i in range(0, len(points) - 2):
        p0, p1, p2 = points[i:i + 3]
        for t in range(2, 10, 2):
            a = p(p0, p1, t / 10)
            b = p(p1, p2, t / 10)
            f = p(a, b, t / 10)
            xs.append(f.x)
            ys.append(f.y)
    xs.append(points[0].x)
    ys.append(points[0].y)
    print(xs, ys)
    return xs, ys


points = [p0, p1, p2]
x = [p.x for p in points]
y = [p.y for p in points]
plt.plot(x, y)
x, y = bezier_points(points)
plt.plot(x, y)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()
