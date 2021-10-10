from urllib.request import Request
from argparse import ArgumentParser
from pokeretriever.api_manager import APIManager
from pokeretriever.poke_object import PokemonStat, PokemonAbility, PokemonMove, Pokemon, Stats


class Request:
    """
        Holds the json request details and user args
    """

    def __init__(self, mode, input, is_expanded, output):
        self.mode = mode
        self.input = input
        self.is_expanded = is_expanded
        self.output = output
        self.searches = []
        self.stat_urls = []
        self.ability_urls = []
        self.move_urls = []

    def __str__(self):
        return f"Mode: {self.mode}\n" \
               f"Input: {self.input}\n" \
               f"Is Expanded: {self.is_expanded}\n" \
               f"Output Path: {self.output}\n"


class RequestManager:
    """
        Manages the json requests
    """

    @staticmethod
    def parse_arguments_to_request() -> Request:
        """
            Adds helper arguments for the user and parses arguments to create a new Request.
        :return: request from check_input
        """

        # Adds arguments and helper text for the user
        parser = ArgumentParser()
        parser.add_argument("mode", help="It can be one of 3 specific modes, Pokemon, Ability, or Move.")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--inputfile", help="When providing a file name, the --inputfile flag "
                                               "must be provided.")
        group.add_argument("--inputdata", help="Either an id or a name. ")
        parser.add_argument("--expanded", action="store_true",
                            help="Determine whether or not to provide expanded data, only used with 'pokemon' mode.")
        parser.add_argument("--output", help="When providing an output file name, the --output flag"
                                             " must be provided.")

        # Makes a new request based on the arguments the user passed in
        try:
            args = parser.parse_args()
            if args.inputfile:
                request = Request(args.mode.lower(), args.inputfile, args.expanded, args.output)
            else:
                request = Request(args.mode.lower(), args.inputdata.lower(), args.expanded, args.output)
            r = RequestManager.check_input(request)
            return r
        except Exception as e:
            print(e)

    @staticmethod
    def check_input(request):
        """
            Checking whether the user entered a text file or not.
        :param request: Request json
        :return: request after it has appended the input
        """

        if request.input.endswith(".txt"):
            with open(request.input, 'r') as file:
                for line in file.readlines():
                    request.searches.append(line.rstrip('\n'))
        else:
            request.searches.append(request.input)
        return request


class RequestHandler:
    """
        Handles the json request.
    """

    async def handle_request(self, request):
        """
            Handles printing out the selected mode by the user
        :param request: Json request from pokeapi
        """

        api = APIManager()
        jsons = await api.manage_request(request)

        # Append non-expanded data to file
        if not request.is_expanded and request.output is not None:

            # Pokemon
            if request.mode == 'pokemon':
                fn = request.output
                with open(fn, "a", encoding="utf-8") as file:
                    for j in jsons:
                        file.write(str(self.get_pokemon(j)))
                        file.write("\n")
                    print("Appended pokemon data to file. Please check output file: " + request.output)
                    return

            # Ability
            elif request.mode == 'ability':
                fn = request.output
                with open(fn, "a", encoding="utf-8") as file:
                    for j in jsons:
                        file.write(str(self.get_ability(j)))
                        file.write("\n")
                    print("Appended pokemon ability data to file. Please check output file: " + request.output)
                    return

            # Move
            elif request.mode == 'move':
                fn = request.output
                with open(fn, "a", encoding="utf-8") as file:
                    for j in jsons:
                        file.write(str(self.get_move(j)))
                        file.write("\n")
                    print("Appended pokemon move data to file. Please check output file: " + request.output)
                    return

        # Append expanded data to file
        if request.is_expanded and request.mode == 'pokemon' and request.output is not None:
            stat_urls = []
            ability_urls = []
            move_urls = []
            pokemonlist = []

            for j in jsons:
                temppokemon = self.get_pokemon(j)
                pokemonlist.append(temppokemon)

                # Updating the urls for stats, ability, move
                for i in range(len(j['stats'])):
                    stat_urls.append(j['stats'][i]['stat']['url'])
                for a in j['abilities']:
                    ability_urls.append(a['ability']['url'])
                for i in range(len(j['moves'])):
                    move_urls.append(j['moves'][i]['move']['url'])

                # Adding the urls to request
                request.stat_urls.append(stat_urls)
                request.ability_urls.append(ability_urls)
                request.move_urls.append(move_urls)

                # Resetting lists
                stat_urls = []
                ability_urls = []
                move_urls = []

            jsons = await api.manage_request(request)

            # Setting pokemon stats' is_battle_only
            for pokemon in pokemonlist:
                pokemon.stats.speed.is_battle_only = (jsons[0][0][0]['is_battle_only'])
                pokemon.stats.sp_def.is_battle_only = (jsons[0][1][0]['is_battle_only'])
                pokemon.stats.sp_atk.is_battle_only = (jsons[0][2][0]['is_battle_only'])
                pokemon.stats.defense.is_battle_only = (jsons[0][3][0]['is_battle_only'])
                pokemon.stats.attack.is_battle_only = (jsons[0][4][0]['is_battle_only'])
                pokemon.stats.hp.is_battle_only = (jsons[0][5][0]['is_battle_only'])

            i = 0
            # Setting pokemons' ability
            for pokemon in pokemonlist:
                tempabilities = []
                for ability in pokemon.abilities:
                    tempurl = ability.url
                    tempability = self.get_ability(jsons[1][i][0])
                    tempability.url = tempurl
                    tempabilities.append(tempability)
                    i = i + 1
                pokemon.abilities = tempabilities

            i = 0
            # Setting pokemon's move
            for pokemon in pokemonlist:
                tempmoves = []
                for move in pokemon.moves:
                    templvl = move.level
                    tempurl = move.url
                    tempmove = self.get_move(jsons[2][i][0])
                    tempmove.url = tempurl
                    tempmove.level = templvl
                    tempmoves.append(tempmove)
                    i = i + 1
                pokemon.moves = tempmoves

            # File for results to be appended to
            fn = request.output
            with open(fn, "a", encoding="utf-8") as file:
                for pokemon in pokemonlist:
                    file.write(str(pokemon.expanded()))
                    file.write("\n")
                print("Appended pokemon expanded data to file. Please check output file: " + request.output)
                return

        # Expanded pokemon print to console
        if request.is_expanded and request.mode == 'pokemon':

            # Same code as expanded pokemon file appending
            stat_urls = []
            ability_urls = []
            move_urls = []
            pokemonlist = []

            for j in jsons:
                temppokemon = self.get_pokemon(j)
                pokemonlist.append(temppokemon)
                for i in range(len(j['stats'])):
                    stat_urls.append(j['stats'][i]['stat']['url'])
                for a in j['abilities']:
                    ability_urls.append(a['ability']['url'])
                for i in range(len(j['moves'])):
                    move_urls.append(j['moves'][i]['move']['url'])

                request.stat_urls.append(stat_urls)
                request.ability_urls.append(ability_urls)
                request.move_urls.append(move_urls)
                stat_urls = []
                ability_urls = []
                move_urls = []
            jsons = await api.manage_request(request)

            for pokemon in pokemonlist:
                pokemon.stats.speed.is_battle_only = (jsons[0][0][0]['is_battle_only'])
                pokemon.stats.sp_def.is_battle_only = (jsons[0][1][0]['is_battle_only'])
                pokemon.stats.sp_atk.is_battle_only = (jsons[0][2][0]['is_battle_only'])
                pokemon.stats.defense.is_battle_only = (jsons[0][3][0]['is_battle_only'])
                pokemon.stats.attack.is_battle_only = (jsons[0][4][0]['is_battle_only'])
                pokemon.stats.hp.is_battle_only = (jsons[0][5][0]['is_battle_only'])

            i = 0
            for pokemon in pokemonlist:
                tempabilities = []
                for ability in pokemon.abilities:
                    tempurl = ability.url
                    tempability = self.get_ability(jsons[1][i][0])
                    tempability.url = tempurl
                    tempabilities.append(tempability)
                    i = i + 1
                pokemon.abilities = tempabilities

            i = 0
            for pokemon in pokemonlist:
                tempmoves = []
                for move in pokemon.moves:
                    templvl = move.level
                    tempurl = move.url
                    tempmove = self.get_move(jsons[2][i][0])
                    tempmove.url = tempurl
                    tempmove.level = templvl
                    tempmoves.append(tempmove)
                    i = i + 1
                pokemon.moves = tempmoves

            for pokemon in pokemonlist:
                print(pokemon.expanded())

        # Non-expanded print to console
        else:
            if request.mode == 'pokemon':
                for j in jsons:
                    print(self.get_pokemon(j))
            elif request.mode == 'ability':
                for j in jsons:
                    print(self.get_ability(j))
            elif request.mode == 'move':
                for j in jsons:
                    print(self.get_move(j))

    def get_pokemon(self, json):
        """
            Returns pokemon with all of their required stats from the json request.
        :param json: Json request from pokeapi
        :return: Pokemon object with stats
        """

        # Setting the pokemon's base stats
        pName = json["name"]
        pId = int(json["id"])
        tempList = []
        height = int(json["height"])
        weight = int(json["weight"])

        # Parsing all stats to create a new Stats object
        for data in json["stats"]:
            tempid = int((data['stat']['url']).split('/')[6])
            temp = PokemonStat((data['stat']['name']), tempid, int((data['base_stat'])))
            temp.url = (data['stat']['url'])
            tempList.append(temp)

        stats = Stats(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4], tempList[5])

        types = []
        # Parsing type data
        for data in json["types"]:
            temp = data['type']['name']
            types.append(temp)

        abilities = []
        # Parsing ability data
        for data in json["abilities"]:
            tempid = int((data['ability']['url']).split('/')[6])
            temp = PokemonAbility((data['ability']['name']), tempid)
            temp.url = (data['ability']['url'])
            abilities.append(temp)

        moves = []
        # Parsing move data
        for i in range(len(json["moves"])):
            name = json["moves"][i]["move"]["name"]
            level = int(json["moves"][i]["version_group_details"][0]["level_learned_at"])
            temp = PokemonMove(name, i + 1, level)
            temp.url = json["moves"][i]["move"]["url"]
            moves.append(temp)

        # Create a new pokemon after all data has been parsed from the json
        return Pokemon(pName, pId, height, weight, stats, types, abilities, moves)

    def get_move(self, json):
        """
            Returns pokemon's move with all of their required stats from the json request.
        :param json: Json request from pokeapi
        :return: move object with stats
        """

        effect = json["effect_entries"][0]["short_effect"]

        # Converting the string into an int literal and then back into a string
        if "$effect_chance" in effect:
            effect = (effect.replace("$effect_chance", str(json['effect_chance'])))

        move = PokemonMove(json["name"], json["id"], 0, json["generation"]["name"],
                           json["accuracy"], json["pp"], json["power"],
                           json["type"]["name"], json["damage_class"]["name"],
                           effect)
        return move

    def get_ability(self, json):
        """
            Returns the pokemon's ability with all of their required stats from the json request.
        :param json: Json request from pokeapi.
        :return: ability object with stats
        """

        pokelist = json["pokemon"]
        templist = []

        for poke in pokelist:
            templist.append(poke['pokemon']['name'])

        ability = PokemonAbility(json["name"], json["id"],
                                 json["generation"]["name"],
                                 json["effect_entries"][0]["effect"],
                                 json["effect_entries"][0]["short_effect"],
                                 templist)
        return ability
