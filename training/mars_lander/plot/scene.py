import json
from training.mars_lander.ship_physics import ShipPhysics
from training.mars_lander.plot.window import GameWindow

class Scene:

    def __init__(self, id=1):

        fp = "/home/florian/Dev/coding_game/training/mars_lander/game_data.json"
        with open(fp) as file:
            data = json.load(file)
            self.game_data = data.get(str(id))

        self.terrain = self.game_data.get("terrain")
        self.ship = ShipPhysics(**dict(self.game_data.get("ship")))
        self.window = GameWindow(self.ship)

    def launch(self):
        self.window.terrain(self.terrain)
        self.window.draw(self.ship)



s = Scene()
s.launch()
print(s.ship)
print(s.terrain)
