#import sys
#import collections
#import StateMachine.GameStates 
#import StateMachine.InputAction

colors = ['red','green','blue','black','purple']

war_status = ['early','mid','mid','late']


		
class DarknessSpreadsCard:
	def __init__(self, area1 = False, area1_color = False, area1_count = 0, 
		area2 = False, area2_color = False, area2_count = 0, 
		general = False, general_move_to_area = False, 
		general_minion_color = False, general_minion_count = 0, 
		special_actions = False):

		self.general = general
		self.general_move_to_area = general_move_to_area
		self.general_minion_count = general_minion_count
		self.general_minion_color = general_minion_color
		self.area1 = area1
		self.area1_color = area1_color
		self.area1_count = area1_count
		self.area2 = area2
		self.area2_color = area2_color
		self.area2_count = area2_count
		self.special_actions = special_actions

	def display(self):
		print self.area1.name  + ": " + str(self.area1_count) + " " + self.area1_color
		print self.area2.name  + ": " + str(self.area2_count) + " " + self.area2_color
		print self.general.name  + ": " + self.general_move_to_area.name + " " + str(self.general_minion_count) + " " + self.general_minion_color

	def execute(self):
		if self.special_actions != False:
			for action in self.special_actions:
				action
		for x in range (0, self.area1_count):
			add_minion_to_area(self.area1_color, self.area1)
		for x in range (0, self.area2_count):
			add_minion_to_area(self.area2_color, self.area2)
		if (self.general):
			self.general.move(self.general_move_to_area)
			for x in range (0, self.general_minion_count):
				add_minion_to_area(self.general_minion_color ,self.general_move_to_area)
		

class General:
	def __init__(self, location, path, name, hits, wounded_hits):
		self.location = location
		self.path = path
		self.name = name
		self.total_hits = hits
		self.wounded_hits = wounded_hits
		self.remaining_hits = hits
		location.general.add(self)

	def move(self, move_to_area):
		if (self.able_to_move() == False):
			return
		if (move_to_area == "Any"):
			self.location.general = False #TODO, maybe fix this to work as list in case 2 generals in dame location?
			self.location = path[path.index(location) +1]
			self.location.general.append(self)
		elif (move_to_area in path):
			if (path.index(self.location) + 1 == path.index(move_to_area)):
					self.location.general = False #TODO, maybe fix this to work as list in case 2 generals in dame location?
					self.location = move_to_area
					move_to_area.general.append(self)
		else:
			raise Exception("Trying to move a general somewhere?")
			
		if (self.location.name == "Monarch City"):
			print "Game over: " + general.name + " has conquered Monarch City"
			sys.exit(0)

	def able_to_move(self):
		# TODO, actually implement this
		# not critically wounded
		# not dead
		# not blocked by a card?
		return True

class Crystal:
	def __init__(self,location):
		self.location = location
		location.add(self)

class Minion:
	def __init__(self, color,location):
		if color in colors:
			self.color = color
			self.location = location
			location.add(self)
		else:
			raise AttributeError

class Area:
	# TODO - how do we handle inns?
	# TODO - need to handle treasure chest areas for rogue etc
	def __init__(self, name, color, treasure_chest=False, gateway=False,neighbors=set()):
		if color in colors:
			self.color     = color
			self.name      = name
			self.treasure_chest = treasure_chest
			self.gateway   = gateway
			self.neighbors = neighbors
			self.minions   = set()
			self.general   = set()
			self.crystals  = set()
			self.defenders = set()
		else:
			raise AttributeError



		# allowed actions for day
			# move
			# fight minions
			# done (moves to next phase)
			# show board
			# play special cards (instants that can be played any time)
		#allowed actions evening
			# done (moves to next phase) but only after  taking two cards and if needed discarding
			# show board
			# take two hero card
			# discard down to hand limit (10)
			# play special cards (instants that can be played any time)
		# allowed actions night
# darkness spreads procedure
# 1. Advance to darkenss spreads in turn data
# 2. Draw card (pop from deck)
# 3. do actions on card
# 4. discard card (put in pile)
			# done (moves to next phase) But only after darkness spreads tasks
			# show board
			# take correct number of cards and do correct actions on them
			# play special cards (instants that can be played any time)
		# any time actions
			# show board
			# save bookmark to this game (dump state and serialize?)
			# quit

#TODO Think about logging each action (hero or darkness spreads) somewhere so we can replay game?
			
class action:
	def __init__(self,name,function,*args):
		self.action=function(*args)

class GameController:
	def __init__(self):
		self.possible_actions = None
		self.allowed_actions  = None

		self.initialize_actions()
		self.game_data = Game()

	
		
	def initialize_actions(self):
		self.possible_actions["goto_next_phase"] = game_data.advance_phase 


class Game:
	def __init__(self):
		self.minions = dict()
		self.minions["red"]   = None;
		self.minions["green"] = None;
		self.minions["blue"]  = None;
		self.minions["black"] = None;

		self.unused_minions = dict()
		self.unused_minions["red"] = set()
		self.unused_minions["green"] = set()
		self.unused_minions["blue"] = set()
		self.unused_minions["black"] = set()

		self.crystals = set()
		self.unused_crystals = set()
		self.generals=dict()
		
		self.areas         = None

		self.ds_cards = list()
		self.ds_deck = None
		self.hc_deck = None
		self.qc_deck = None

		self.war_status = 0

		self.initialize_minions()
		self.initialize_areas()
		self.initialize_crystals()
		self.initialize_generals()
		self.initialize_ds_cards()

	def dump_game_data(self):
		print "Unused Minions:"
		print "\tRed: (" + str(len(self.unused_minions["red"])) + ")"
		print "\tGreen: (" + str(len(self.unused_minions["green"])) + ")"
		print "\tBlue: (" + str(len(self.unused_minions["blue"])) + ")"
		print "\tBlack: (" + str(len(self.unused_minions["black"])) + ")"
		print "Unused Crystals: (" + str(len(self.unused_crystals)) + ")" 
		print "Areas:"
		for area_name in self.areas:
			area = self.areas[area_name]
			print area.name + ":"
			print "\tminions: ",
			for minion in area.minions:
				print minion.color,
			print " "
			print "\tcrystals: " + str(len(area.crystals))

	def initialize_minions(self, minion_count=20):
		self.minions["red"] = [Minion("red",self.unused_minions["red"])     for _ in range(minion_count)]
		self.minions["green"] = [Minion("green",self.unused_minions["green"]) for _ in range(minion_count)]
		self.minions["black"] = [Minion("black",self.unused_minions["black"]) for _ in range(minion_count)]
		self.minions["blue"] = [Minion("blue",self.unused_minions["blue"])   for _ in range(minion_count)]

	def initialize_crystals(self, crystal_count=12):
		self.crystals = [Crystal(self.unused_crystals)   for _ in range(crystal_count)]

	def initialize_generals(self):
		sapphire_path = (self.areas["Blizzard Mountains"],self.areas["Heavens Glade"],
			self.areas["Ancient Ruins"],self.areas["Greenleaf Village"],self.areas["Monarch City"])
		varkolak_path = (self.areas["Dark Woods"],self.areas["Windy Pass"],
			self.areas["Seabird Port"],self.areas["Father Oak Forest"],self.areas["Monarch City"])
		gorgutt_path = (self.areas["Thorny Woods"],self.areas["Amarak Peak"],
			self.areas["Eagle Peak Pass"],self.areas["Orc Valley"],self.areas["Monarch City"])
		balazarg_path = (self.areas["Scorpion Canyon"],self.areas["Raven Forest"],
			self.areas["Angel Tear Falls"],self.areas["Bounty Bay"],self.areas["Monarch City"])

		self.generals["Sapphire"] = General(self.areas["Blizzard Mountains"],sapphire_path,"Sapphire",4,0)
		self.generals["Varkolak"] = General(self.areas["Dark Woods"],varkolak_path,"Varkolak",5,0)
		self.generals["Gorgutt"] = General(self.areas["Thorny Woods"],gorgutt_path,"Gorgutt",6,2)
		self.generals["Balazarg"] = General(self.areas["Scorpion Canyon"],balazarg_path,"Balazarg",6,1)

	def initialize_ds_cards(self):
		#areas and generals and minions must be initialized first
		self.ds_cards = [DarknessSpreadsCard(self.areas["Windy Pass"], "red", 2, 
							self.areas["Raven Forest"], "green", 1,
							self.generals["Gorgutt"],self.areas["Orc Valley"],
							"green", 2, False),
				DarknessSpreadsCard(self.areas["Cursed Plateau"], "red", 1,
							self.areas["Golden Oak Forest"], "green", 2,
							self.generals["Gorgutt"],self.areas["Amarak Peak"],
							"green", 2, False),
				DarknessSpreadsCard(self.areas["Blood Flats"], "red", 2,
							self.areas["Greenleaf Village"], "green", 1,
							self.generals["Varkolak"],self.areas["Seabird Port"],
							"black", 2, False),
				DarknessSpreadsCard(self.areas["Pleasant Hill"], "red", 1,
							self.areas["Minotaur Forest"], "green", 2,
							self.generals["Varkolak"],self.areas["Father Oak Forest"],
							"black", 1, False),
				DarknessSpreadsCard(self.areas["Bounty Bay"], "blue", 2,
							self.areas["Brookdale Village"], "black", 2,
							self.generals["Sapphire"],self.areas["Greenleaf Village"],
							"blue", 1, False),
				DarknessSpreadsCard(self.areas["Rock Bridge Pass"], "blue", 1,
							self.areas["Dark Woods"], "black", 1,
							self.generals["Balazarg"],self.areas["Bounty Bay"],
							"red", 1, False),
				DarknessSpreadsCard(self.areas["Cursed Plateau"], "red", 2,
							self.areas["Fire River"], "black", 2,
							self.generals["Balazarg"],self.areas["Bounty Bay"],
							"red", 2, False),

				DarknessSpreadsCard(self.areas["Wyvern Forest"], "green", 2,
							self.areas["Seabird Port"], "black", 2,
							self.generals["Sapphire"],self.areas["Heavens Glade"],
							"blue", 1, False),
				DarknessSpreadsCard(self.areas["Unicorn Forest"], "green", 2,
							self.areas["Crystal Hills"], "blue", 2,
							self.generals["Gorgutt"],"Any",
							"green", 2, False),
				DarknessSpreadsCard(False, False, 0,
							False, False, 0,
							self.generals["Sapphire"],self.areas["Monarch City"],
							"blue", 0, self.orc_war_party),
				DarknessSpreadsCard(self.areas["Rock Bridge Pass"], "blue", 2,
							self.areas["Angel Tear Falls"], "black", 1,
							self.generals["Balazarg"],self.areas["Angel Tear Falls"],
							"red", 2, False),
				DarknessSpreadsCard(self.areas["Minotaur Forest"], "green", 2,
							self.areas["Land of Amazons"], "black", 1,
							self.generals["Balazarg"],"Any",
							"red", 1, False),
				DarknessSpreadsCard(self.areas["Wolf Pass"], "blue", 1,
							self.areas["Dancing Stone"], "black", 1,
							self.generals["Gorgutt"],self.areas["Monarch City"],
							"green", 0, False),
				DarknessSpreadsCard(self.areas["Blood Flats"], "red", 1,
							self.areas["Bounty Bay"], "blue", 1,
							self.generals["Gorgutt"],self.areas["Amarak Peak"],
							"green", 2, False),

				DarknessSpreadsCard(self.areas["Ancient Ruins"], "red", 2,
							self.areas["Eagle Peak Pass"], "blue", 2,
							self.generals["Sapphire"],self.areas["Heavens Glade"],
							"blue", 1, False),
				]

	def orc_war_party(self):
		print "ORC WAR PARTY!!!!!!"
		for area in self.areas:
			if len(self.areas[area].minons) == 1 and self.areas[area].minons[0].color == "green":
				print "\t\t Adding orc to " + area
				add_minion_to_area("green", self.areas[area])

	def orc_patrols(self):
		print "ORC PATROL!!!!!!!"
		for area in self.areas:
			if len(self.areas[area].minons) == 0 and self.areas[area].color == "green":
				print "\t\t Adding orc to " + area
				add_minion_to_area("green", self.areas[area])

	def initialize_areas(self):
		#Eventually make this read in from config file?
		self.areas = dict()
		self.areas['Amarak Peak']         = Area('Amarak Peak','blue')
		self.areas['Ancient Ruins']       = Area('Ancient Ruins','red')
		self.areas['Angel Tear Falls']    = Area('Angel Tear Falls','black')
		self.areas['Blizzard Mountains']  = Area('Blizzard Mountains','blue')
		self.areas['Blood Flats']         = Area('Blood Flats','red')
		self.areas['Bounty Bay']          = Area('Bounty Bay','blue',treasure_chest=True)
		self.areas['Brookdale Village']   = Area('Brookdale Village','black')
		self.areas['Chimera Inn']         = Area('Chimera Inn','purple')
		self.areas['Crystal Hills']       = Area('Crystal Hills','blue')
		self.areas['Cursed Plateau']      = Area('Cursed Plateau','red')
		self.areas['Dancing Stone']      = Area('Dancing Stone','black',gateway=True)
		self.areas['Dark Woods']          = Area('Dark Woods','black')
		self.areas['Dragons Teeth Range'] = Area('Dragons Teeth Range','blue')
		self.areas['Eagle Nest Inn']      = Area('Eagle Nest Inn','purple')
		self.areas['Eagle Peak Pass']     = Area('Eagle Peak Pass','blue')
		self.areas['Enchanted Glade']     = Area('Enchanted Glade','black')
		self.areas['Father Oak Forest']   = Area('Father Oak Forest','green')
		self.areas['Fire River']          = Area('Fire River','black')
		self.areas['Ghost Marsh']         = Area('Ghost Marsh','red')
		self.areas['Golden Oak Forest']   = Area('Golden Oak Forest','green')
		self.areas['Greenleaf Village']   = Area('Greenleaf Village','green') 
		self.areas['Gryphon Forest']      = Area('Gryphon Forest','green')
		self.areas['Gryphon Inn']         = Area('Gryphon Inn','purple')
		self.areas['Heavens Glade']       = Area('Heavens Glade','green')
		self.areas['Land of Amazons']     = Area('Land of Amazons','black',treasure_chest=True)
		self.areas['Mccorm Highlands']    = Area('Mccorm Highlands','black',treasure_chest=True)
		self.areas['Mermaid Harbor']      = Area('Mermaid Harbor','black',treasure_chest=True)
		self.areas['Minotaur Forest']     = Area('Minotaur Forest','green')
		self.areas['Monarch City']        = Area('Monarch City','purple',treasure_chest=True)
		self.areas['Mountains of Mist']   = Area('Mountains of Mist','blue')
		self.areas['Orc Valley']          = Area('Orc Valley','red')
		self.areas['Pleasant Hill']       = Area('Pleasant Hill','red',treasure_chest=True)
		self.areas['Raven Forest']        = Area('Raven Forest','green')
		self.areas['Rock Bridge Pass']    = Area('Rock Bridge Pass','blue')
		self.areas['Scorpion Canyon']     = Area('Scorpion Canyon','red')
		self.areas['Seabird Port']        = Area('Seabird Port','black',treasure_chest=True)
		self.areas['Seagull Lagoon']      = Area('Seagull Lagoon','blue')
		self.areas['Serpent Swamp']       = Area('Serpent Swamp','red')
		self.areas['Thorny Woods']        = Area('Thorny Woods','green')
		self.areas['Unicorn Forest']      = Area('Unicorn Forest','green')
		self.areas['Whispering Woods']    = Area('Whispering Woods','green')
		self.areas['Windy Pass']          = Area('Windy Pass','red')
		self.areas['Withered Hills']      = Area('Withered Hills','red')
		self.areas['Wolf Pass']           = Area('Wolf Pass','blue')
		self.areas['Wyvern Forest']       = Area('Wyvern Forest','green')

		self.areas['Amarak Peak'].neighbors   = [self.areas['Eagle Peak Pass'],
								self.areas['Mccorm Highlands'],
								self.areas['Ghost Marsh'],
								self.areas['Thorny Woods']]
		self.areas['Ancient Ruins'].neighbors   = [self.areas['Whispering Woods'],
								self.areas['Heavens Glade'],
								self.areas['Greenleaf Village']]
		self.areas['Angel Tear Falls'].neighbors   = [self.areas['Bounty Bay'],
								self.areas['Pleasant Hill'],
								self.areas['Fire River'],
								self.areas['Dragons Teeth Range'],
								self.areas['Raven Forest']]
		self.areas['Blizzard Mountains'].neighbors = [self.areas['Withered Hills'],
								self.areas['Heavens Glade']]
		self.areas['Blood Flats'].neighbors = [self.areas['Scorpion Canyon'],
								self.areas['Raven Forest'],
								self.areas['Unicorn Forest'],
								self.areas['Brookdale Village']]
		self.areas['Bounty Bay'].neighbors         = [self.areas['Monarch City'],
								self.areas['Greenleaf Village'],
								self.areas['Angel Tear Falls'],
								self.areas['Mermaid Harbor']]
		self.areas['Brookdale Village'].neighbors     = [self.areas['Blood Flats'],
								self.areas['Unicorn Forest'],
								self.areas['Rock Bridge Pass'],
								self.areas['Seabird Port'],
								self.areas['Father Oak Forest'],
								self.areas['Pleasant Hill']]
		self.areas['Chimera Inn'].neighbors     = [self.areas['Withered Hills']]
		self.areas['Crystal Hills'].neighbors     = [self.areas['Withered Hills'],
								self.areas['Fire River'],
								self.areas['Mermaid Harbor'],
								self.areas['Wyvern Forest']]
		self.areas['Cursed Plateau'].neighbors     = [self.areas['Withered Hills'],
								self.areas['Land of Amazons'],
								self.areas['Wyvern Forest']]
		self.areas['Dancing Stone'].neighbors     = [self.areas['Monarch City'],
								self.areas['Orc Valley'],
								self.areas['Greenleaf Village']]
		self.areas['Dark Woods'].neighbors  = [self.areas['Windy Pass'],
								self.areas['Golden Oak Forest']]
		self.areas['Dragons Teeth Range'].neighbors  = [self.areas['Angel Tear Falls']]
		self.areas['Eagle Nest Inn'].neighbors     = [self.areas['Enchanted Glade']]
		self.areas['Eagle Peak Pass'].neighbors  = [self.areas['Orc Valley'],
								self.areas['Amarak Peak'],
								self.areas['Whispering Woods']]
		self.areas['Enchanted Glade'].neighbors  = [self.areas['Eagle Nest Inn'],
								self.areas['Rock Bridge Pass'],
								self.areas['Unicorn Forest']]
		self.areas['Father Oak Forest'].neighbors  = [self.areas['Monarch City'],
								self.areas['Wolf Pass']]
		self.areas['Fire River'].neighbors = [self.areas['Angel Tear Falls'],
								self.areas['Mermaid Harbor'],
								self.areas['Crystal Hills']]
		self.areas['Ghost Marsh'].neighbors = [self.areas['Amarak Peak']]
		self.areas['Golden Oak Forest'].neighbors = [self.areas['Dark Woods'],
								self.areas['Rock Bridge Pass']]
		self.areas['Greenleaf Village'].neighbors = [self.areas['Monarch City'],
								self.areas['Dancing Stone'],
								self.areas['Ancient Ruins'],
								self.areas['Mountains of Mist'],
								self.areas['Bounty Bay']]
		self.areas['Gryphon Forest'].neighbors = [self.areas['Seagull Lagoon'],
								self.areas['Serpent Swamp'],
								self.areas['Gryphon Inn']]
		self.areas['Gryphon Inn'].neighbors = [self.areas['Gryphon Forest']]
		self.areas['Heavens Glade'].neighbors = [self.areas['Thorny Woods'],
								self.areas['Blizzard Mountains'],
								self.areas['Ancient Ruins'],
								self.areas['Whispering Woods']]
		self.areas['Land of Amazons'].neighbors = [self.areas['Mountains of Mist'],
								self.areas['Cursed Plateau'],
								self.areas['Wyvern Forest'],
								self.areas['Mermaid Harbor']]
		self.areas['Mccorm Highlands'].neighbors = [self.areas['Serpent Swamp'],
								self.areas['Amarak Peak']]
		self.areas['Mermaid Harbor'].neighbors       = [self.areas['Bounty Bay'],
								self.areas['Land of Amazons'],
								self.areas['Wyvern Forest'],
								self.areas['Crystal Hills'],
								self.areas['Fire River']]
		self.areas['Minotaur Forest'].neighbors = [self.areas['Seagull Lagoon'],
								self.areas['Wolf Pass']]
		self.areas['Monarch City'].neighbors       = [self.areas['Father Oak Forest'],
								self.areas['Wolf Pass'],
								self.areas['Orc Valley'],
								self.areas['Dancing Stone'],
								self.areas['Greenleaf Village'],
								self.areas['Bounty Bay']]
		self.areas['Mountains of Mist'].neighbors = [self.areas['Greenleaf Village'],
								self.areas['Land of Amazons'],
								self.areas['Withered Hills']]
		self.areas['Orc Valley'].neighbors         = [self.areas['Monarch City'],
								self.areas['Wolf Pass'],
								self.areas['Dancing Stone']]
		self.areas['Pleasant Hill'].neighbors      = [self.areas['Angel Tear Falls'],
								self.areas['Father Oak Forest']]
		self.areas['Raven Forest'].neighbors       = [self.areas['Scorpion Canyon'],
								self.areas['Blood Flats'],
								self.areas['Pleasant Hill'],
								self.areas['Angel Tear Falls']]
		self.areas['Rock Bridge Pass'].neighbors       = [self.areas['Golden Oak Forest'],
								self.areas['Windy Pass'],
								self.areas['Seabird Port'],
								self.areas['Brookdale Village'],
								self.areas['Enchanted Glade']]
		self.areas['Scorpion Canyon'].neighbors      = [self.areas['Raven Forest'],
								self.areas['Blood Flats']]
		self.areas['Seabird Port'].neighbors       = [self.areas['Father Oak Forest'],
								self.areas['Brookdale Village'],
								self.areas['Rock Bridge Pass'],
								self.areas['Windy Pass']]
		self.areas['Seagull Lagoon'].neighbors      = [self.areas['Minotaur Forest'],
								self.areas['Gryphon Forest'],
								self.areas['Wolf Pass']]
		self.areas['Serpent Swamp'].neighbors      = [self.areas['Gryphon Forest'],
								self.areas['Mccorm Highlands']]
		self.areas['Thorny Woods'].neighbors      = [self.areas['Heavens Glade'],
								self.areas['Amarak Peak']]
		self.areas['Unicorn Forest'].neighbors      = [self.areas['Enchanted Glade'],
								self.areas['Brookdale Village'],
								self.areas['Blood Flats']]
		self.areas['Whispering Woods'].neighbors       = [self.areas['Heavens Glade'],
								self.areas['Ancient Ruins'],
								self.areas['Dancing Stone'],
								self.areas['Eagle Peak Pass']]
		self.areas['Windy Pass'].neighbors          = [self.areas['Dark Woods'],
								self.areas['Rock Bridge Pass'],
								self.areas['Seabird Port']]
		self.areas['Withered Hills'].neighbors       = [self.areas['Blizzard Mountains'],
								self.areas['Chimera Inn'],
								self.areas['Mountains of Mist'],
								self.areas['Eagle Peak Pass']]
		self.areas['Wolf Pass'].neighbors          = [self.areas['Monarch City'],
								self.areas['Father Oak Forest'],
								self.areas['Seagull Lagoon'],
								self.areas['Minotaur Forest'],
								self.areas['Orc Valley']]
		self.areas['Wyvern Forest'].neighbors          = [self.areas['Crystal Hills'],
								self.areas['Mermaid Harbor'],
								self.areas['Land of Amazons'],
								self.areas['Cursed Plateau']]

	def overrun_area(self,color,area):
		print "An overrun was triggered in " + area.name + " || color (" + color + ")"
		for neighbor in area.neighbors:
			print "An overrun flowed into " + neighbor.name + " || color (" + color + ")"
			self.add_minion_to_area(color, neighbor, True)


	def taint_area(self, area):
		print "A taint was triggered in " + area.name 
		try:
			crystal = self.unused_crystals.pop()
			area.crystals.add(crystal)
			crystal.location = area
		except KeyError, e:
			print "Game over, no more crystals to place"
			sys.exit(0)

	def add_minion_to_area(self,color, area, overrun_triggered = False):
		# TODO if unused piles have no minions left, than check if they are on quest cards
		taint_done = False
		if (area.name == 'Monarch City'): # so no overflow or taint, but we could lose the game if there are 5
			if (len(area.minions) >=5):
				print "Game over, Monarch city has been overrun with minions"
				sys.exit(0)
			else:
				minion = self.unused_minions[color].pop()
				minion.location = area
				area.minions.add(minion)
		else: #Monarch city is different from how we handle everything else
			if (len(area.minions) >= 3):
				self.taint_area(area)
				taint_done = True
				if (overrun_triggered == False):
					self.overrun_area(color,area)

			else:
				try:
					minion = self.unused_minions[color].pop()
					minion.location = area
					area.minions.add(minion)
				except KeyError, e:
					#TODO need to check for minions quest cards now or we lose the game
					print "Game over, no more " + color + "minions to place"
					sys.exit(0)

			if (color == 'red' and len(area.minions) >= 3 and taint_done == False):
				# keep this separate from overrun logic so its not too messy
				#This is for demon overruns only, the minion should have already been placed unlike the other taint code
				#TODO , need to see if other already placed minions are all red
				red_count = 0
				for i in area.minions:
					if i.color=='red':
						red_count += 1
				if red_count >= 3:
					print "\tDemon taint in " + area.name
					self.taint_area(area)

	def darknessSpreads(self):
		# draw card, do actions
		# if middle or late war draw another and do actions, but skip non-general move actions
		if self.war_status[current_war_state] != 'early':
			print "hello"
		# if late war draw another and do actions, but skip non-general move actions
		if self.war_status[current_war_state] == 'late':
			print "hello"

# vim: tabstop=4 shiftwidth=4 expandtab

