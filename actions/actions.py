from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import requests
import pandas as pd
import numpy as np


class ActionGetPokemon(Action):
    def name(self):
        return "action_get_pokemon"

    def run(self, dispatcher, tracker, domain):
        # We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon is None:
            response = "Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase. 😉"
        else:
            response = "I have a lot of knowledge about {}! 🧠 What do you want to know? Its types ? Its areas ? Its generation ? If it is a legendary Pokémon ? Or a recommandation ?".format(pokemon)
        dispatcher.utter_message(response)
        return []


class ActionGetType(Action):
    def name(self):
        return "action_get_type"

    def run(self, dispatcher, tracker, domain):
        #We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon!=None:
            #We perform our research
            pokemon=pokemon.lower()
            search="https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)
            info=requests.get(search)
            pokemon=pokemon.capitalize()
            if info.status_code==200:
                info=info.json()
                pokemon_types=[]
                for element in info['types']:
                        pokemon_types.append(element["type"]["name"])

                if len(pokemon_types)==1:
                    response = "{} has one type which is {}.".format(pokemon,*pokemon_types)
                else:
                    response="{} has two types which are {} and {}.".format(pokemon,*pokemon_types)
            else:
                response="Sorry, I do not know this pokemon : {}. 😥".format(pokemon)
        else:
            response="I need some help first. Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase. 😉"
        dispatcher.utter_message(response)
        return []

class ActionGetGeneration(Action):
    def name(self):
        return "action_get_generation"
    def run(self,dispatcher,tracker,domain):
        #We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon!=None:
            #We collect the generation from the entities
            generation_user = tracker.get_slot('generation')
            #We perform our research
            pokemon=pokemon.lower()
            search="https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)
            info=requests.get(search).json()
            #We search for the relevant information
            keys_sprites=info["sprites"]["versions"].keys()
            index=0
            generation_true=0
            for key_sprites in keys_sprites:
                index=index+1
                for key,value in info["sprites"]["versions"][key_sprites].items():
                    if value["front_default"]!=None:
                        generation_true=index
                        break
                if generation_true!=0:
                    break
            #We create the response
            pokemon=pokemon.capitalize()
            if generation_user!=None:
                generation_user=int(generation_user)
                if generation_user==generation_true:
                    response = "Yes, you are right. {} is from generation {}. 👏🥳".format(pokemon,generation_true)
                else:
                    response="No, {} is from generation {}. 🤦‍♂️".format(pokemon,generation_true)
            else:
                response="{} is from generation {}.".format(pokemon,generation_true)
        else:
            response="I need some help first. Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase."
        dispatcher.utter_message(response)
        #We delete the value in the slot for furthers answers
        return [SlotSet('generation',None)]

class ActionGetArea(Action):
    def name(self):
        return "action_get_area"

    def run(self, dispatcher, tracker, domain):
        #We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon!=None:
            #We perform our research
            pokemon=pokemon.lower()
            search="https://pokeapi.co/api/v2/pokemon/{}/encounters".format(pokemon)
            infos=requests.get(search)
            pokemon=pokemon.capitalize()
            if infos.status_code==200:
                infos=infos.json()
                location_area=[]
                for info in infos:
                    location_area.append(info["location_area"]["url"])
                locations=[]
                for area in location_area:
                    info_area=requests.get(area).json()
                    locations.append(info_area["location"]["url"])
                regions=[]
                for location in locations:
                    infog=requests.get(location).json()
                    regions.append(infog["region"]["name"])
                regions=[region.capitalize() for region in set(regions)]
                if len(regions)>0:
                    response="🗺 {} can be found in the following regions : {}. 🗺".format(pokemon,', '.join(regions))
                else:
                    response="{} is very uncommon, I do not have informations about its location. 🌌".format(pokemon)
            else:
                response="Sorry, I do not know this pokemon : {}. 😥".format(pokemon)
        else:
            response="I need some help first. Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase."
        dispatcher.utter_message(response)
        return []

class ActionGetLegendary(Action):
    def name(self):
        return "action_get_legendary"

    def run(self, dispatcher, tracker, domain):
        #We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon!=None:
            #We perform our research
            pokemon=pokemon.lower()
            search="https://pokeapi.co/api/v2/pokemon-species/{}".format(pokemon)
            info=requests.get(search)
            pokemon=pokemon.capitalize()
            if info.status_code==200:
                info=info.json()
                legendary=info["is_legendary"]
                if legendary:
                    response="{} is a legendary pokemon. It appearead in the world very rarely, but maybe you will have the chance to encounter it! ✨✨".format(pokemon)
                else:
                    response="{} is not a legendary pokemon. Anyways, it is still a great pokemon!".format(pokemon)
            else:
                response="Sorry, I do not know this pokemon : {}. 😥".format(pokemon)
        else:
            response="I need some help first. Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase."
        dispatcher.utter_message(response)
        return []


def cosine(u, m):
    u = np.array(u)
    m = np.array(m)
    numerator=u*m
    numerator=numerator.sum()
    u_norm=np.linalg.norm(u)
    m_norm=np.linalg.norm(m)
    denominator=u_norm*m_norm
    return numerator/denominator


class ActionGetRecommendation(Action):
    def name(self):
        return "action_get_recommendation"

    def run(self, dispatcher, tracker, domain):
        # We collect the name of the current pokemon
        pokemon = tracker.get_slot('pokemon_name')
        if pokemon != None:
            dataset=pd.read_csv(r".\actions\data_recommendation.csv")
            # We select the first vector, it contains the row we want to compare
            vector1=dataset[dataset["Pokemon Name"] == pokemon]
            vector1=vector1.iloc[:,2:]
            # We select all the others rows
            data=dataset[dataset["Pokemon Name"] != pokemon]
            # We create a dict to store the results
            results={}
            for index in range(len(data)):
                vector2=data.iloc[index,2:]
                name=data["Pokemon Name"].iloc[index]
                results[name]=cosine(vector1,vector2)
                results_sort={k:v for k,v in sorted(results.items(), key=lambda item:item[1])}
            final_results=[]
            for index in range(1,4):
                final_results.append(list(results_sort)[-index])
            response="♥️ If you love {}, you should take a look at these pokemons : {}.".format(pokemon,', '.join(final_results))
        else:
            response="I need some help first. Please, enter a valid pokemon name. Don't forget, pokemon are human being, its name take a uppercase."
        dispatcher.utter_message(response)
        return []
