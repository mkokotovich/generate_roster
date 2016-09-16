import random
import operator

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


    def __lt__(self, other):
        return len(self.positionsPlayed) < len(other.positionsPlayed)


    def addPosition(self, position):
        self.positionsPlayed.append(position)


    def countPosition(self, position):
        return self.positionsPlayed.count(position)

    
    def detailedStats(self):
        return "Player {0} played {1} positions: {2}".format(self.playerId, len(self.positionsPlayed), ", ".join(str(pos) for pos in self.positionsPlayed))



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


    def addListToPlaying(self, players):
        for player in players:
            self.addToPlaying(player)


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


    def addListToSitting(self, players):
        for player in players:
            self.addToSitting(player)


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
    players = []
    lines = []


    def __init__(self, numberOfPlayers, numberOfLines=8):
        self.numberOfPlayers=numberOfPlayers
        self.numberOfLines = numberOfLines
        self.players = [Player(""+str(x)) for x in range(self.numberOfPlayers)]
        self.lines = []


    def __str__(self):
        msg = ""
        for i in range(0, self.numberOfLines):
            msg += "Line {0}:\n".format(i+1)
            msg += str(self.lines[i])
        return msg


    def findNextGoalie(self, players):
        goalie = -1,100000
        for player in players:
            if player.countPosition(0) < goalie[1]:
                goalie = player, player.countPosition(0)
        return goalie[0]


    def findNextDefense(self, players):
        defense = -1,100000
        for player in players:
            defense_count = player.countPosition(1) + player.countPosition(2)
            if defense_count < defense[1]:
                defense = player, defense_count
        return defense[0]


    def findNextForward(self, players):
        forward = -1,100000
        for player in players:
            forward_count = player.countPosition(3) + player.countPosition(4) + player.countPosition(5)
            if forward_count < forward[1]:
                forward = player, forward_count
        return forward[0]


    def generateOptimized(self):
        for i in range(0, self.numberOfLines):
            line = Line(self.numberOfPlayers)
            playing = []
            sitting = []
            if i == 0:
                # First round is just the first 6
                playing = self.players[0:MAX_ON_FIELD]
                sitting = self.players[MAX_ON_FIELD:]
            else:
                # Initialize the playing list to those who were sitting last time
                playing = list(self.lines[i-1].sitting)
                sitting = [x for x in self.players if x not in playing]
                sitting.sort()
                while len(playing) < MAX_ON_FIELD:
                    # Add the next least-played players from the sitting list
                    playing.append(sitting[0])
                    sitting = sitting[1:]
            # Goalie
            player = self.findNextGoalie(playing)
            line.addToPosition(player, 0)
            playing.remove(player)
            # Defense
            player = self.findNextDefense(playing)
            line.addToPosition(player, 1)
            playing.remove(player)
            player = self.findNextDefense(playing)
            line.addToPosition(player, 2)
            playing.remove(player)
            # Forward
            player = self.findNextForward(playing)
            line.addToPosition(player, 3)
            playing.remove(player)
            player = self.findNextForward(playing)
            line.addToPosition(player, 4)
            playing.remove(player)
            player = self.findNextForward(playing)
            line.addToPosition(player, 5)
            playing.remove(player)
            # Sitting
            line.addListToSitting(sitting)
            self.lines.append(line)


    def generateRandom(self):
        positions = [x for x in range(MAX_ON_FIELD)]
        for i in range(0, self.numberOfLines):
            line = Line(self.numberOfPlayers)
            random.shuffle(self.players)
            for player in self.players:
                line.addPlayer(player)
            self.lines.append(line)


    def printDetailedStats(self):
        for player in self.players:
            print(player.detailedStats())



for i in range(6, 11):
    roster = Roster(i)
    roster.generateOptimized()
    print("Roster:")
    print(str(roster))
    roster.printDetailedStats()
