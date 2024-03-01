from gameAssets.player import *
from gameAssets.cards import *
from gameAssets.game import *
from gameAssets.CPU import *
from os import system as console_commands
from time import sleep as wait_for_next_line
from re import sub


def restart_game(MainGame, player, dealer, deck):
    input('Press ENTER to continue...')
    console_commands('cls')
    if (player.cash == 0 or dealer.cash == 0):
        who = player.player_name if player.cash == 0 else dealer.player_name
        print('Endgame!', who, 'run out of cash!')
        MainGame.state = 'Out of Cash'
        MainGame.turn = 'None'
        MainGame.active = False
        input('Press ENTER to finish...')
        return 0
    console_commands('cls')
    print('Starting...')
    MainGame.state, MainGame.turn = 'Running', 'Player'
    deck.clear_hands(player, dealer)
    deck.shuffle_deck()
    deck.initialize_player_hand(player)
    deck.initialize_dealer_hand(dealer)
    player.show_player_hand()
    dealer.show_player_hand()
    input('Press ENTER to continue...')


def force_float(user_float_number):
    while True:
        try:
            user_float_number = float(user_float_number)
            break
        except Exception:
            user_float_number = input('Invalid number! Type number only: ')
            continue
    return user_float_number


def decision_control(player_decision):
    decisions = ['0', '1']
    while player_decision not in decisions:
        player_decision = input('[0] Hit  [1] Stand: ')
    return int(decisions[int(player_decision)])


def check_for_ace(player: Player | CPU, game_control: Game):
    values = {'O': 1, 'E': 11}

    if player.getPoints + 10 == 21:
        game_control.turn, game_control.state = 'None', 'BlackJack'
        ace_value = 'E'

    match player._player_type.upper():
        case 'HUMAN':
            for cards in player.hand:
                while match('((ace))', cards):
                    if game_control.state == 'Running':
                        ace_value = input(
                            'You got an Ace! Choose value:\n[O] 1  [E] 11: ').upper()
                        while ace_value not in ['O', 'E']:
                            ace_value = input(
                                'You got an Ace! Choose value:\n[O] 1  [E] 11: ').upper()
                        player.hand[player.hand.index(cards)] = sub(
                            '((ace))', 'Ace', cards)
                    console_commands('cls')
                    player.chooseAceValue(values[ace_value[0]])
                    player.show_player_hand()
                    break

        case 'CPU':
            for cards in player.hand:
                while match('((ace))', cards):
                    player.chooseAceValue(values[player.ace_value()])
                    try:
                        player.hand[player.hand.index(cards)] = sub(
                            '((ace))', 'Ace', cards)
                    except Exception:
                        break


def check_game_state(game_state, bet, *players):
    match game_state:
        case 'Bust':
            players[1].cash = players[1].cash + (2 * bet)
            print(f'{players[0].player_name} BUST!')

        case 'BlackJack':
            players[0].cash = players[0].cash + (2 * bet)
            print(f'{players[0].player_name} BLACKJACKED!')

        case 'Win':
            players[0].cash = players[0].cash + (2 * bet)
            print(f'{players[0].player_name} WINS!')

        case 'Lose':
            players[1].cash = players[1].cash + (2 * bet)
            print(f'{players[0].player_name} LOSE!')

        case 'Push':
            players[0].cash = players[0].cash + bet
            players[1].cash = players[1].cash + bet
            print('This is a draw!')


def main():
    # Game control
    MainGame = Game(False, None, 'Not Started')

    # Game variables
    initial_cash = 5000
    deck = Card()

    # Players
    player = Player('Player', [], initial_cash, 'human')
    dealer = CPU('Dealer', [], 250_000)

    # Initializing players hands
    deck.initialize_player_hand(player)
    deck.initialize_dealer_hand(dealer)

    # Main Game
    MainGame.active, MainGame.turn, MainGame.state = True, 'Player', 'Running'

    player.show_player_hand()
    wait_for_next_line(1.5)
    dealer.show_player_hand()
    wait_for_next_line(1.5)
    input('Press ENTER to continue...')
    console_commands('cls')

    while MainGame.active:
        match MainGame.turn:
            case 'Player':
                player.show_player_cash()
                player_bet = force_float(input('Your bet: US$'))
                while player_bet > player.cash or player_bet < 100:
                    player_bet = force_float(
                        input("Bets must be between 100 or all of your money: US$"))
                player.cash, dealer.cash = (player.cash - player_bet,
                                            dealer.cash - player_bet
                                            if dealer.cash >= player_bet else 0)

                console_commands('cls')
                print(f'Bet: US${player_bet}')

                while MainGame.turn == 'Player':
                    player.show_player_hand()
                    check_for_ace(player, MainGame)

                    d = 1
                    if player.getPoints < 21:
                        d = decision_control(input('[0] Hit  [1] Stand: '))
                        wait_for_next_line(1.5)

                    match d:
                        case 0:
                            console_commands('cls')
                            if not player.getPoints >= 21:
                                player.hand = deck.new_card()

                        case 1:
                            console_commands('cls')
                            MainGame.turn, MainGame.state = 'Dealer', 'Finished'
                    if player.getPoints == 21:
                        MainGame.state, MainGame.turn = 'BlackJack', 'None'
                        check_game_state(
                            MainGame.state, player_bet, player, dealer)
                        
                    if player.getPoints > 21:
                        MainGame.state, MainGame.turn = 'Bust', 'None'
                        check_game_state(
                            MainGame.state, player_bet, player, dealer)
                wait_for_next_line(1.5)

            case 'Dealer':
                dealer.reveal_card()

                while MainGame.turn == 'Dealer':
                    check_for_ace(dealer, MainGame)
                    dealer.show_player_hand()
                    wait_for_next_line(0.7)
                    dealer.show_player_cash()
                    wait_for_next_line(1.5)

                    if dealer.getPoints >= 17:
                        MainGame.state, MainGame.turn = 'Finished', 'None'

                    match dealer.decision(player):
                        case 'Hit':
                            dealer.hand = deck.new_card()
                        case 'Stand':
                            MainGame.turn, MainGame.state = 'None', 'Finished'
                        case 'Draw':
                            MainGame.turn, MainGame.state = 'None', 'Push'
                        case _:
                            MainGame.turn, MainGame.state = 'None', 'Finished'

                    if dealer.getPoints > 21:
                        MainGame.state, MainGame.turn = 'Bust', 'None'
                        check_game_state(
                            MainGame.state, player_bet, dealer, player)
                    elif dealer.getPoints == 21:
                        MainGame.state, MainGame.turn = 'BlackJack', 'None'
                        check_game_state(
                            MainGame.state, player_bet, dealer, player)
                    input('Press ENTER to continue...')
                    console_commands('cls')

            case _:
                player.show_player_hand()
                dealer.show_player_hand()

                if (player.getPoints > dealer.getPoints and dealer.getPoints <= 21
                        and MainGame.state == 'Finished'):
                    check_game_state('Win', player_bet, player, dealer)

                elif (player.getPoints < dealer.getPoints and dealer.getPoints <= 21
                      and MainGame.state == 'Finished'):
                    check_game_state('Lose', player_bet, player, dealer)

                elif (player.getPoints == dealer.getPoints and dealer.getPoints <= 21
                      and MainGame.state == 'Finished'):
                    check_game_state('Push', player_bet, player, dealer)
                restart_game(MainGame, player, dealer, deck)


if __name__ == '__main__':
    main()
