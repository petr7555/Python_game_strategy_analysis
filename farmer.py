import random


class Game:
    def __init__(self, available={"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}):
        self.animals_available = available.copy()
        self.default = available.copy()
        self.exchange_rules = {"rabbit": 1, "sheep": 6, "pig": 12, "cow": 36, "horse": 72, "fox": 0, "wolf": 0}
        self.edible = ["rabbit", "sheep", "pig", "cow"]

    def reset(self):
        self.animals_available = self.default.copy()


class Person(Game):

    def __init__(self, game):
        self.game = game
        self.farm = {"rabbit": 0, "sheep": 0, "pig": 0, "cow": 0, "horse": 0}

    def set_farm(self, kind, count):
        self.farm[kind] = count

    def add_farm(self, kind, count):
        if self.is_available(kind, count):
            self.farm[kind] += count
            self.game.animals_available[kind] -= count
        else:
            available = self.get_available(kind)
            self.farm[kind] += available
            self.game.animals_available[kind] -= available

    def reduce_farm(self, kind, count):
        self.farm[kind] -= count
        self.game.animals_available[kind] += count

    def eat_by_fox(self):
        self.game.animals_available["rabbit"] += self.farm["rabbit"]
        self.set_farm("rabbit", 0)

    def eat_by_wolf(self):
        for animal in self.game.edible:
            self.game.animals_available[animal] += self.farm[animal]
            self.set_farm(animal, 0)

    def is_available(self, animal, count):
        if self.game.animals_available[animal] >= count:
            return True
        return False

    def get_available(self, animal):
        return self.game.animals_available[animal]

    # how many {former count} of {former kind}
    # you want to exchange for {latter kind}
    def exchange(self, former_kind, former_count, latter_kind):
        # former is less valuable than latter
        exchange_rules = self.game.exchange_rules
        if exchange_rules[latter_kind] > exchange_rules[former_kind]:
            small = former_kind
            big = latter_kind
            add_value = (former_count * exchange_rules[small]) // exchange_rules[big]
            if not self.is_available(latter_kind, add_value):
                available = self.get_available(latter_kind)
                add_value = available
            reduce_value = (add_value * exchange_rules[big]) // exchange_rules[small]
        # former is more valuable than latter
        else:
            small = latter_kind
            big = former_kind
            add_value = (former_count * exchange_rules[big]) // exchange_rules[small]
            if self.is_available(latter_kind, add_value):
                reduce_value = former_count
            # when there are fewer animals available than needed, exchange all available animals remaining
            else:
                available = self.get_available(latter_kind)
                reduce_value = (available * exchange_rules[small]) // exchange_rules[big]
                add_value = (reduce_value * exchange_rules[big]) // exchange_rules[small]

        self.add_farm(latter_kind, add_value)
        self.reduce_farm(former_kind, reduce_value)

    @staticmethod
    def roll_dice_red(red_dice):
        return red_dice.roll()

    @staticmethod
    def roll_dice_yellow(yellow_dice):
        return yellow_dice.roll()

    @staticmethod
    def roll_both_dice(red_dice, yellow_dice):
        return Person.roll_dice_red(red_dice), Person.roll_dice_yellow(yellow_dice)

    def make_turn(self, red_dice, yellow_dice):
        self.exchange_strategy()
        red, yellow = Person.roll_both_dice(red_dice, yellow_dice)
        if yellow == "wolf":
            self.eat_by_wolf()
        elif red == "fox":
            self.add_farm(yellow, (self.farm[yellow] + 1) // 2)
            self.eat_by_fox()
        else:
            if red == yellow:
                self.add_farm(red, (self.farm[red] + 2) // 2)
            else:
                self.add_farm(red, (self.farm[red] + 1) // 2)
                self.add_farm(yellow, (self.farm[yellow] + 1) // 2)

        return self.check_win()

    def calculate_value(self):
        value = 0
        for animal in self.farm:
            value += self.farm[animal] * self.game.exchange_rules[animal]
        return value

    def check_win(self):
        if self.calculate_value() >= 127:
            return True
        return False

    def reset(self):
        # self.farm = self.default.copy()
        self.farm = {"rabbit": 0, "sheep": 0, "pig": 0, "cow": 0, "horse": 0}


# doesn't make any exchanges
class StrategyDoNothing(Person):

    def exchange_strategy(self):
        pass


# exchanges everything for the biggest value animal
class StrategyBiggestAnimal(Person):

    def exchange_strategy(self):
        animals = ["rabbit", "sheep", "pig", "cow", "horse"]
        farm = self.farm
        for i in range(len(animals) - 1):
            self.exchange(animals[i], farm[animals[i]], animals[i + 1])


# exchanges everything for his favourite animal
class StrategyFavouriteAnimal(Person):

    def __init__(self, favourite, game):
        Person.__init__(self, game)
        self.favourite = favourite

    def exchange_strategy(self):
        animals = ["rabbit", "sheep", "pig", "cow", "horse"]
        farm = self.farm
        for i in range(len(animals) - 1):
            if animals[i] != self.favourite:
                self.exchange(animals[i], farm[animals[i]], self.favourite)


class StrategyAdvantage(Person):

    def __init__(self, favourite, game):
        Person.__init__(self, game)
        self.favourite = favourite
        self.default = {"rabbit": 0, "sheep": 0, "pig": 0, "cow": 0, "horse": 0}

    def reset(self):
        self.farm = self.default.copy()

    def exchange_strategy(self):
        animals = ["rabbit", "sheep", "pig", "cow", "horse"]
        farm = self.farm
        for i in range(len(animals) - 1):
            if animals[i] != self.favourite:
                self.exchange(animals[i], farm[animals[i]], self.favourite)


class Dice:

    def __init__(self, animals):
        self.animals = []
        num_of_sides = sum(animals.values())
        assert num_of_sides == 12, "A dice should have 12 sides."

        # parse dict to list
        for animal in animals:
            for i in range(animals[animal]):
                self.animals.append(animal)

    def roll(self):
        return random.choice(self.animals)
