from random import randint

from icecream import ic



class Interface:
    def __init__(self,game):
        self.game=game()
        self._play=False
        self.how_many_moves=0



    def printBoard(self):
        for name in self.game.get_players():
            print("{} {} => {}".format(name,self.game.get_players()[name][1],self.game.get_players()[name][0]))
        print()
        print("x   " + "".join([str(x).center(3) for x in range(1, self.game.get_size() + 1)]))
        print("y")
        for v in range(1, self.game.get_size() + 1):
            print("{} -".format(str(v).center(3)) + "".join([str(x).center(3) for x in self.game.get_All_Place_In_Landscape_Or_Vertical(v, "landscape")]))
        print()



    def get_move_human_player(self):
        while True:
            text = input("{} Make your moves : ".format(self.how_many_moves)).split(" ")
            if len(text) == 2:
                return [int(x) for x in text]

    def get_move_CPU_player(self):

        return randint(1,15),randint(1,15)


    def startGame(self):
        self._play=True
        gen=self._gen_next_player(list(self.game.get_players()))
        while self._play:
            self.printBoard()
            player=next(gen)

            if list(self.game.get_players())[0]==player:
                x,y=self.get_move_human_player()
            else:
                x,y=self.get_move_CPU_player()

            self.doMove(x,y,self.game.get_players()[player][0])
            if self.game.check_winner(x,y):
                self._play=False
        self.printBoard()
        print(" good job {}".format(player))

    def _gen_next_player(self,l:list):
        while True:
            yield l[self.how_many_moves%len(l)]
            self.how_many_moves+=1

    def doMove(self,x:int,y:int,player:str):
        self.game.make_move(player, x, y)

