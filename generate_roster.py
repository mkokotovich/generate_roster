import random

MAX_ON_FIELD = 6
POSITIONS = [x for x in range(MAX_ON_FIELD)]

class Player:
    playerId = "" 
    positionsPlayed = []

    def __init__(self, playerId):
        self.playerId = playerId
        self.positionsPlayed = []

    def __str__(self):
        return self.playerId

    def addPosition(self, position):
        self.positionsPlayed.append(position)

    def countPosition(self, position):
        return self.positionsPlayed.count(position)

class Line:
    numberOfPlayers = 0
    playing = {}
    sitting = []

    def __init__(self, numberOfPlayers):
        self.numberOfPlayers=numberOfPlayers
        self.playing = {}
        self.sitting = []

    def __str__(self):
        msg =  "Playing: {0}\nSitting: {1}\n".format(", ".join(str(player) for position,player in self.playing.items()), ", ".join(str(player) for player in self.sitting))
        return msg

    def addPlayer(self, player):
        if (len(self.playing) < MAX_ON_FIELD):
            self.addToPlaying(player)
        else:
            self.addToSitting(player)

    def addToPosition(self, player, position):
        if (position >= MAX_ON_FIELD):
            print("Error, invalid position {0}, unable to add player {1}".format(position, player))
            return
        if position in self.playing:
            print("Error, position {0} is already taken".format(position))
            return
        self.playing[position] = player
        player.addPosition(position)

    def addToPlaying(self, player):
        if (len(self.playing) + len(self.sitting) >= self.numberOfPlayers):
            print("Error, too many players on line, can not add player {0}".format(player))
            return
        if (len(self.playing) >= MAX_ON_FIELD):
            print("Error, too many players on the field, can not add player {0}".format(player))
            return
        for position in POSITIONS:
            if position not in self.playing:
                self.playing[position] = player
                player.addPosition(position)
                return

    def addToSitting(self, player):
        if (len(self.playing) + len(self.sitting) >= self.numberOfPlayers):
            print("Error, too many players on line, can not add player {0}".format(player))
            return
        if (len(self.sitting) >= self.numberOfPlayers - MAX_ON_FIELD):
            print("Error, too many players sitting, can not add player {0}".format(player))
            return
        self.sitting.append(player)
    
class Roster:
    numberOfPlayers = 0
    numberOfLines = 0
    lines = []

    def __init__(self, numberOfPlayers, numberOfLines=8):
        self.numberOfPlayers=numberOfPlayers
        self.numberOfLines = numberOfLines
        self.lines = []

    def __str__(self):
        msg = ""
        for i in range(0, self.numberOfLines-1):
            msg += "Line {0}:\n".format(i+1)
            msg += str(self.lines[i])
        return msg

    def generate_optimized(self):
        players = [Player("Player"+str(x)) for x in range(self.numberOfPlayers)]
        for i in range(0, self.numberOfLines):
            line = Line(self.numberOfPlayers)

    def generate_random(self):
        players = [Player("Player"+str(x)) for x in range(self.numberOfPlayers)]
        positions = [x for x in range(MAX_ON_FIELD)]
        for i in range(0, self.numberOfLines):
            line = Line(self.numberOfPlayers)
            random.shuffle(players)
            for player in players:
                line.addPlayer(player)
            self.lines.append(line)

roster = Roster(10)
roster.generate_random()
print("Roster:")
print(str(roster))
