import random
import unittest
import dotr
from StateMachine.StateMachine import StateMachine
from StateMachine.InputAction import InputAction
from StateMachine.State import State
from StateMachine.GameStates import GameStates

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    def test_adding_minions(self):
	print "Test Adding minions to an area"
	game_data = dotr.Game()
	area = game_data.areas["Pleasant Hill"]
        self.assertTrue(len(area.minions) == 0)
	game_data.add_minion_to_area("red", area)
	print "Asserting that minions in area = 1"
        self.assertTrue(len(area.minions) == 1)
	print "Asserting that unused red minions = 19 (" + str(len(game_data.unused_minions["red"])) + ")"
        self.assertTrue(len(game_data.unused_minions["red"]) == 19)

    def test_max_minions_per_area(self):
	print "Test max minions per area"
	game_data = dotr.Game()
	area = game_data.areas["Father Oak Forest"]
	print "Testing that area starts with no minions"
        self.assertTrue(len(area.minions) == 0)
	game_data.add_minion_to_area("black", area)
	game_data.add_minion_to_area("red", area)
	game_data.add_minion_to_area("black", area)
	print "Asserting that minions = 3"
        self.assertTrue(len(area.minions) == 3)
	print "Asserting that minions still = 3"
	game_data.add_minion_to_area("red", area)
        self.assertTrue(len(area.minions) == 3)
	print "Asserting that minions still = 3"
	game_data.add_minion_to_area("blue", area)
        self.assertTrue(len(area.minions) == 3)
	print "Asserting that unused black minions = 18 (" + str(len(game_data.unused_minions["black"])) + ")"
        self.assertTrue(len(game_data.unused_minions["black"]) == 18)
	print "Asserting that unused blue minions = 19 (" + str(len(game_data.unused_minions["blue"])) + ")"
        self.assertTrue(len(game_data.unused_minions["blue"]) == 18)

    def test_game_ends_when_no_more_minions_to_place(self):
	print "Test game ends when no more minions to place"
	game_data = dotr.Game()
	area = game_data.areas["Father Oak Forest"]
	game_data.add_minion_to_area("blue", area)
	game_data.add_minion_to_area("blue", area)
	game_data.add_minion_to_area("blue", area)
	area = game_data.areas["Father Oak Forest"]
        self.assertRaises(SystemExit)

    def test_state_machine(self):
        test = [InputAction("draw ds card"),InputAction("execute ds card")]
        print "TEST: " + str(test)
        for i in test:
            print "\t\t\tMOVE: " + i.action
        GameStates().runAll(test)
# test over run
# test crystal placement
# test game ends when out of minions of a color, and a new one is attempted to be placed (we mightbe doing this wrong in the code)
# test game ends when out of crystals
# test monarch city can get up to 5 minions, game ends when at 5 or maybe when one more than 5 attempts to get placed
# test you can;t place minions in inns, especially with overruns

#
#
#for area_name in game_data.areas:
#	an_area = game_data.areas[area_name]
#	#print "Number of unused crystals: " + str(len(game_data.unused_crystals))
#	#print "Area name is " + str(an_area.name)
#	print "Adding a new minion ---------------------------------------------- " + str(an_area.name) 
#	game_data.add_minion_to_area("black", an_area) 
#	game_data.dump_game_data()
#	print "Adding a new minion ---------------------------------------------- " + str(an_area.name) 
#	game_data.add_minion_to_area("black", an_area) 
#	game_data.dump_game_data()
#	print "Adding a new minion ---------------------------------------------- " + str(an_area.name) 
#	game_data.add_minion_to_area("black", an_area) 
#	game_data.dump_game_data()
#	print "Adding a new minion ---------------------------------------------- " + str(an_area.name) 
#	game_data.add_minion_to_area("black", an_area) 
#	game_data.dump_game_data()
#	#print "Adding a new minion ----------------------------------------------"
#	#game_data.add_minion_to_area("black", an_area) 
#	#game_data.dump_game_data()
#	#print "Adding a new minion ----------------------------------------------"
#	#game_data.add_minion_to_area("black", an_area) 
#	#game_data.dump_game_data()
#	#print "Adding a new minion ----------------------------------------------"
#	#game_data.add_minion_to_area("black", an_area) 
#	#game_data.dump_game_data()
#	#print "Number of unused black minions: " + str(len(game_data.unused_minions["black"]))
#	#print "Number of minions in area: " + str(len(an_area.minions))
#	#print "Area minions set: " + str(an_area.minions)
#
#
if __name__ == '__main__':
    unittest.main()

