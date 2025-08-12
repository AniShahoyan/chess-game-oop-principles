from abc import ABC, abstractmethod
import random

class Piece:
    def __init__(self, position, color):

        self.__position = position
        self.__color = color
        
    def get_position(self):
        return self.__position
    
    def get_color(self):

        return self.__color
        
    @abstractmethod
    def available_moves(self, board):
        pass

class King(Piece):        
    def available_moves(self, board):
        moves = []
        board_size = len(board)
        x, y = self.get_position()
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < board_size and 0 <= new_y < board_size:
                    target = board[new_x][new_y]
                    if target == " " or target.get_color() != self.get_color():
                        moves.append(self.index_to_chess(new_x, new_y))  # Call on 'self' instead
        return moves

class King(Piece):        
    def available_moves(self, board):
        moves = []
        board_size = len(board.grid)  # Access grid from the ChessSimple instance
        x, y = self.get_position()
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < board_size and 0 <= new_y < board_size:
                    target = board.grid[new_x][new_y]  # Access grid here
                    if target == " " or target.get_color() != self.get_color():
                        moves.append(board.index_to_chess(new_x, new_y))  # Corrected call
        return moves


class Queen(Piece):        
    def available_moves(self, board):
        moves = []
        board_size = len(board.grid)  # Access grid from the ChessSimple instance
        x, y = self.get_position()
        
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dx, dy in directions:
            new_x, new_y = x, y
            while True:
                new_x += dx
                new_y += dy
                
                if not (0 <= new_x < board_size and 0 <= new_y < board_size):
                    break
                
                target = board.grid[new_x][new_y]  # Access grid here
                if target == " ":
                    moves.append(board.index_to_chess(new_x, new_y))  # Corrected call
                else:
                    if target.get_color() != self.get_color():
                        moves.append(board.index_to_chess(new_x, new_y))  # Corrected call
                    break
        return moves


class Knight(Piece):
    def available_moves(self, board):
        moves = []
        board_size = len(board.grid)  # Access grid from the ChessSimple instance
        x, y = self.get_position()
        
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in knight_moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                target = board.grid[new_x][new_y]  # Access grid here
                if target == " " or target.get_color() != self.get_color():
                    moves.append(board.index_to_chess(new_x, new_y))  # Corrected call
        return moves


class ChessSimple:
    def __init__(self):
        self.grid_size = 8
        self.grid = [[" " for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.setup_random_pieces()
        self.current_turn = random.choice(['w', 'b'])

    def chess_to_index(self, chess_position):
        column = chess_position[0].upper()  
        row = chess_position[1]
        x = ord(column) - ord('A')
        y = 8 - int(row)
        return y, x

    def index_to_chess(self, x, y):
        column = chr(y + ord('A'))
        row = 8 - x
        return f"{column}{row}"

    def setup_random_pieces(self):
        piece_classes = [King, Queen, Knight]
        colors = ['w', 'b']
        
        for color in colors:
            for piece_class in piece_classes:
                num_pieces = random.randint(1, 4)
                placed_pieces = 0
                while placed_pieces < num_pieces:
                    x, y = random.randint(0, 7), random.randint(0, 7)
                    if self.grid[x][y] == " ":
                        self.grid[x][y] = piece_class((x, y), color)
                        placed_pieces += 1

    def add_piece(self, piece_class, position, color):
        x, y = self.chess_to_index(position)
        piece = piece_class((x,y), color)
        self.grid[x][y] = piece
        
    def remove_piece(self, piece):
        x, y = piece.get_position()
        self.grid[x][y] = " "
        
    def display_grid(self):
        column_labels = "    " + "   ".join("A B C D E F G H".split()) + "    "
        horizontal_line = "  +" + "---+" * self.grid_size

        print(f"Current turn: {'White' if self.current_turn == 'w' else 'Black'}")
        print(column_labels)  
        print(horizontal_line)
        for i in range(self.grid_size):
            row_label = f"{8 - i} " 
            row_elements = []
            for j in range(self.grid_size):
                piece = self.grid[i][j]
                if isinstance(piece, King):
                    row_elements.append(" K " if piece.get_color() == "b" else " k ")
                elif isinstance(piece, Queen):
                    row_elements.append(" Q " if piece.get_color() == "b" else " q ")
                elif isinstance(piece, Knight):
                    row_elements.append(" N " if piece.get_color() == "b" else " n ")
                else:
                    row_elements.append("   ")
            
            print(row_label + "|" + "|".join(row_elements) + "| " + row_label)  
            print(horizontal_line)
        
        print(column_labels)  

    def get_available_moves(self, piece):
        return piece.available_moves(self)

    def make_move(self, piece, target_pos):
        x, y = self.chess_to_index(target_pos)
        self.grid[x][y] = piece
        old_x, old_y = piece.get_position()
        self.grid[old_x][old_y] = " "
        piece._Piece__position = (x, y)  

    def is_game_over(self):
        white_pieces = sum(1 for row in self.grid for piece in row if isinstance(piece, Piece) and piece.get_color() == 'w')
        black_pieces = sum(1 for row in self.grid for piece in row if isinstance(piece, Piece) and piece.get_color() == 'b')
        return white_pieces == 0 or black_pieces == 0

    def switch_turn(self):
        self.current_turn = 'b' if self.current_turn == 'w' else 'w'

    def get_piece_at_position(self, position):
        
        x, y = self.chess_to_index(position)
        return self.grid[x][y] if self.grid[x][y] != " " else None

    def player_turn(self):
        while True:
            print(f"\nIt's {'White' if self.current_turn == 'w' else 'Black'}'s turn.")
            self.display_grid()
            
            piece_position = input(f"Enter the position of the piece you want to move (or 'cancel' to choose another piece): ").strip().upper()
            
            if piece_position == 'CANCEL':
                continue
            
            piece = self.get_piece_at_position(piece_position)
            
            if not piece or piece.get_color() != self.current_turn:
                print("Invalid piece. Try again.")
                continue
            
            available_moves = self.get_available_moves(piece)
            
            if not available_moves:
                print("This piece has no valid moves. Choose another piece.")
                continue
            
            print("Available moves:", ", ".join(available_moves))
            
            target_pos = input(f"Select the target position (or 'cancel' to choose another piece): ").strip().upper()
            
            if target_pos == 'CANCEL':
                continue
            
            if target_pos in available_moves:
                self.make_move(piece, target_pos)
                self.switch_turn()
                break
            else:
                print("Invalid move. Try again.")

    def play(self):
        while not self.is_game_over():
            self.player_turn()

        self.display_grid()
        print(f"Game Over! {'White' if self.current_turn == 'b' else 'Black'} wins!")


chess_game = ChessSimple()
chess_game.play()
