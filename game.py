# Python Text RPG
# by Dave Rave

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100


# Player Set up ########
class player:
    def __init__(self):
        self.name = ""
        self.job = ""
        self.hp = 0
        self.damage = 0
        self.armor = 0
        self.mana = 0
        self.gold = 0
        self.status_effects = []
        self.location = "c3"
        self.game_over = False


myPlayer = player()


# Title Screen ######
def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        print("Play")
        setup_game()
    elif option.lower() == "help":
        print("Help")
        help_menu()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ["play", "help", "quit"]:
        print("Please choose between: play, help or quit: ")
        option = input("> ")
        if option.lower() == "play":
            print("Play")
            setup_game()
        elif option.lower() == "help":
            print("Help")
            help_menu()
        elif option.lower() == "quit":
            sys.exit()


def title_screen():
    os.system('cls')
    print("##############################")
    print("## Welcome to H # E # L # L ##")
    print("##############################")
    print("##        - Play -          ##")
    print("##        - Help -          ##")
    print("##        - Quit -          ##")
    print("##############################")
    print("##############################")
    print("##   Created by DaaVee      ##")
    print("##############################")
    title_screen_selections()


def help_menu():
    print("##############################")
    print("## Welcome to H # E # L # L ##")
    print("##############################")
    print("~ Use 'up' 'left' ...  to move")
    print(" ~ Type commands to stay LIT  ")
    print("##  ~ Use 'look' to inspect ##")
    print("##  ~ Go out there and DIE  ##")
    print("##############################")
    title_screen_selections()


# MAP #########
zone_name = ""
description = "description"
examination = "examine"
solved = False
up = "up", "north"
down = "down", "south"
left = "left", "west"
right = "right", "east"

solved_places = {"a1": False, "a2": False, "a3": False, "a4": False,
                 "b1": False, "b2": False, "b3": False, "b4": False,
                 "c1": False, "c2": False, "c3": False, "c4": False,
                 "d1": False, "d2": False, "d3": False, "d4": False, }

zone_map = {
    "a1": {
        zone_name: "The High Mountain",
        description: "An old legend says that up there lives The King of HELL",
        examination: "What's up there?",
        solved: False,
        up: "",
        down: "b1",
        left: "",
        right: "a2",
    },
    "a2": {
        zone_name: "Forest",
        description: "I think I saw a squirrel",
        examination: "Look around for something unusual...",
        solved: False,
        up: "",
        down: "b2",
        left: "a1",
        right: "a3",
    },
    "a3": {
        zone_name: "Sea",
        description: "You can't put description on something that hides so many mysteries...",
        examination: "Hmm... What if there is something else out there?",
        solved: False,
        up: "",
        down: "b3",
        left: "a2",
        right: "a4",
    },
    "a4": {
        zone_name: "Island",
        description: "Shit dude, maybe you found the goal of the game? The final thing to be done!",
        examination: "There are footsteps on the beach that lead deep into a wild forest.",
        solved: False,
        up: "",
        down: "b4",
        left: "a3",
        right: "",
    },
    "b1": {
        zone_name: "Swamp",
        description: "This looks like something haunted... maybe you should gtfo asap",
        examination: "You hear something weird like a crazy person laughing at the distance.",
        solved: False,
        up: "a1",
        down: "c1",
        left: "",
        right: "b2",
    },
    "b2": {
        zone_name: "Lake",
        description: "Beautiful, ain't it ?",
        examination: "There are some ducks quacking and swimming in it :3",
        solved: False,
        up: "a2",
        down: "c2",
        left: "b1",
        right: "b3",
    },
    "b3": {
        zone_name: "Plains",
        description: "A large area of flat land with few trees.",
        examination: "There are some mushrooms and mice",
        solved: False,
        up: "a3",
        down: "c3",
        left: "b2",
        right: "b4",
    },
    "b4": {
        zone_name: "Sea",
        description: "Why we are here? Just to suffer?",
        examination: "This beach is quite clean... something you can't see nowadays....",
        solved: False,
        up: "a4",
        down: "c4",
        left: "b3",
        right: "",
    },
    "c1": {
        zone_name: "Farm",
        description: "A huge farm dude, you are really lucky finding this!",
        examination: "You see a lot of food, the problem is... it's still moving...",
        solved: False,
        up: "b1",
        down: "d1",
        left: "",
        right: "c2",
    },
    "c2": {
        zone_name: "Forest",
        description: "This is quite chilly.",
        examination: "You hear the birds singing, the wind yoinking the tree leafs and some cows moo-ing, "
                     "wait... cows moo-ing?",
        solved: False,
        up: "b2",
        down: "d2",
        left: "c1",
        right: "c3",
    },
    "c3": {
        zone_name: "Home",
        description: "This is where you drink, smoke and eat. "
                     "Also it's not your mom's basement, which is a plus.",
        examination: "Your home looks the same - nothing has changed. "
                     "You start feeling lonely again, "
                     "and the best way to fight anxiety is to go out, "
                     "so get your fat ass up and GET THE FUCK OUT!",
        solved: False,
        up: "b3",
        down: "d3",
        left: "c2",
        right: "c4",
    },
    "c4": {
        zone_name: "The Docks",
        description: "There are lots of useful shit here.",
        examination: "Here works a lonely soul, who had lost everyone close to him...",
        solved: False,
        up: "b4",
        down: "d4",
        left: "c3",
        right: "",
    },
    "d1": {
        zone_name: "Camp",
        description: "A camp? Oh, you aren't alone after all... Wait..... A CAMP???",
        examination: "Uhm... they seem quite armed... make a good approach "
                     "or leave immediately",
        solved: False,
        up: "c1",
        down: "",
        left: "",
        right: "d2",
    },
    "d2": {
        zone_name: "Shop",
        description: "Here you can buy goods to ease you journey!",
        examination: "You see things you can exchange money for.",
        solved: False,
        up: "c2",
        down: "",
        left: "d1",
        right: "d3",
    },
    "d3": {
        zone_name: "Plains",
        description: "There is a silly smell here...",
        examination: "You see a lying man in the distance.",
        solved: False,
        up: "c3",
        down: "",
        left: "d2",
        right: "d4",
    },
    "d4": {
        zone_name: "Tavern",
        description: "Your local 'Get Shitfaced' place",
        examination: "There are a lot of drink men in this place.",
        solved: False,
        up: "c4",
        down: "",
        left: "d3",
        right: "",
    },
}


# Game Interactivity ########
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + myPlayer.location.upper() + ' #')
    print('# ' + zone_map[myPlayer.location][description] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))


def prompt():
    print("\n" + "==================================")
    print("What would you like to do?")
    action = input("> ")
    acceptable_actions = ["move", "go", "travel", "walk", "QUIT", "examine", "inspect", "interact", "look"]
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input("> ")
    if action.lower() == "QUIT":
        sys.exit()
    elif action.lower() in ["move", "go", "travel", "walk"]:
        player_move(action.lower())
    elif action.lower() in ["examine", "inspect", "interact", "look"]:
        player_examine(action.lower())


def player_move(action):
    ask = "Where would you like to go next?\n"
    destination = input(ask)
    if destination in ["up", "north"]:
        destination = zone_map[myPlayer.location[up]]
        movement_handler(destination)
    elif destination in ["down", "south"]:
        destination = zone_map[myPlayer.location[down]]
        movement_handler(destination)
    elif destination in ["left", "west"]:
        destination = zone_map[myPlayer.location[left]]
        movement_handler(destination)
    elif destination in ["right", "east"]:
        destination = zone_map[myPlayer.location[right]]
        movement_handler(destination)


def movement_handler(destination):
    print("\n" + "You have moved to the " + destination + ".")
    myPlayer.location = destination
    print_location()


def player_examine(action):
    if zone_map[myPlayer.location][solved]:
        print("You have already fuck the shit out of this zone.")
    else:
        print("There are still so many things you could do here...")


# Game Functionality ########


def main_game_loop():
    while myPlayer.game_over is False:
        prompt()
    # here handle if puzzles have been solved, boss defeated etc. etc.


def setup_game():
    os.system('cls')

    # NAME COLLECTING ####
    question1 = "Hello, what is your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    myPlayer.name = player_name

    # JOB HANDLING
    question2 = "Which class would you like to be?\n"
    question2added = "You can play as a warrior, mage or archer :)\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    player_job = input("> ")
    valid_jobs = ["warrior", "mage", "archer"]
    if player_job.lower() in valid_jobs:
        myPlayer.job = player_job
        print("Well that;s weird, good luck with " + player_job + "ing...\n")
    while player_job.lower() not in valid_jobs:
        player_job = input("> Please, enter a valid class...\n ")
        if player_job.lower() in valid_jobs:
            myPlayer.job = player_job
            print("Pffft... good luck with that, " + player_job + " scum!\n")

    # PLAYER STATS
    if myPlayer.job is "warrior":
        myPlayer.hp = 12
        myPlayer.damage = 2
        myPlayer.armor = 4
        myPlayer.mana = 5
    elif myPlayer.job is "mage":
        myPlayer.hp = 6
        myPlayer.damage = 4
        myPlayer.armor = 2
        myPlayer.mana = 10
    elif myPlayer.job is "archer":
        myPlayer.hp = 8
        myPlayer.damage = 3
        myPlayer.armor = 3
        myPlayer.mana = 5

    # INTRODUCTION ########
    question3 = "Welcome, " + player_name + " the " + player_job + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    speech1 = "Welcome to... H E L L ! ! !\n"
    speech2 = "Mysterious powers rule over this place!\n"
    speech3 = "Would you be able to handle the pressure. . . MUAHAHAHAAA....\n"
    speech4 = "Oh, yeah, and good luck getting out. . . ALIVE. . .\n"

    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    os.system('cls')
    print("#####################")
    print("##  LET'S GO BABY  ##")
    print("#####################")
    main_game_loop()


title_screen()


