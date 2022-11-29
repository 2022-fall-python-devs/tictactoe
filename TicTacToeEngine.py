import numpy
from TicTacToeBoard import *


# A class that plays many games of tic-tac-toe.
class TicTacToeEngine(TicTacToeBoard):

    NUM_SQUARES = 9 # Number of squares on a tic-tac-toe board.

    def start(self):
        self.__board = TicTacToeBoard()
        # Create the board.

        self.clear_board()
        self.total_x_wins = 0.0
        self.total_o_wins = 0.0
        self.total_ties = 0.0

        response = 'y'
        winner = 0
        game_plays = []

        # Play a bunch of games...
        while response != 'n':
            # Play!
            self.__play_single_game()
            if (winner == 1):
                self.total_x_wins += 1
            elif (winner == 2):
                self.total_o_wins += 1
            else:
                self.total_ties += 1

            numpy.set_printoptions(precision=3)

            if winner == 0:
                print('The game was a tie.')
            else:
                print("The winner was {0}!".format(winner))
            total = self.total_x_wins + self.total_o_wins + self.total_ties
            print('% x wins: {0}, % o wins: {1}, % ties: {2}'.format(self.total_x_wins/total, self.total_o_wins/total, self.total_ties/total))
            response = input('Play again? (y/n) ')
            self.__board.clear_board()


    def __play_single_game(self):
        winner = 3
        # Numbers the spots on the tic-tac-toe board from 0 to 8. When a spot is played, it is
        # removed from this list.
        num_plays = 0
        single_game_is_done = False
        # The game_plays list will hold all the moves for a single game in a list in the order in
        # which they were played.
        game_plays = list()
        board = numpy.zeros((1, 9), dtype=float)
        # The game_plays list holds all the moves for a single game in a list in the order
        # in which they were played. __print_game_plays will display the board states for
        # all the moves.
        #__print_game_plays(game_plays)
        while (not single_game_is_done):
            # The player variable oscillates between 1 and 2. 1 represents X's. 2 represents O's.
            for player in range(1,3):
                if (single_game_is_done or (num_plays > 8)):
                    # It seems silly to check if single_game_is_done and then set the same flag,
                    # but it gets us around the problem where the previous for loop may loop
                    # again, even if the game is won. Just trust me, we need it.
                    single_game_is_done = True
                else:
                    next_play = int(input(f'Player {player}, which space (1-9)? ')) - 1
                    while (next_play in game_plays) or (next_play < 0) or (next_play > 8):
                        next_play = int(input(f'Player {player}, which space (1-9)? '))
                    num_plays += 1

                    # Set the square to an X or an O.
                    self.__board.set_square(next_play, player)
                    board[0][next_play] = player

                    game_plays.append(next_play)

                    # The game_plays list holds all the moves for a single game in a list in the order
                    # in which they were played. __print_game_plays will display the board states for
                    # all the moves.
                    self.__print_game_plays(game_plays)

                    single_game_is_done = (num_plays == 9)

                    if (self.__board.check_for_win(player) == True):
                        winner = player
                        single_game_is_done = True

        return (winner, game_plays)


    def __get_square_marker(self, square):
        if (square == 0):
            return ' '
        elif (square == 1):
            return 'X'
        else:
            return 'O'


    # The following prints out each play in the game. Since it's difficult, I did not introduce any
    # bugs to it. You should not need to instrument or make any changes to it.
    def __print_game_plays(self, game_plays, probabilities_list = None):
        # Create several game states; one for each play.
        game_states = [[0] * self.NUM_SQUARES for partial_board_it in range(len(game_plays))]

        # This is a numbered list of all the board states in the game. For example, if the player
        # won on play 5, it would contain [0,1,2,3,4]
        board_combos = list(range(0, len(game_plays)))

        # This loop is a little mind-bending. It puts the first play in all the game states. Then it
        # puts the second play in all the game states except the first (because the first play does not
        # have the second play in its board). And so on.
        play_index = 0
        # Every time we add a play, we drop one of the board states. It will hit 0 after all the
        # plays have been stored in the game states.
        while (len(board_combos) > 0):
            # This is the mind-bending part. Say we're on play 3 of 5 (0-based). That means we want
            # to add this play to game states 2, 3 and 4 so the for loop will iterate from 2 to 4. Then
            # with the next iteration of the above while, the for loop will iterate over 3 and 4,
            # and then finally just 4.
            for board_it in range(board_combos.pop(0), len(game_plays)):
                # The right-hand side is setting the value to 1 or 2 (X or O).
                game_states[board_it][game_plays[play_index]] = (play_index % 2) + 1
            play_index += 1

        if (not probabilities_list is None):
            probabilities_board = [0] * self.NUM_SQUARES
            counter = 0
            for (game_index, game_play) in enumerate(game_plays):
                probabilities_board[game_plays[game_index]] = probabilities_list[counter]
                counter += 1

        print()
        # Print out the top row of all the game states, except the last. Note that these prints do not have a newline.
        print('1|2|3 ', end=" ")
        for board_it in range(0, len(game_plays)):
            print(self.__get_square_marker(game_states[board_it][0]) + '|' + self.__get_square_marker(game_states[board_it][1]) + '|' + self.__get_square_marker(game_states[board_it][2]) + ' ', end=" ")
        # Now print out the last board, along with a newline character.
        if (not probabilities_list is None):
            print('{:+.6f}'.format(probabilities_board[0]) + '|' + '{:+.6f}'.format(probabilities_board[1]) + '|' + '{:+.6f}'.format(probabilities_board[2]) + ' ', end=" ")
        print()

        # Now do the same for the middle row...
        print('4|5|6 ', end=" ")
        for board_it in range(0, len(game_plays)):
            print(self.__get_square_marker(game_states[board_it][3]) + '|' + self.__get_square_marker(game_states[board_it][4]) + '|' + self.__get_square_marker(game_states[board_it][5]) + ' ', end=" ")
        if (not probabilities_list is None):
            print('{:+.6f}'.format(probabilities_board[3]) + '|' + '{:+.6f}'.format(probabilities_board[4]) + '|' + '{:+.6f}'.format(probabilities_board[5]) + ' ', end=" ")
        print()

        # ...and last row.
        print('7|8|9 ', end=" ")
        for board_it in range(0, len(game_plays)):
            print(self.__get_square_marker(game_states[board_it][6]) + '|' + self.__get_square_marker(game_states[board_it][7]) + '|' + self.__get_square_marker(game_states[board_it][8]) + ' ', end=" ")
        if (not probabilities_list is None):
            print('{:+.6f}'.format(probabilities_board[6]) + '|' + '{:+.6f}'.format(probabilities_board[7]) + '|' + '{:+.6f}'.format(probabilities_board[8]) + ' ', end=" ")
        print()

        print()
