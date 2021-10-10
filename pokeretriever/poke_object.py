from abc import ABC


class PokedexObject(ABC):
    """
        Pokemon object that exists in the pokedex
    """

    def __init__(self, name, id):
        self._name = name
        self._id = id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


class Pokemon(PokedexObject):
    """
        Pokemon object with its own stats.
    """

    def __init__(self, name, id, height, weight, stats, types, abilities, moves):
        super().__init__(name, id)
        self._height = height
        self._weight = weight
        self._stats = stats
        self._types = types
        self._abilities = abilities
        self._moves = moves

    @property
    def stats(self):
        return self._stats

    @property
    def abilities(self):
        return self._abilities

    @property
    def moves(self):
        return self._moves

    @property
    def types(self):
        return self._types

    @abilities.setter
    def abilities(self, value):
        self._abilities = value

    @moves.setter
    def moves(self, value):
        self._moves = value

    def expanded(self):
        """
            Returns the expanded, formatted, information of a pokemon, similar to __str__
        :return: String containing the expanded information
        """

        # ************TYPE*************
        types = ""
        count = 1
        for type in self._types:
            types = types + "    Type " + str(count) + ": " + type.title() + "\n"
            count = count + 1

        # ****************MOVE**************
        moves = ""
        count = 1
        for move in self._moves:
            moves = moves + "        Move " + str(count) + ": " + move.name.title() +\
                " (Learned at level: " + str(move.level) + ")\n" \
                "                Expanded Info:\n" \
                "                        URL: " + move.url + "\n" \
                "                        Name: " + move.name.title() + "\n" \
                "                        Id: " + str(move.id) + "\n" \
                "                        Generation: " + move.generation + "\n" \
                "                        Accuracy: " + str(move.accuracy) + "\n" \
                "                        PP: " + str(move.pp) + "\n" \
                "                        Power: " + str(move.power) + "\n" \
                "                        Type: " + move.type + "\n" \
                "                        Damage Class: " + move.damage_class + "\n" \
                "                        Effect (short): " + move.effect_short + "\n"
            count = count + 1

        # ********STATS*******

        # Speed
        stats = ""
        stats += "        " + self.stats.speed.name.title() + ": " + str(self.stats.speed.base_value) + \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.speed.url + "\n" \
            + "                        Name: " + self.stats.speed.name.title() + "\n" \
            + "                        Id: " + str(self.stats.speed.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.speed.is_battle_only) + "\n"

        # Special Defence
        stats += "        " + self.stats.sp_def.name.title() + ": " + str(self.stats.sp_def.base_value) + \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.sp_def.url + "\n" \
            + "                        Name: " + self.stats.sp_def.name.title() + "\n" \
            + "                        Id: " + str(self.stats.sp_def.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.sp_def.is_battle_only) + "\n"

        # Special Attack
        stats += "        " + self.stats.sp_atk.name.title() + ": " + str(self.stats.sp_atk.base_value) + \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.sp_atk.url + "\n" \
            + "                        Name: " + self.stats.sp_atk.name.title() + "\n" \
            + "                        Id: " + str(self.stats.sp_atk.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.sp_atk.is_battle_only) + "\n"

        # Defense
        stats += "        " + self.stats.defense.name.title() + ": " + str(self.stats.defense.base_value) +  \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.defense.url + "\n" \
            + "                        Name: " + self.stats.defense.name.title() + "\n" \
            + "                        Id: " + str(self.stats.defense.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.defense.is_battle_only) + "\n"

        # Attack
        stats += "        " + self.stats.attack.name.title() + ": " + str(self.stats.attack.base_value) + \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.attack.url + "\n" \
            + "                        Name: " + self.stats.attack.name.title() + "\n" \
            + "                        Id: " + str(self.stats.attack.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.attack.is_battle_only) + "\n"

        # HP
        stats += "        " + self.stats.hp.name.title() + ": " + str(self.stats.hp.base_value) + \
            "\n                Expanded Info:\n" \
            + "                        URL: " + self.stats.hp.url + "\n" \
            + "                        Name: " + self.stats.hp.name.title() + "\n" \
            + "                        Id: " + str(self.stats.hp.id) + "\n" \
            + "                        Is Battle Only: " + str(self.stats.hp.is_battle_only) + "\n"

        # ************ABILITY************
        abilities = ""
        count = 1
        effects = ""

        # Getting rid of original, weird formatting from api
        for ability in self._abilities:
            effects = ""
            for eff in ability.effect:
                if eff == "\n":
                    continue
                if eff == ".":
                    effects += eff + " "
                    continue
                effects += eff

        poke_count = 0
        pokemon_str = ""

        for ability in self._abilities:
            for pokemon in ability.pokemon:
                pokemon_str += "                                Pokemon " + str(poke_count) + ": " \
                    + pokemon.title() + "\n"
                poke_count += 1

            abilities = abilities + "        Ability " + str(count) + ": " + ability.name.title() + "\n" \
                "                Expanded Info:\n                        (URL: " + ability.url + ")\n" \
                "                        Name: " + ability.name.title() + "\n" \
                "                        Id: " + str(ability.id) + "\n" \
                "                        Generation: " + ability.generation + "\n" \
                "                        Effect: " + effects + "\n" \
                "                        Effect (short): " + ability.effect_short + "\n" \
                + pokemon_str

            # Resetting the pokemon string and count for the next pokemon in the list
            pokemon_str = ""
            poke_count = 0
            count = count + 1

        # Returns the string with expanded information on stats, abilities, and move
        return f"Name: {self.name.title()}\n" \
               f"Id: {self._id}\n" \
               f"Height: {self._height} decimeters\n" \
               f"Weight: {self._weight} hectograms\n" \
               f"Stats:\n{stats}" \
               f"Type(s):\n{types}" \
               f"Ability(s):\n{abilities}" \
               f"Moves(s):\n{moves}"

    def __str__(self):

        # Additional formatting to make it look nice
        types = ""
        count = 1
        for type in self._types:
            types = types + "    Type " + str(count) + ": " + type.title() + "\n"
            count = count + 1

        abilities = ""
        count = 1
        for ability in self._abilities:
            abilities = abilities + "    Ability " + str(count) + ": " + ability.name.title() + "\n"
            count = count + 1

        moves = ""
        count = 1
        for move in self._moves:
            moves = moves + "    Move " + str(count) + ": " + move.name.title()\
                    + " (Learned at level: " + str(move.level) + ")\n"
            count = count + 1

        return f"Name: {self.name.title()}\n" \
               f"Id: {self._id}\n" \
               f"Height: {self._height} decimeters\n" \
               f"Weight: {self._weight} hectograms\n" \
               f"Stats:{self.stats}" \
               f"Type(s):\n{types}" \
               f"Ability(s):\n{abilities}" \
               f"Moves(s):\n{moves}"


class PokemonAbility(PokedexObject):
    """
        Each Pokemon's individual abilities and their context.
    """

    def __init__(self, name, id, generation=None, effect=None, effect_short=None, pokemon=None):
        super().__init__(name, id)
        if pokemon is None:
            pokemon = []
        self._generation = generation
        self._effect = effect
        self._effect_short = effect_short
        self._pokemon = pokemon
        self._url = None

    @property
    def generation(self):
        return self._generation

    @property
    def effect(self):
        return self._effect

    @property
    def effect_short(self):
        return self._effect_short

    @property
    def pokemon(self):
        return self._pokemon

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def __str__(self):

        # Additional formatting to make it look nice
        pokes = ""
        count = 1

        for pokemons in self.pokemon:
            pokes += "    Pokemon " + str(count) + ": " + pokemons.title() + "\n"
            count = count + 1

        effects = ""
        for eff in self.effect:
            if eff == "\n":
                continue
            if eff == ".":
                effects += eff + " "
                continue
            effects += eff

        return f"Name: {self.name.title()}\n" \
               f"Id: {self._id}\n" \
               f"Generation: {self.generation}\n" \
               f"Effect: {effects}\n" \
               f"Effect (short): {self.effect_short}\n" \
               f"Pokemon:\n{pokes}"


class Stats:
    """
        Holds the individual pokemon's stats.
    """

    def __init__(self, speed=None, sp_def=None, sp_atk=None, defense=None, attack=None, hp=None):
        self._speed = speed
        self._sp_def = sp_def
        self._sp_atk = sp_atk
        self._defense = defense
        self._attack = attack
        self._hp = hp

    @property
    def speed(self):
        return self._speed

    @property
    def sp_def(self):
        return self._sp_def

    @property
    def sp_atk(self):
        return self._sp_atk

    @property
    def defense(self):
        return self._defense

    @property
    def attack(self):
        return self._attack

    @property
    def hp(self):
        return self._hp

    def __str__(self):
        return f"\n    Speed: {self._speed.base_value}\n" \
               f"    Special Defense: {self._sp_def.base_value}\n" \
               f"    Special Attack: {self._sp_atk.base_value}\n" \
               f"    Defense: {self._defense.base_value}\n" \
               f"    Attack: {self._attack.base_value}\n" \
               f"    HP: {self._hp.base_value}\n"


class PokemonStat(PokedexObject):
    """
        Categorizes pokemon stats.
    """

    def __init__(self, name, id, base_value=None, url=None, is_battle_only=None):
        super().__init__(name, id)
        self._url = url
        self._base_value = base_value
        self._is_battle_only = is_battle_only

    @property
    def url(self):
        return self._url

    @property
    def is_battle_only(self):
        return self._is_battle_only

    @property
    def base_value(self):
        return self._base_value

    @url.setter
    def url(self, value):
        self._url = value

    @is_battle_only.setter
    def is_battle_only(self, value):
        self._is_battle_only = value

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Id: {self._id}\n" \
               f"Base_Value: {self._base_value}\n" \
               f"Url: {self._url}\n"


class PokemonMove(PokedexObject):
    """
        Individual pokemon's move and their stats.
    """

    def __init__(self, name, id, level=None, generation=None, accuracy=None, pp=None, power=None, type=None,
                 damage_class=None, effect_short=None, url=None):
        super().__init__(name, id)
        self._level = level
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._type = type
        self._damage_class = damage_class
        self._effect_short = effect_short
        self._url = url

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def generation(self):
        return self._generation

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def pp(self):
        return self._pp

    @property
    def power(self):
        return self._power

    @property
    def type(self):
        return self._type

    @property
    def damage_class(self):
        return self._damage_class

    @property
    def effect_short(self):
        return self._effect_short

    def __str__(self):
        return f"Name: {self.name.title()}\n" \
               f"Id: {self._id}\n" \
               f"Generation: {self._generation}\n" \
               f"Accuracy: {self._accuracy}\n" \
               f"PP: {self._pp}\n" \
               f"Power: {self._power}\n" \
               f"Type: {self._type}\n" \
               f"Damage Class: {self._damage_class}\n" \
               f"Effect (short): {self._effect_short}\n"
