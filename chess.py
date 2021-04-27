import itertools
import copy
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

num_to_let = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
let_to_num = dict(item[::-1] for item in num_to_let.items())


def validate_square(square):
    return square[0] in range(1, 9) and square[1] in range(1, 9)


def filter_squares(squares):
    return list(filter(validate_square, squares))


class Board:
    
    def __init__(self):
        self.squares = {j: {i: None for i in range(1, 9)} for j in range(1, 9)}
        
    
    def __call__(self, x, y):
        return self.squares[x][y]
        

    def place_piece(self, x, y, piece, color):
        self.squares[x][y] = piece(x, y, color)


    def init_board(self):
        self.place_piece(1, 1, Rook, 'white')
        self.place_piece(2, 1, Knight, 'white')
        self.place_piece(3, 1, Bishop, 'white')
        self.place_piece(4, 1, Queen, 'white')
        self.place_piece(5, 1, King, 'white')
        self.place_piece(6, 1, Bishop, 'white')
        self.place_piece(7, 1, Knight, 'white')
        self.place_piece(8, 1, Rook, 'white')

        for i in range(1, 9):
            self.place_piece(i, 2, Pawn, 'white')

        self.place_piece(1, 8, Rook, 'black')
        self.place_piece(2, 8, Knight, 'black')
        self.place_piece(3, 8, Bishop, 'black')
        self.place_piece(4, 8, Queen, 'black')
        self.place_piece(5, 8, King, 'black')
        self.place_piece(6, 8, Bishop, 'black')
        self.place_piece(7, 8, Knight, 'black')
        self.place_piece(8, 8, Rook, 'black')

        for i in range(1, 9):
            self.place_piece(i, 7, Pawn, 'black')
            
        self.update_pieces_on_board()
        self.last_post = None
        
        self.white_pieces = [(i, j) for i in range(1, 9) for j in range(1, 3)]
        self.black_pieces = [(i, j) for i in range(1, 9) for j in range(7, 9)]


    def clear_board(self):
        for i in range(1, 9):
            for j in range(1, 9):
                self.squares[i][j] = None
                
                
    def reset_board(self):
        self.clear_board()
        self.init_board()


    def update_square(self, x, y, piece):
        self.squares[x][y] = piece
        
        
    def update_pieces_on_board(self):
        for i in range(1, 9):
            for j in range(1, 9):
                target_square = self.squares[i][j]
                if target_square:
                    target_square.update_piece()
                   
    
    def get_king_pos(self, color):
        if color == 'white':
            places = self.white_pieces
        else:
            places = self.black_pieces
            
        for place in places:
            piece = self(*place)
            if isinstance(piece, King):
                return place
                
                
    def handle_take(self, x, y):
        target_square = self.squares[x][y]
        if target_square:
            if target_square.color == 'white':
                self.white_pieces.remove((x, y))
            else:
                self.black_pieces.remove((x, y))
    
    
    def is_takeable_by_player(self, x, y, color):
        if color == 'white':
            places = self.white_pieces
        else:
            places = self.black_pieces
            
        for place in places:
            piece = self(*place)
            if isinstance(piece, Pawn):
                covered_squares = piece.possible_takes
            else:
                covered_squares = piece.legal_moves
            if (x, y) in covered_squares:
                return True

        return False
            
            
class Piece:
    
    def __init__(self, x, y, color):
        if isinstance(x, int):
            self.x = x
        else:
            self.x = let_to_num[x]
        self.y = y
        self.color = color
        self.has_moved = False
        self.update_possible_moves()
        self.update_legal_moves()
        self.legal_takes = []
        self.tran_state = 0
    
    
    def update_possible_moves(self):
        pass
    
    
    def update_pos(self, x, y):
        self.x = x
        self.y = y

    
    def update_piece(self):
        self.update_possible_moves()
        self.update_legal_moves()
    
            
    def move(self, x, y):
        
        x_from = self.x
        y_from = self.y
        color = self.color
        
        if (x, y) in self.legal_moves + self.legal_takes:
            global last_board
            global board
            global turn
            last_board = copy.deepcopy(board)
            
            board.handle_take(x, y)
            
            board.update_square(self.x, self.y, None)
            
            if self.color == 'white':
                board.white_pieces.remove((self.x, self.y))
                board.white_pieces.append((x, y))
            else:
                board.black_pieces.remove((self.x, self.y))
                board.black_pieces.append((x, y))
            
            board.update_square(x, y, self)
            self.update_pos(x, y)
            board.update_pieces_on_board()
        
        else:
            print("Can't move there.")
            return False
        
        if color == 'white':
            if white.is_in_check():
                board = copy.deepcopy(last_board)
                print(f'{color} king is in check.')
                return False
            else:
                print(vars(self))
                self.has_moved = True
                turn = 'black'
                return True
            
        elif color == 'black':
            if black.is_in_check():
                board = copy.deepcopy(last_board)
                print(f'{color} king is in check.')
                return False
            else:
                print(vars(self))
                self.has_moved = True
                turn = 'white'
                return True
            
    
    
    def update_unblockable_legal_moves(self):
        
        legal_moves = []
        
        for move in self.possible_moves:
            target_square = board(move[0], move[1])
            if not target_square or target_square.color != self.color:
                legal_moves.append(move)
                
        self.legal_moves = legal_moves
    
    
    def update_blockable_legal_moves(self):
        
        legal_moves = []
        
        for move_dir in self.possible_moves:
            for i, move in enumerate(move_dir):
                target_square = board(move[0], move[1])
                if target_square:
                    if not isinstance(self, Pawn):
                        if target_square.color == self.color:
                            legal_moves.append(move_dir[:i])
                        else:
                            legal_moves.append(move_dir[:i+1])
                    
                    else:
                        legal_moves.append(move_dir[:i])
                        
                    break
            else:
                legal_moves.append(move_dir)
                
        self.legal_moves = list(itertools.chain(*legal_moves))
        
        
    def update_legal_takes(self):
        pass
        
            
    def translate_squares(self):
        if self.tran_state == 0:
            self.x = num_to_let[self.x]
            self.possible_moves = [[(num_to_let[square[0]], square[1]) for square in dir_] for dir_ in self.possible_moves]
            
            self.tran_state = 1
            
        else:
            self.x = let_to_num[self.x]
            self.possible_moves = [[(let_to_num[square[0]], square[1]) for square in dir_] for dir_ in self.possible_moves]
            
            self.tran_state = 0
    
    
    def __repr__(self):
        return f'{self.color} {self.__class__.__name__.lower()}'



class Rook(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.init_pos = (self.x, self.y)
        
        
    def update_possible_moves(self):
        directions = []
        
        x = self.x
        y = self.y
        
        left = [(i, y) for i in range(x-1, 0, -1)]
        right = [(i, y) for i in range(x+1, 9)]
        up = [(x, j) for j in range(y+1, 9)]
        down = [(x, j) for j in range(y-1, 0, -1)]
        
        directions.append(left)
        directions.append(right)
        directions.append(up)
        directions.append(down)
        
        self.possible_moves = directions
    
    
    def move(self, x, y):
        return super().move(x, y)
        
    
    def update_legal_moves(self):
        super().update_blockable_legal_moves()
    
    
    def translate_squares(self):
        if self.tran_state == 0:
            self.init_pos = (num_to_let[self.init_pos[0]], self.init_pos[1])
        else:
            self.init_pos = (let_to_num[self.init_pos[0]], self.init_pos[1])
        super().translate_squares()
            


class Bishop(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
        
    def update_possible_moves(self):
        directions = [[], [], [], []]
        
        
        for k in range(4):
            i = self.x
            j = self.y
            
            while True:
                if k == 0:
                    i -= 1
                    j += 1
                elif k == 1:
                    i += 1
                    j += 1
                elif k == 2:
                    i -= 1
                    j -= 1
                elif k == 3:
                    i += 1
                    j -= 1
                
                if validate_square((i, j)):
                    directions[k].append((i, j))
                else:
                    break
        
        
        self.possible_moves = directions
    
    
    def move(self, x, y):
        return super().move(x, y)
        
    
    def update_legal_moves(self):
        super().update_blockable_legal_moves()
    
    
    def translate_squares(self):
        super().translate_squares()
        
        

class Queen(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
        
    def update_possible_moves(self):
        r = Rook(self.x, self.y, self.color)
        b = Bishop(self.x, self.y, self.color)
        
        directions = r.possible_moves + b.possible_moves
        
        
        self.possible_moves = directions
    
    
    def move(self, x, y):
        return super().move(x, y)
        
    
    def update_legal_moves(self):
        super().update_blockable_legal_moves()
    
    
    def translate_squares(self):
        super().translate_squares()



class King(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        in_check = False
        is_mated = False
        self.can_long_castle = False
        self.can_short_castle = False
        
        
    def update_possible_moves(self):
        q = Queen(self.x, self.y, self.color)
        
        directions = [square[0] for square in q.possible_moves if square]
        
        
        self.possible_moves = directions
    
    
    def move(self, x, y):
        return super().move(x, y)
        
    
    def castle_short(self):
        color = self.color
        
        global turn
        
        if color == 'white':
            board.update_square(5, 1, None)
            board.update_square(7, 1, self)
            self.update_pos(7, 1)
            board.white_pieces.remove((5, 1))
            board.white_pieces.append((7, 1))
            
            right_rook = board(8, 1)
            board.update_square(8, 1, None)
            board.update_square(6, 1, right_rook)
            right_rook.update_pos(6, 1)
            board.white_pieces.remove((8, 1))
            board.white_pieces.append((6, 1))
            
            turn = 'black'
            
        else:
            board.update_square(5, 8, None)
            board.update_square(7, 8, self)
            self.update_pos(7, 8)
            board.black_pieces.remove((5, 8))
            board.black_pieces.append((7, 8))
            
            right_rook = board(8, 8)
            board.update_square(8, 8, None)
            board.update_square(6, 8, right_rook)
            right_rook.update_pos(6, 8)
            board.black_pieces.remove((8, 8))
            board.black_pieces.append((6, 8))
            
            turn = 'white'
            
        self.has_moved = True
        right_rook.has_moved = True
        board.update_pieces_on_board()
        
        
    def castle_long(self):
        color = self.color
        
        global turn
        
        if color == 'white':
            board.update_square(5, 1, None)
            board.update_square(3, 1, self)
            self.update_pos(3, 1)
            board.white_pieces.remove((5, 1))
            board.white_pieces.append((3, 1))
            
            left_rook = board(1, 1)
            board.update_square(1, 1, None)
            board.update_square(4, 1, left_rook)
            left_rook.update_pos(4, 1)
            board.white_pieces.remove((1, 1))
            board.white_pieces.append((4, 1))
            
            turn = 'black'
            
        else:
            board.update_square(5, 8, None)
            board.update_square(3, 8, self)
            self.update_pos(3, 8)
            board.black_pieces.remove((5, 8))
            board.black_pieces.append((3, 8))
            
            left_rook = board(1, 8)
            board.update_square(1, 8, None)
            board.update_square(4, 8, left_rook)
            left_rook.update_pos(4, 8)
            board.black_pieces.remove((1, 8))
            board.black_pieces.append((4, 8))
            
            turn = 'white'
            
        self.has_moved = True
        left_rook.has_moved = True
        board.update_pieces_on_board()
        
    
    def update_legal_moves(self):
        super().update_unblockable_legal_moves()
        
    
    def is_in_check(self):
        x = self.x
        y = self.y
        color = 'black' if self.color == 'white' else 'white'
        
        return board.is_takeable_by_player(x, y, color)
        
        
    
    
    def translate_squares(self):
        if self.tran_state == 0:
            self.x = num_to_let[self.x]
            self.possible_moves = [(num_to_let[square[0]], square[1]) for square in self.possible_moves]
            
            self.tran_state = 1
            
        else:
            self.x = let_to_num[self.x]
            self.possible_moves = [(let_to_num[square[0]], square[1]) for square in self.possible_moves]
            
            self.tran_state = 0



class Knight(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
        
    def update_possible_moves(self):
        
        x = self.x
        y = self.y
        
        directions = []
        
        if (u := x-1) in range(1, 9) and (v := y+2) in range(1, 9):
            directions.append((u, v))
        if (u := x+1) in range(1, 9) and (v := y+2) in range(1, 9):
            directions.append((u, v))
        if (u := x-2) in range(1, 9) and (v := y+1) in range(1, 9):
            directions.append((u, v))
        if (u := x+2) in range(1, 9) and (v := y+1) in range(1, 9):
            directions.append((u, v))
        if (u := x-2) in range(1, 9) and (v := y-1) in range(1, 9):
            directions.append((u, v))
        if (u := x+2) in range(1, 9) and (v := y-1) in range(1, 9):
            directions.append((u, v))
        if (u := x-1) in range(1, 9) and (v := y-2) in range(1, 9):
            directions.append((u, v))
        if (u := x+1) in range(1, 9) and (v := y-2) in range(1, 9):
            directions.append((u, v))
        
        self.possible_moves = directions
    
    
    def move(self, x, y):
        return super().move(x, y)
        
    
    def update_legal_moves(self):
        super().update_unblockable_legal_moves()
    
    
    def translate_squares(self):
        if self.tran_state == 0:
            self.x = num_to_let[self.x]
            self.possible_moves = [(num_to_let[square[0]], square[1]) for square in self.possible_moves]
            
            self.tran_state = 1
            
        else:
            self.x = let_to_num[self.x]
            self.possible_moves = [(let_to_num[square[0]], square[1]) for square in self.possible_moves]
            
            self.tran_state = 0



class Pawn(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.update_possible_takes()
        self.update_legal_takes()
        
        
    def update_possible_moves(self):
        
        x = self.x
        y = self.y
        color = self.color
        
        if color == 'white':
            if y == 2:
                self.possible_moves = [filter_squares([(x, y+1), (x, y+2)])]
            else:
                self.possible_moves = [filter_squares([(x, y+1)])]
            
        else:
            if y == 7:
                self.possible_moves = [filter_squares([(x, y-1), (x, y-2)])]
            else:
                self.possible_moves = [filter_squares([(x, y-1)])]
    
    
    def update_possible_takes(self):
        x = self.x
        y = self.y
        color = self.color
    
        if color == 'white':
            self.possible_takes = filter_squares([(x-1, y+1), (x+1, y+1)])
            
        else:
            self.possible_takes = filter_squares([(x-1, y-1), (x+1, y-1)])
            
            
    def update_piece(self):
        super().update_piece()
        self.update_possible_takes()
        self.update_legal_takes()
    
            
    def move(self, x, y):
        return super().move(x, y)
        
        
    def update_legal_moves(self):
        x = self.x
        y = self.y
        color = self.color
        
        if color == 'white':
            super().update_blockable_legal_moves()            
                    
        else:
            super().update_blockable_legal_moves()
        
        
    def update_legal_takes(self):
        
        legal_takes = []
        
        for take in self.possible_takes:
            target_square = board(take[0], take[1])
            if target_square and target_square.color != self.color:
                legal_takes.append((take[0], take[1]))
                
        self.legal_takes = legal_takes
    
    
    def translate_squares(self):
        if self.tran_state == 0:
            self.x = num_to_let[self.x]
            self.possible_moves = [(num_to_let[square[0]], square[1]) for square in self.possible_moves]
            
            self.possible_takes = [(num_to_let[take[0]], take[1]) for take in self.possible_takes]
            
            self.tran_state = 1
            
        else:
            self.x = let_to_num[self.x]
            self.possible_moves = [(let_to_num[square[0]], square[1]) for square in self.possible_moves]
            
            self.possible_takes = [(let_to_num[take[0]], take[1]) for take in self.possible_takes]
            
            self.tran_state = 0
            
           
        
class Player:
    
    def __init__(self, color):
        self.color = color
        self.king_pos = board.get_king_pos(self.color)
        self.in_check = False
        
    
    def is_in_check(self):
        self.king_pos = board.get_king_pos(self.color)
        king_x = self.king_pos[0]
        king_y = self.king_pos[1]
        
        return board(king_x, king_y).is_in_check()
    
    
    def move_piece(self, x_from, y_from, x_to, y_to):
        print(locals())

        if turn != self.color:
            print('Not your turn.')
            return False
        
        if self.color == 'white':
            places = board.white_pieces
        else:
            places = board.black_pieces
            
        if (x_from, y_from) not in places:
            print(f'No {self.color} piece found on ({x_from}, {y_from}).')
            return False
        
        piece = board(x_from, y_from)
        return piece.move(x_to, y_to)
        
    
    def castle_short(self):
        color = self.color
        
        if turn != color:
            return 'Not your turn.'
        
        king_pos = board.get_king_pos(color)
        king = board(*king_pos)
        
        right_rook = board(8, 1) if color == 'white' else board(8, 8)
        
        if king.has_moved or right_rook.has_moved:
            return "Can't castle short."
        
          
        if color == 'white':  
            if board(6, 1) or board(7, 1):
                return "Can't castle short."
            
            if board.is_takeable_by_player(5, 1, 'black') or board.is_takeable_by_player(6, 1, 'black')\
                or board.is_takeable_by_player(7, 1, 'black'):
                return "Can't castle short."
            
        else:
            if board(6, 8) or board(7, 8):
                return "Can't castle short."
            
            if board.is_takeable_by_player(5, 8, 'white') or board.is_takeable_by_player(6, 8, 'white')\
                or board.is_takeable_by_player(7, 8, 'white'):
                return "Can't castle short."
        
        king.castle_short()
        print(f'{color} castled short.')

        
    def castle_long(self):
        color = self.color
        
        if turn != color:
            return 'Not your turn.'
        
        king_pos = board.get_king_pos(color)
        king = board(*king_pos)
        
        left_rook = board(1, 1) if color == 'white' else board(1, 8)
        
        if king.has_moved or left_rook.has_moved:
            return "Can't castle long."
        
          
        if color == 'white':  
            if board(4, 1) or board(3, 1):
                return "Can't castle long."
            
            if board.is_takeable_by_player(5, 1, 'black') or board.is_takeable_by_player(4, 1, 'black')\
                or board.is_takeable_by_player(3, 1, 'black'):
                return "Can't castle long."
            
        else:
            if board(4, 8) or board(3, 8):
                return "Can't castle long."
            
            if board.is_takeable_by_player(5, 8, 'white') or board.is_takeable_by_player(4, 8, 'white')\
                or board.is_takeable_by_player(3, 8, 'white'):
                return "Can't castle long."
        
        king.castle_long()
        print(f'{color} castled long.')
        


turn = 'white'

board = Board()
board.reset_board()

last_board = None

white = Player('white')
black = Player('black')




mouse_x = None
mouse_y = None


def get_mouse_pos(event):
    global mouse_x
    global mouse_y
    mouse_x = window.winfo_pointerx() - window.winfo_rootx()
    mouse_y = window.winfo_pointery() - window.winfo_rooty()
    #print('Mouse pos: {}, {}'.format(mouse_x, mouse_y))
    square = get_square_from_point(mouse_x-50, mouse_y-50)
    square = transform_square(*square)
    #print(f'Square: {square}')
    #print(f'Square middle: {get_point_from_square(*square)}')
    #print('\n')



def transform_square(x, y):
    return x+1, 8-y


def get_square_from_point(x, y):
    x = max(51, min(x, 599))
    y = max(51, min(y, 599))
    return x // 75, y // 75


def get_point_from_square(x, y):

    x -= 1
    y = 8-y

    square = 50 + 75*x + 75/2, 50 + 75*y + 75/2

    return square


def mouse_over_board():
    return (51 <= mouse_x <= 649) and (51 <= mouse_y <= 649)


class Piece_image:
    
    def __init__(self, image_file):
        self.piece = Image.open(image_file)
        self.piece = self.piece.resize((50, 50))
        self.render_piece = ImageTk.PhotoImage(self.piece)
        self.piece = ttk.Label(image=self.render_piece)
        
        self.piece.bind("<ButtonPress-1>", self.on_start)
        self.piece.bind("<B1-Motion>", self.on_drag)
        #self.piece.bind("<B1-Motion>", get_mouse_pos)
        self.piece.bind("<ButtonRelease-1>", self.on_drop)

        
    
    def place_on_board(self, x, y):
        square = get_square_from_point(x, y)
        x_ = square[0]+1
        y_ = 8-square[1]

        print(x_, y_)

        x_coord = square[0]*75 + 12
        y_coord = square[1]*75 + 12
        
        self.x = x
        self.y = y

        self.piece.place(x=50+x_coord, y=50+y_coord)
        
        
    def on_start(self, event):
        self.piece.place(x=mouse_x-25, y=mouse_y-25)
    
    
    def on_drag(self, event):
        self.piece.place(x=mouse_x-25, y=mouse_y-25)
    
    
    def on_drop(self, event):

        x_from = self.backend.x
        y_from = self.backend.y
        color = self.backend.color
        point_x, point_y = get_point_from_square(x_from, y_from)

        if mouse_over_board(): 

            square = get_square_from_point(mouse_x-50, mouse_y-50)

            square = transform_square(*square)

            print(square)

            print(color)

            if color == 'white':
                possible_move = white.move_piece(x_from, y_from, square[0], square[1])
            else:
                possible_move = black.move_piece(x_from, y_from, square[0], square[1])


            print(possible_move)
            
            if possible_move:
                print(f'------- {color} has moved --------')
                self.place_on_board(x=mouse_x-50, y=mouse_y-50)
                self.backend = board(square[0], square[1])
                self.x = mouse_x
                self.y = mouse_y
            else:
                self.backend = board(x_from, y_from)
                self.place_on_board(x=point_x-50, y=point_y-50)

        else:
            self.place_on_board(x=point_x-50, y=point_y-50)


def add_piece_to_board(piece, color, square_x, square_y):
    x, y = get_point_from_square(square_x, square_y)

    piece_pic = Piece_image(f'{color}_{piece.__name__.lower()}.png')

    piece_pic.backend = board(square_x, square_y)

    piece_pic.place_on_board(x-50, y-50)

        

window = tk.Tk()
window.geometry("1000x700")

board_canvas = tk.Canvas(window, bg="white", height=600, width=600)
board_canvas.place(x=50, y=50)

window.bind('<Motion>', get_mouse_pos)
window.bind('<B1-Motion>', get_mouse_pos)


for j in range(8):
    for i in range(8):
        color = 'brown' if (i+j) % 2 else 'white'
        board_canvas.create_rectangle(j*75, i*75, (j+1) * 75, (i+1)*75, fill=color)

        
        
#white_rook = Piece_image('white_rook.png')
#white_rook.place_on_board(100, 100)

#turn = 'white'

for i in range(1, 9):
    for j in range(1, 9):
        if board(i, j):
            piece = board(i, j)
            add_piece_to_board(piece.__class__, piece.color, i, j)


#add_piece_to_board(Knight, 'white', 2, 1)
#add_piece_to_board(Knight, 'black', 2, 8)

        
window.mainloop()