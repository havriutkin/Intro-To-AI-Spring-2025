import random

# The cave is a dodecahedron: 20 rooms, each connected to 3 others.
CAVE = {
    1:  [2, 5, 8],
    2:  [1, 3, 10],
    3:  [2, 4, 12],
    4:  [3, 5, 14],
    5:  [1, 4, 6],
    6:  [5, 7, 15],
    7:  [6, 8, 17],
    8:  [1, 7, 9],
    9:  [8, 10, 18],
    10: [2, 9, 11],
    11: [10, 12, 19],
    12: [3, 11, 13],
    13: [12, 14, 20],
    14: [4, 13, 15],
    15: [6, 14, 16],
    16: [15, 17, 20],
    17: [7, 16, 18],
    18: [9, 17, 19],
    19: [11, 18, 20],
    20: [13, 16, 19]
}

class WumpusGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        rooms = list(CAVE.keys())
        self.wumpus = random.choice(rooms)
        hazard_rooms = {self.wumpus}

        # Place pits
        self.pits = set(random.sample([r for r in rooms if r not in hazard_rooms], 2))
        hazard_rooms.update(self.pits)

        # Place bats
        self.bats = set(random.sample([r for r in rooms if r not in hazard_rooms], 2))
        hazard_rooms.update(self.bats)

        # Place player
        available_rooms = [r for r in rooms if r not in hazard_rooms]
        self.player = random.choice(available_rooms)

        self.arrows = 5
        self.game_over = False
        self.victory = False

    def adjacent_hazards(self):
        warnings = []
        for neighbor in CAVE[self.player]:
            if neighbor == self.wumpus:
                warnings.append("You smell a terrible stench.")
            if neighbor in self.pits:
                warnings.append("You feel a breeze.")
            if neighbor in self.bats:
                warnings.append("You hear rustling of bat wings.")
        return warnings

    def move_player(self, room):
        if room not in CAVE[self.player]:
            print("You can't move there; it's not adjacent.")
            return
        self.player = room

        if self.player == self.wumpus:
            print("You entered the Wumpus's room! It ate you. Game over.")
            self.game_over = True
        elif self.player in self.pits:
            print("You fell into a bottomless pit! Game over.")
            self.game_over = True
        elif self.player in self.bats:
            print("A bat snatches you! It drops you in a random room.")
            self.player = random.choice(list(CAVE.keys()))
            # Check for hazards again after being dropped
            if self.player == self.wumpus:
                print("You were dropped into the Wumpus's room! It ate you. Game over.")
                self.game_over = True
            elif self.player in self.pits:
                print("You were dropped into a pit! Game over.")
                self.game_over = True

    def shoot_arrow(self, path):
        if self.arrows <= 0:
            print("You have no arrows left!")
            return
        self.arrows -= 1
        room = self.player
        for next_room in path:
            if next_room not in CAVE[room]:
                # Ricochet: arrow bounces to a random adjacent room
                next_room = random.choice(CAVE[room])
            room = next_room
            if room == self.wumpus:
                print("Your arrow strikes true! You killed the Wumpus. You win!")
                self.victory = True
                self.game_over = True
                return
            if room == self.player:
                print("Your arrow came back and killed you! Game over.")
                self.game_over = True
                return
        print("Your arrow missed.")
        # Wumpus might move after a missed shot
        if random.random() < 0.75:
            self.move_wumpus()

    def move_wumpus(self):
        self.wumpus = random.choice(CAVE[self.wumpus])
        if self.wumpus == self.player:
            print("You hear a rumble... The Wumpus moved into your room and ate you! Game over.")
            self.game_over = True

    def play(self):
        print("Welcome to Kill the Wumpus!")
        while not self.game_over:
            print(f"\nYou are in room {self.player}.")
            print("Tunnels lead to rooms:", ", ".join(str(r) for r in CAVE[self.player]))
            for warning in self.adjacent_hazards():
                print(warning)
            action = input("Move or Shoot (M/S)? ").strip().upper()
            if action == 'M':
                try:
                    dest = int(input("Enter room number to move: "))
                except ValueError:
                    print("That's not a valid room number.")
                    continue
                self.move_player(dest)
            elif action == 'S':
                try:
                    path = list(map(int, input("Enter up to 3 rooms to shoot through, separated by spaces: ").split()))
                except ValueError:
                    print("Invalid input for shooting path.")
                    continue
                if len(path) > 3:
                    print("You can only shoot through up to 3 rooms.")
                    continue
                self.shoot_arrow(path)
            else:
                print("Invalid action. Choose M or S.")

        if self.victory:
            print("Congratulations, you have slain the Wumpus!")
        else:
            print("Better luck next time.")

if __name__ == '__main__':
    game = WumpusGame()
    game.play()
