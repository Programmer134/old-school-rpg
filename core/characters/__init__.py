from math import ceil


class Character(object):
    def __init__(self, name, type, race):
        self.name = name
        self.type = type
        self.race = race
        self.weapon = {'name': '', 'type': '', 'bonus': 0}
        self.shield = {'name': '', 'type': '', 'bonus': 0}
        self.armor = {'name': '', 'type': '', 'bonus': 0}
        self.inventory = []
        self.attack = 0
        self.defense = 0
        self.full_hp = 0
        self.hp = 0
        self.speed = 0
        self.status = 'unknown'

    def change_status(self, new_status = None):
        if not new_status:
            if self.hp <= 0:
                self.status = 'dead'
            elif self.hp == self.full_hp:
                self.status = 'well'
            elif self.hp <= ceil(self.full_hp / 3):
                self.status = 'severily wounded'
            elif self.hp <= ceil(self.full_hp * 2 / 3):
                self.status = 'wounded'
            else:
                self.status = 'lightly wounded'
        else:
            self.status = new_status


    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.type == 'Player':
            print(f'You take {damage} damage.')
        else:
            print(f'{self.name} takes {damage} damage.')
        self.declare_hp()
        self.change_status()

    def declare_status(self):
        if self.type == 'Player':
            print(f'You are {self.status}')
        else:
            print(f'{self.name} looks {self.status}.')

    def declare_hp(self):
        if self.type == 'Player':
            print(f'Your current HP: {self.hp}')
        else:
            print(f'{self.name}\'s current HP: {self.hp}.')

    def declare_inventory(self):
        print(f'Your inventory:')
        # return self.inventory
        for item in self.inventory:
            if type(item) == dict:
                print(f'\t- {item["name"]}')
            else:
                print(f'\t- {item}')

    def draw_weapon(self):
        if not self.weapon["name"]:
            if self.type == 'Player':
                print(f'You have no weapon.')
            else:
                exit(
                    f'{self.name} doesn\'t have a weapon. This is probably a mistake on your code.')
        else:
            if self.weapon["type"] == 'blade':
                action = ['unsheathe',  'unsheathes']
            elif self.weapon["type"] == 'range':
                action = ['place an arrow on',
                          'places an arrow on']
            elif self.weapon["type"] == 'blunt':
                action = ['draw', 'draws']

            if self.type == 'Player':
                print(f'You {action[0]} your {self.weapon["name"]}.')
            else:
                print(f'{self.name} {action[1]} a {self.weapon["name"]}.')


class Player(Character):
    def __init__(self, name='Hero', race='human'):
        super(Player, self).__init__(name, 'Player', race)
        self.status = 'well'

    def get_item(self, item):
        if type(item) == dict:
            print(f'You get {item["name"]}.')
        else:
            print(f'You get {item}.')
        self.inventory.append(item)

    def drop_item(self, item=None):
        if item == None:
            print('Which item would you like to drop?')
            self.declare_inventory()
            which_item = input('> ')
            for this_item in self.inventory:
                if type(this_item) == dict:
                    if str(this_item["name"]).lower() == which_item.lower():
                        item = this_item
                elif this_item.lower() == which_item.lower():
                    item = this_item

        if item != None:
            if type(item) == dict:
                print(f'You dropped {item["name"]}.')
            else:
                print(f'You dropped {item}.')
            self.inventory.remove(item)
        else:
            print(f'You don\'t have {which_item} on your inventory.')


class NPC(Character):
    def __init__(self, name='Ugly Monster', race='humanoid'):
        super(NPC, self).__init__(name, 'NPC', race)

    def set_name(self, new_name):
        self.name = new_name
        print(f'The {self.race} tells you his name is {self.name}.')

    def declare_action(self, action):
        print(f'{self.name} is {action}.')