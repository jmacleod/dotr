from StateMachine.State import State
from StateMachine.StateMachine import StateMachine
from StateMachine.InputAction import InputAction
from GameData.GameData import GameData

class StateT(State):
    state_stack = list()
    game_data = GameData()

    def __init__(self):
        self.transitions = None
    def next(self, input):
        if self.transitions.has_key(input):
            return self.transitions[input]
        else:
            raise Exception("Input not supported for current state")

class NightBegins(StateT):
    def run(self):
        print("NightTime Falls")
    def next(self, input):
        StateT.state_stack.append(self)
        if not self.transitions:
            self.transitions = {
                InputAction.getGameData : GameStates.nightBegins,
                InputAction.playHeroCard : GameStates.nightBegins,
                InputAction.playQuestCard : GameStates.nightBegins,
                InputAction.drawDSCard : GameStates.drawDSCard,
            }
        return StateT.next(self, input)

class DrawDSCard(StateT):
    def run(self):
        print("Darkness Spreads drawing card")
	StateT.current_ds_card = StateT.game_data.ds_cards.pop()
	StateT.current_ds_card.display()
	print "STACK: " + str(StateT.state_stack)
    def next(self, input):
        StateT.state_stack.append(self)
        if not self.transitions:
            self.transitions = {
              InputAction.getGameData : GameStates.nightBegins,
              InputAction.playHeroCard : GameStates.nightBegins,
              InputAction.playQuestCard : GameStates.nightBegins,
              InputAction.drawDSCard : GameStates.drawDSCard,
              InputAction.executeDSCard : GameStates.executeDSCard,
            }
        return StateT.next(self, input)

class ExecuteDSCard(StateT):
    def run(self):
        print("Darkness Spreads - executing card")
	StateT.current_ds_card.execute(StateT.game_data)
	print "STACK: " + str(StateT.state_stack)
    def next(self, input):
        StateT.state_stack.append(self)
        if not self.transitions:
            self.transitions = {
              InputAction.getGameData : GameStates.nightBegins,
              InputAction.playHeroCard : GameStates.nightBegins,
              InputAction.playQuestCard : GameStates.nightBegins,
              InputAction.drawDSCard : GameStates.drawDSCard,
              InputAction.advanceToDay : GameStates.dayBegins,
            }
        return StateT.next(self, input)

class DayBegins(StateT):
    def run(self):
        print("Day Time")
	print "STACK: " + str(StateT.state_stack)
    def next(self, input):
        if not self.transitions:
            self.transitions = {
              InputAction.getGameData : GameStates.nightBegins,
              InputAction.playHeroCard : GameStates.nightBegins,
              InputAction.PlayQuestCard : GameStates.nightBegins,
              InputAction.advanceToEvening : GameStates.eveningBegins,
            }
        return StateT.next(self, input)

class EveningBegins(StateT):
    def run(self):
        print("Day Time")
	print "STACK: " + str(StateT.state_stack)
    def next(self, input):
        if not self.transitions:
            self.transitions = {
              InputAction.getGameData : GameStates.nightBegins,
              InputAction.playHeroCard : GameStates.nightBegins,
              InputAction.PlayQuestCard : GameStates.nightBegins,
              InputAction.advanceToNight : GameStates.nightBegins,
            }
        return StateT.next(self, input)

class GameStates(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, GameStates.nightBegins)

# Static variable initialization:
GameStates.nightBegins = NightBegins()
GameStates.drawDSCard = DrawDSCard()
GameStates.executeDSCard = ExecuteDSCard()
GameStates.eveningBegins = EveningBegins()
GameStates.dayBegins = DayBegins()

