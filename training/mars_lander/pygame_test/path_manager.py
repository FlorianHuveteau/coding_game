import math

import inspect
import pygame


class PathManager():
    """
    Gère la trajectoire
    """

    def __init__(self, lander_init, terrain_topology):
        # Liste des commandes rotation/power/dt saisies
        self.inputs = list()
        # Liste des points de la trajectoire avec les data correspondantes
        self.points = list()
        # Point de départ du lander qu'on ajoute de suite à la liste des inputs
        self.starting_point = PathManager.PointData(**lander_init)
        # Liste des triplets rotation/power/delta_time permettant de calculer la trajectoire
        input = (lander_init.get("rotation"),
                 lander_init.get("power"),
                 1
                 )
        # On calcul dès le départ la trajectoire à partir du premier point
        self.update(input)

    def update(self, input):
        """
        Ajoute un point à la liste des points de la trajectoire
        Calcul la nouvelle trajectoire
        Le parametre dt dans le tuple input est en secondes
        :param input: dictionnary {rotation: , power: , dt: }
        """
        self.inputs.append(input)
        self.points.clear()

        xs = []
        ys = []

        previous_point = self.starting_point
        point = previous_point

        for input in self.inputs:
            (target_rotation, target_power, dt) = input
            power = previous_point.power
            rotation = previous_point.rotation
            # Calcul de la position après que rotation/power aient été appliqués pendant dt
            for i in range(dt):
                if not (0 < point.y < 3000 and 0 < point.x < 7000 and point.fuel > 0):
                    break
                # Hack pour le changement d'angle de max(abs(15)) et de power de max(abs(1))
                delta_power = target_power - previous_point.power
                if delta_power != 0:
                    power = previous_point.power + 1 if delta_power > 0 else previous_point.power - 1
                    # power += delta_power / abs(delta_power)
                # TODO: trouver un hack pour la rotation
                rotation = target_rotation
                # Calcul la position (et les autres infos) pour chaque triplets rotation/power/dt dans la liste des inputs
                point = self.compute_point_data(previous_point, rotation, power, 1)
                previous_point = point
            self.points.append(point)

        # Tant que le vaisseau sort pas du cadre et a du fuel
        while 0 < point.y < 3000 and 0 < point.x < 7000 and point.fuel > 0:
            # Calcul du point final
            point = self.compute_point_data(previous_point, rotation, power, 1)
            previous_point = point

        self.points.append(point)
        return self.points

    def compute_point_data(self, previous_point, rotation, power, delta_time):

        fuel = previous_point.fuel - (power * delta_time)

        v_acc = math.cos(math.radians(-rotation)) * power - 3.711
        h_acc = math.sin(math.radians(-rotation)) * power
        v_speed = (previous_point.v_speed + (v_acc * delta_time))
        h_speed = previous_point.h_speed + (h_acc * delta_time)

        x = previous_point.x + (delta_time * ((h_speed + previous_point.h_speed) / 2))
        y = previous_point.y + (delta_time * ((v_speed + previous_point.v_speed) / 2))

        return PathManager.PointData(x=x, y=y, power=power, rotation=rotation, fuel=fuel, v_speed=v_speed,
                                     h_speed=h_speed)

    def draw(self, surface):
        l = []
        # l = [list(map(lambda x: int(x / 10), e.coordinates)) for e in self.path_mng.points]
        # print(l)
        for e in self.points:
            x = int(e.x / 10)
            y = min(300, 300 - int(e.y / 10))
            l.append((x, y))
        pygame.draw.lines(surface, (255, 255, 0), False, l)
        print(l)

    def __str__(self):
        return "\n".join(str(e) for e in self.points)

    class PointData():
        """
        Utility class
        """

        def __init__(self, **data):
            self.x = data.get("x")
            self.y = data.get("y")
            self.coordinates = (data.get("x"), data.get("y"))
            self.rotation = data.get("rotation")
            self.power = data.get("power")
            self.fuel = data.get("fuel")
            self.h_speed = data.get("h_speed")
            self.v_speed = data.get("v_speed")

        def __str__(self):
            return "x:{:>4.0f} | y:{:>4.0f} | rotation:{:>3} | power: {} | fuel: {:>3.0f} | hs: {:.2f} | vs: {:.2f}" \
                .format(self.x, self.y, self.rotation, self.power, self.fuel, self.h_speed, self.v_speed)
