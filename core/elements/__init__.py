import gameplay
from core.config import *
from typing import List

# DEFINES BASIC LOGICS FOR ELEMENTS AND ITEMS

# Element
'''
    CLASS used for all interactable elements on the game.
'''


class Element(object):

    def __init__(self, name, description):
        self.name: str = name
        self.description: str = description
        self.scenario: str = ''
        self.looking_effect: str = None
        self.searching_effect: List[str] = None
        self.on_hearing = None
        self.hearing_effect: str = None
        self.on_touching = None
        self.touching_effect: str = None
        self.on_tasting = None
        self.tasting_effect: str = None

    # on_looking

    '''
        If the place looked upon has visible elements (ej. apples on trees),
        the items are added to the Scenario instance and can now be also interacted to with.
        Hidden elements are only found with on_serching.
    '''

    @property
    def article(self) -> str:
        if self.name.endswith('s'):
            return
        elif self.name.startswith(('a', 'e', 'i', 'o', 'u', 'y')):
            return 'an'
        else:
            return 'a'

    def on_looking(self) -> None:
        for attr, value in self.__dict__.items():

            if issubclass(type(value), Item) or type(value) == Item:
                if value.hidden == False:
                    if not hasattr(gameplay.CURRENT_SCENARIO, attr):
                        print_cinematics(
                            f'You see {value.name} on the {self.name}')
                        gameplay.CURRENT_SCENARIO.add_to_scenario(
                            attr, value)

    # on_searching

    '''
    If the place looked upon has hidden items,
    they are added to the Scenario instance and can now be also interacted to with.
    Visible items are not found here with on_serching, but seen with on_looking.
    '''

    def on_searching(self) -> None:
        if self.searching_effect:
            print_cinematics(self.searching_effect[0])
            self.searching_effect[1]()

        for attr, value in self.__dict__.items():

            if issubclass(type(value), Item) and value.hidden == True:
                value.hidden = False
                print_cinematics(f'You find {value.name}')
                system_name = value.name.replace(' ', '_').lower()
                gameplay.CURRENT_SCENARIO.add_to_scenario(
                    system_name, value)
                # delattr(self, system_name)
                return
        print_cinematics(f'You search the {self.name} but you find nothing.')

# called when Hero takes an item with on_taking attribute
    def on_taking(self, callback=None):
        if callback:
            callback()

# Item


'''
    CLASS used exclusively for items that can be taken and/or used by the Hero.
'''


class Item(Element):

    def __init__(self, name: str, description: str, weight: int):
        super(Item, self).__init__(name, description)
        self.hidden: bool = False
        self.usable: bool = False
        self.weight: int = weight

# Container


'''
    CLASS used exclusively for elements that contain another elements (ej. a chest).
'''


class Container(Element):

    def __init__(self, name: str, description: str):
        super(Container, self).__init__(name, description)

    def add_item(self, item: Item):
        setattr(self, item.name, item)


class Food(Item):

    def __init__(self, name: str, description: str, weight: int, quantity: int):
        self.description: str = description
        super(Food, self).__init__(name, self.description, weight)
        self.usable: bool = True
        self.quantity: int = quantity
        self.unity_weight: int = weight
        self.weight: int = weight * quantity

    def add(self, quantity: int):
        self.quantity = self.quantity + quantity
        self.update_quantity()

    def remove(self, quantity: int):
        self.quantity = self.quantity - quantity
        self.update_quantity()

    def update_quantity(self):
        self.weight = self.unity_weight * self.quantity

# Weapon


'''
    CLASS used exclusively for Weapons.
'''


class Weapon(Item):

    def __init__(self, name: str, description: str, weight: int, weapon_type: str, bonus: int):
        super(Weapon, self).__init__(name, description, weight)
        self.type: str = weapon_type
        self.bonus: str = bonus

# Shield


'''
    CLASS used exclusively for Shields.
'''


class Shield(Item):

    def __init__(self, name: str, description: str, weight: int, bonus: int):
        super(Shield, self).__init__(name, description, weight)
        self.bonus: int = bonus

# Armor


'''
    CLASS used exclusively for Armors.
'''


class Armor(Item):

    def __init__(self, name: str, description: str, weight: int, bonus: int):
        super(Armor, self).__init__(name, description, weight)
        self.bonus: int = bonus


'''
  class Element(object):
  def __init__(self, name, description):
    self.name = name
    self.description = description

    on_looking =
    'looking_effect': 'tired'

    'on_searching': 'You spend a very long time searching the bushes and start to feel tired.',
    'searching_effect': 'tired'

'''
