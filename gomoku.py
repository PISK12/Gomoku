from config import config


class Board:
    def __init__(self):
        self._players=config["Players"]
        self._blank_place="0"
        self._size=15
        self._how_many_stone_neet_to_win=5
        self._board = {(x, y): self.get_blank() for x in range(1, self.get_size() + 1) for y in range(1, self.get_size() + 1)}

    def get_blank(self):
        return self._blank_place

    def get_players(self) -> dict:
        return self._players

    def get_size(self) -> int:
        return self._size

    def get_board(self) -> dict:
        return self._board

    def get_place(self,x:int,y:int) -> str:
        return self.get_board()[x,y]

    def check_number_exist(self,number) -> bool:
        return 0<number<=self.get_size()

    def get_All_Place_In_Landscape_Or_Vertical(self, number: int, type: str) -> list:
        result = []
        if type == "landscape" or type == "y":
            for x in range(1, self.get_size() + 1):
                result.append(self.get_place(x,number))
        elif type == "vertical" or type == "x":
            for y in range(1, self.get_size() + 1):
                result.append(self.get_place(number,y))
        return result

    def _setStone(self, player:str, x:int, y:int):
        self._board[x, y]=player

    def make_move(self, player:str, x:int, y:int)->bool:
        if self.get_blank()==self.get_place(x,y):
            self._setStone(player, x, y)
            return True
        else:
            return False

    def get_neighbours(self,x:int,y:int,all_neighbours=set())->set:
        neighbours=set({(i+x,z+y) for i in range(-1,2) for z in range(-1,2)
                        if self.check_number_exist(x+i) and self.check_number_exist(y+z)})
        neighbours.remove((x,y))
        neighbours={(i,z) for i,z in neighbours if self.get_place(i,z) == self.get_place(x,y)}
        neighbours=neighbours-all_neighbours
        all_neighbours=all_neighbours | neighbours
        if not len(neighbours):
            return all_neighbours
        for i,z in neighbours:
            all_neighbours=all_neighbours|self.get_neighbours(i,z,all_neighbours)
        return all_neighbours



    def _check_winner_place(self, x:int, y:int)->bool:
        option=[]
        if self.check_number_exist(y-2) and self.check_number_exist(y+2):
            landscape=  [(0,-2), (0,-1), (0,0), (0,1), (0,2)]
            option.append((landscape))
        if self.check_number_exist(x-2) and self.check_number_exist(x+2):
            vertical =  [(-2,0), (-1,0), (0,0), (1,0), (2,0)]
            option.append(vertical)
        if len(option)==2:
            cross1 = [(-2,-2), (-1,-1), (0,0), (1,1), (2,2)]
            cross2 = [(2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2)]
            option.append(cross1)
            option.append(cross2)
        if not len(option):
            return False
        for opt in option:
            if all(self.get_board()[(x + hx, y + hy)] == self.get_board()[x, y] for hx, hy in opt):
                return True
        return False

    def check_winner(self,x:int,y:int)->bool:
        return any(self._check_winner_place(i,z) for i,z in self.get_neighbours(x,y))

