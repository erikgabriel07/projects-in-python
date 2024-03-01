from gameAssets.player import *


class CPU(Player):
    def __init__(self, cpu_name, cpu_hand=[], cpu_cash=0):
        super(CPU, self).__init__(cpu_name, cpu_hand, cpu_cash, 'CPU')
        self._hidden_card = ''

    def reveal_card(self) -> None:
        super(CPU, self).__delattr__('hand')
        super(CPU, self).__setattr__(
            'hand', self._hidden_card + ' (Revealed) ')

    def __evaluate(self, oponnent: Player) -> int:
        oponnent_points = oponnent.getPoints
        my_points = super(CPU, self).getPoints
        difference = my_points - oponnent_points
        if difference < 0 and not super(CPU, self).getPoints >= 17:
            return 0
        elif difference > 0 and not super(CPU, self).getPoints >= 17:
            return 1
        elif difference == 0 and not super(CPU, self).getPoints >= 17:
            return 2
        else:
            return 3

    def decision(self, oponnent: Player) -> str:
        variable = self.__evaluate(oponnent=oponnent)
        match variable:
            case 0:
                return 'Hit'
            case 1:
                return 'Stand'
            case 2:
                return 'Draw'
            case _:
                return 'None'

    def ace_value(self):
        d = super(CPU, self).getPoints + 11
        if d > 21:
            return 'O'
        else:
            return 'E'
