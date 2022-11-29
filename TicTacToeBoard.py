class TicTacToeBoard():


    def __init__(self):
        self.clear_board()


    def clear_board(self):
        self.__squares = [0] * 9


    def set_square(self, next_play, player):
        self.__squares[next_play] = player


    def check_for_win(self, player):
        if ( # Horizontal wins.
            ((self.__squares[0] == player) and (self.__squares[1] == player) and (self.__squares[2] == player))
            or ((self.__squares[3] == player) and (self.__squares[4] == player) and (self.__squares[5] == player))
            or ((self.__squares[6] == player) and (self.__squares[7] == player) and (self.__squares[8] == player))
            # Vertical wins.
            or ((self.__squares[0] == player) and (self.__squares[3] == player) and (self.__squares[6] == player))
            or ((self.__squares[1] == player) and (self.__squares[4] == player) and (self.__squares[7] == player))
            or ((self.__squares[2] == player) and (self.__squares[5] == player) and (self.__squares[8] == player))
            # Criss-cross win.
            or ((self.__squares[0] == player) and (self.__squares[4] == player) and (self.__squares[8] == player))
            # Cross-criss win.
            or ((self.__squares[2] == player) and (self.__squares[4] == player) and (self.__squares[6] == player))):
            return True
        return False
