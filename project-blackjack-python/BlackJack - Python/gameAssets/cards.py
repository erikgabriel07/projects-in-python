from random import shuffle, choice


class Card:

    def __init__(self):
        self.__deck = self.__create_deck(self.__deck_structure, self.__deck_length)
        shuffle(self.__deck)

    @staticmethod
    def __create_deck(structure, structure_length):
        sample = []

        const_value = 2
        for i in structure['cards']:
            for key, value in structure_length['card'].items():
                if i == key:
                    if not i in ['King', 'Queen', 'Valet', 'ace']:
                        sample += [f'{key} {const_value + _}' for _ in range(value)]
                    else:
                        sample += [f'{key} {structure['cards'][_]}' for _ in range(value)]
        return sample

    def initialize_player_hand(self, player) -> None:
        while True:
            try:
                for _ in range(2):
                    card = choice(self.__deck)
                    self.__deck.remove(card)
                    player.hand = card
                break
            except Exception:
                self.__deck = self.__create_deck(self.__deck_structure, self.__deck_length)
                continue
    
    def initialize_dealer_hand(self, dealer) -> None:
        while True:
            try:
                card = choice(self.__deck)
                self.__deck.remove(card)
                dealer.hand = card
                dealer.hand = 'HIDDEN'
                card = choice(self.__deck)
                self.__deck.remove(card)
                dealer._hidden_card = card
                break
            except Exception:
                self.__deck = self.__create_deck(self.__deck_structure, self.__deck_length)
                continue
    
    def shuffle_deck(self) -> None:
        shuffle(self.__deck)
    
    def new_card(self):
        while True:
            try:
                card = choice(self.__deck)
                self.__deck.remove(card)
                return card
            except Exception:
                self.__deck = self.__create_deck(self.__deck_structure, self.__deck_length)
                continue

    def clear_hands(self, *players):
        for player in players:
            hand_length = len(player.hand)
            for card in player.hand:
                for _ in range(hand_length):
                    del player.hand
                self.__deck.append(card)
    
    @property
    def deck(self):
        return self.__deck

    __deck_structure = {
        'cards': [
            'Club', 'Diamond', 'Hearts', 'Spades', 'King', 'Queen', 'Valet', 'ace'
        ]
    }

    __deck_length = {
        'card': {
            'Club': 9,
            'Diamond': 9,
            'Hearts': 9,
            'Spades': 9,
            'King': 4,
            'Queen': 4,
            'Valet': 4,
            'ace': 4,
        }
    }