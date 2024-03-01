from re import findall, match


class Player:
    def __init__(self, player_name: str, player_hand: list, player_cash: float, player_type: str):
        self.player_name = player_name
        self._player_type = player_type
        self.__player_hand = player_hand
        self.__player_cash = player_cash
        self.__player_points = 0
        self.__choosen_ace_value = []

    def show_player_cash(self) -> None:
        print('%s - BALANCE: US$%s' % (self.player_name, self.__player_cash))

    def chooseAceValue(self, value) -> None:
        self.__choosen_ace_value.append(value)

    def show_player_hand(self) -> None:
        count = 0
        print(f'{self.player_name} hand: ', end='')
        for card in self.__player_hand:
            if count < len(self.__player_hand) - 1:
                print(f'\033[1;32m{card.capitalize()+",":<14}\033[m', end='')
            else:
                print(f'\033[1;32m{card.capitalize():<14}\033[m', end='')
            count += 1
        print(f'\033[1;33m{"| total: %s":<14}\033[m' % self.__calculate_points)

    @property
    def __calculate_points(self):
        card_values = {
            'King': 10, 'Queen': 10, 'Valet': 10, 'ace': {}
        }
        index = 0
        self.__player_points = 0
        for card in self.__player_hand:
            try:
                if match('((King|Queen|Valet))', card):
                    self.__player_points += card_values[card.split(' ')[
                        0]]
                elif match('((Ace))', card):
                    card_values['ace'][card] = self.__choosen_ace_value[index]
                    self.__player_points += self.__choosen_ace_value[index]
                    index += 1
                else:
                    self.__player_points += int(findall('[0-9]{1,2}', card)[0])
            except Exception:
                pass
        return self.__player_points

    @property
    def cash(self):
        return self.__player_cash

    @property
    def hand(self):
        return self.__player_hand

    @cash.setter
    def cash(self, new_value: int | float) -> None:
        self.__player_cash = new_value

    @hand.setter
    def hand(self, card: str) -> None:
        self.__player_hand.append(card)

    @hand.deleter
    def hand(self) -> None:
        del self.__player_hand[len(self.__player_hand) - 1]

    @__calculate_points.getter
    def getPoints(self):
        return self.__player_points
