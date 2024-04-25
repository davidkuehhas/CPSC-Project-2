#Author:         David Kuehhas
#Date:           04/02/2024
#Assignment:     Project 1
#Course:         CPSC1050
#Section         001
#GitHubLink      https://github.com/davidkuehhas/CPSC-Project-2

#Code Description: This code runs the player through Dave's Escape Room. It starts with a welcome and warning message.
#It spawns the player in the living room, and gives them options what to do. This code uses several classes and loops
#in order to function as a working escape room. It also offers the option to save a game and load a saved one in and continue playing.

class Base:
    def __init__(self):
        self.log = []

    def add_to_log(self, message):
        self.log.append(message)

class Item(Base):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

class Room(Base):
    def __init__(self, name, description, items=None):
        super().__init__()
        self.name = name
        self.description = description
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)

class Player(Base):
    def __init__(self, name, health=100, inventory=None):
        super().__init__()
        self.name = name
        self.health = health
        self.inventory = inventory if inventory else []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def display_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print("-", item.name)

    def save_player(self, file):
        file.write(f"{self.name}|{self.health}|")
        for item in self.inventory:
            file.write(f"{item.name},{item.description}|")
        file.write("\n")

    def load_player(self, file):
        player_data = file.readline().strip().split("|")
        self.name = player_data[0]
        self.health = int(player_data[1])
        items_data = player_data[2].split("|")
        for item_data in items_data:
            item_info = item_data.split(",")
            self.inventory.append(Item(item_info[0], item_info[1]))

class Game(Base):
    def __init__(self, player, rooms):
        super().__init__()
        self.player = player
        self.rooms = rooms
        self.current_room = None
        self.ending_room = rooms[-1]  #Last room as the ending room

    def start_game(self):
        self.add_to_log("The Escape has Started...")
        print("Welcome to Dave's Escape Room! Hopefully you can find a way out, because you don't want to know what happens if you can't...And also, you're in my house, in my living room right now so, you know, be courteous.")
        self.current_room = self.rooms[0]
        self.play()

    def play(self):
        while True:
            print("\n" + "-" * 40)
            print("You are now in the", self.current_room.name)
            print(self.current_room.description)
            print("There are these items in the room:", [item.name for item in self.current_room.items])

            action = input("What would you like to do? (type 'help' for options): ").lower().strip()

            if action == 'help':
                self.add_to_log("You need help? Already? At this rate, you'll be here forever...")
                self.display_help()

            elif action == 'move':
                self.add_to_log("Player attempted to move.")
                self.move()

            elif action == 'search':
                self.add_to_log("Player searched the room.")
                self.search_room()

            elif action == 'take':
                self.add_to_log("Player attempted to take an item.")
                self.take_item()

            elif action == 'use':
                self.add_to_log("Player attempted to use an item.")
                self.use_item()

            elif action == 'inventory':
                self.add_to_log("Player checked inventory.")
                self.player.display_inventory()

            elif action == 'save':
                self.add_to_log("Player attempted to save the game.")
                self.save_game()

            elif action == 'load':
                self.add_to_log("Player attempted to load the game.")
                self.load_game()

            elif action == 'quit':
                self.add_to_log("Player quit the game.")
                print("You're a quitter...That's not an escape.")
                break

            else:
                self.add_to_log("Player entered an invalid action.")
                print("Invalid action. Type 'help' for options.")

            if self.current_room == self.ending_room:
                if self.check_escape():
                    self.add_to_log("Player escaped successfully.")
                    self.display_ending()
                    play_again = input("Would you like to play again? (yes/no): ").lower().strip()
                    if play_again == 'yes':
                        self.start_game()
                    else:
                        print("You won't be gone for long...")
                        break

    def display_help(self):
        print("Available actions: move, search, take, use, inventory, save, load, quit")

    def move(self):
        direction = input("Which direction do you want to move? (up/back/right/left): ").lower().strip()
        next_room = None
        if direction in ['up', 'back', 'right', 'left']:
            print("You move", direction)
            next_room_index = (self.rooms.index(self.current_room) + 1) % len(self.rooms)
            next_room = self.rooms[next_room_index]
            self.current_room = next_room
        else:
            print("Invalid direction.")

    def search_room(self):
        print("You decide to search around the room...")
        if self.current_room.items:
            print("You found these items:")
            for item in self.current_room.items:
                print("-", item.name + ": " + item.description)
        else:
            print("You found nothing in this room. Maybe move and try the next room?")

    def take_item(self):
        item_name = input("Which item do you think could help you out in the future and you want to take? ").strip()
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.player.add_to_inventory(item)
                self.current_room.items.remove(item)
                print(f"You've taken the {item.name}.")
                return
        print(f"No '{item_name}' found in this room.")

    def use_item(self):
        if not self.player.inventory:
            print("Your inventory is empty. Go take something. Can't escape with an empty inventory.")
            return
        item_name = input("Which item do you want to use? ").strip()
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                if self.current_room == self.ending_room and item.name.lower() == 'key':
                    return True
                else:
                    print(f"You use the {item.name}.")
                    return False
        print(f"No '{item_name}' found in your inventory.")

    def check_escape(self):
        for item in self.player.inventory:
            if item.name.lower() == 'key':
                print("You insert the key into the door lock...")
                return True
        print("You need a key to escape...there's a keyhole. Where did you see a key? Seriously though, you're in an escape room and you saw a key and didn't take it? Must be a first timer.")
        return False

    def display_ending(self):
        print("\n" + "-" * 40)
        print("You have finally escaped from Dave's Escape Room...took you long enough. See you soon though!")

    def save_game(self):
        filename = input("Enter the filename to save the game: ")
        try:
            with open(filename, 'w') as file:
                self.player.save_player(file)
                self.add_to_log("Game saved successfully.")
                print("Game saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

    def load_game(self):
        filename = input("Enter the filename to load the game: ")
        try:
            with open(filename, 'r') as file:
                self.player.load_player(file)
                self.add_to_log("Game loaded successfully.")
                print("Game loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")


item1 = Item("Key", "A rusty big key that looks ancient.")
item2 = Item("Flashlight", "A flashlight that barely works, but gets the job done.")
item3 = Item("Book", "An dusty, old book...'The Old Man and the Sea'")
item4 = Item("Crowbar", "A shiny, sturdy crowbar.")
room1 = Room("Living Room", "A dark, spacious living room with a dirty old couch and a weirdly high number of mirrors.", [item1, item2])
room2 = Room("Bedroom", "A small bedroom with an old, creaky, perfectly made bed. ", [item3, item4])
ending_room = Room("Exit", "You have found the last room, the exit. There is a door with a keyhole.")
player = Player("Player")

# Initialize the game
game = Game(player, [room1, room2, ending_room])

# Start the game
game.start_game()



