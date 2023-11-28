from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import game.combat as combat

class ElementalIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        self.name = "elemental island"
        self.symbol = 'I' #Symbol for map
        self.visitable = True #marks the island as a place pirates can "go ashore"
        self.locations = {} #dictionary of sub-locations on the island
        self.locations["beach"] = Beach(self)
        self.locations["temple"] = Temple(self)
        self.locations["lake"] = Lake(self)
        self.locations["lava zone"] = LavaZone(self)
        self.locations["mountain"] = Mountain(self)
        #where do pirates start?
        self.starting_location = self.locations["beach"]

    def enter(self, ship):
        announce("arrived at a strange island")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        #self.event_chance = 30
        #append events once created
    def enter(self):
        announce("Your ship is anchored, you land at a beach on the south side of the island.")


