from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import game.combat as combat
from game.combat import *

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
        #self.locations["inner temple"] = InnerTemple(self)
        #where do pirates start?
        self.starting_location = self.locations["beach"]
        self.ikey = False
        self.fkey = False
        self.wkey = False

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
        self.verbs["take"] = self
        self.item_in_sand = Sky_Key()
        self.event_chance = 30
        #append events once created

    def enter(self):
        description = "You set foot on a sandy beach on the south side of the island."
        if self.item_in_sand != None:
            description = description + "You see something shimmering in the sand, it looks like a key."
        announce(description)
    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "south"):
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["temple"]
        if(verb == "east"):
            config.the_player.next_loc = self.main_location.locations["lava zone"]
        if(verb == "west"):
            config.the_player.next_loc = self.main_location.locations["lake"]
        if(verb == "take"):
            if(self.item_in_sand == None):
                announce("There's nothing to take here")
            else:
                at_least_one = False
                i = self.item_in_sand
                if(i != None and i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce("You take the " + i.name + " from the sand.")
                    config.the_player.add_to_inventory([i])
                    self.item_in_sand = None
                    config.the_player.go = True
                    at_least_one = True
                if not at_least_one:
                    announce("You don't see that in the area.")
class Temple(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(ElementalIsland)
        super().__init__(main_location)
        self.name = "temple"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["enter"] = self

    def enter(self):
        announce("""You arrive at a large temple. The old stone door appears to be locked, perhaps there's some way to open it.""")

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "south"):
            #announce("You turn around and head south to the beach.")
            config.the_player.next_loc = self.main_location.locations["beach"]
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if(verb == "east"):
            config.the_player.next_loc = self.main_location.locations["lava zone"]
        if(verb == "west"):
            config.the_player.next_loc = self.main_location.locations["lake"]
        if(verb == "enter"):
            if(self.ikey == True and self.fkey == True and self.wkey == True):
                config.the_player.next_loc = self.main_location.locations["inner temple"]

            else:
                announce("You don't have enough keys to open the door")

class InnerTemple(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "inner temple"
        self.verbs["forward"] = self

    def enter(self):
        announce("You open the door to the old temple, there's a strange feeling in the air as you walk forward.")

class Mountain(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "mountain"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["forward"] = self
        
    def enter(self):
        announce("You arrive at the base of a snowy mountain, you hear a loud roar at the peak.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["temple"]
        if(verb == "east"):
            config.the_player.next_loc = self.main_location.locations["lava zone"]
        if(verb == "west"):
           config.the_player.next_loc = self.main_location.locations["lake"]
        if(verb == "forward"):
            monster = Yeti
            if(monster != None):
                announce("A yeti jumps down from the peak and attacks!")
                combat.Combat([Yeti("Yeti")]).combat()
                monster = None
                config.the_player.add_to_inventory([Sky_Key()])
                self.ikey = True
            else:
                announce("The snow blocks the path forward")
class LavaZone(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "lava zone"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["forward"] = self

    def enter(self):
        announce("""You walk out onto a field of rocks and lava, you're unsure of where the lava is coming from.""")

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "west"):
            config.the_player.next_loc = self.main_location.locations["temple"]
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if(verb == "forward"):
            monster = Lava_Golem
            if(monster != None):
                announce("A lava golem emerges!")
                combat.Combat([Lava_Golem("Lava Golem")]).combat()
                monster = None
                config.the_player.add_to_inventory([Sky_Key()])
                self.fkey = True
class Lake(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "lake"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["forward"] = self

    def enter(self):
        announce("You walk towards a small lake, the water is still. It's too quiet around this area.")

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "east"):
            config.the_player.next_loc = self.main_location.locations["temple"]            
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if(verb == "forward"):
            monster = Lake_Serpent
            if(monster != None):
                announce("A lake serpent jumps out of the water!")
                combat.Combat([Lake_Serpent("Lake Serpent")]).combat()
                monster = None
                config.the_player.add_to_inventory([Sky_Key()])
                self.wkey = True
                
class Sky_Key(items.Item):
    def __init__(self):
        super().__init__("key", 50)

class Yeti(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(65,80), (20,35)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(100,200), attacks, 70 + random.randrange(-20,21))

class Lava_Golem(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["lava throw"] = ["throws lava",random.randrange(70,101), (15,25)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(30,45), attacks, 100 + random.randrange(-20,21))

class Lake_Serpent(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["venom bite"] = ["bites",random.randrange(70,101), (30,35)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(10,25), attacks, 200 + random.randrange(-20,21))
