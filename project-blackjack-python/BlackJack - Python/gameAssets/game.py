class Game:
    def __init__(self, game_active, player_turn, state):
        self.__game_active = game_active
        self.__player_turn = player_turn
        self.__state = state

    @property
    def active(self):
        return self.__game_active

    @property
    def turn(self):
        return self.__player_turn

    @property
    def state(self):
        return self.__state

    @active.setter
    def active(self, new_boolean_value: bool) -> None:
        self.__game_active = new_boolean_value

    @turn.setter
    def turn(self, player_turn: str) -> None:
        self.__player_turn = player_turn

    @state.setter
    def state(self, game_state: str) -> None:
        self.__state = game_state
