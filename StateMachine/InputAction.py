class InputAction:
    def __init__(self, action):
        self.action = action
    def __str__(self): return self.action
    def __cmp__(self, other):
        return cmp(self.action, other.action)
    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)

# Static fields; an enumeration of instances:
InputAction.getGameData  = InputAction("get game data")
InputAction.gameInfo  = InputAction("game info")
InputAction.playHeroCard  = InputAction("play hero card")
InputAction.playQuestCard  = InputAction("play quest card")
InputAction.drawDSCard  = InputAction("draw ds card")
InputAction.executeDSCard  = InputAction("execute ds card")
InputAction.advanceToDay  = InputAction("advance to day")
InputAction.advanceToEvening  = InputAction("advance to evening")
InputAction.advanceToNight  = InputAction("advance to night")
