from __future__ import unicode_literals
import collections
import csv

def initialize_dicts(dicty, list_keys):
    dictionary = collections.OrderedDict()
    for key_list in list_keys:
        dictionary[key_list] = dicty[key_list]
    return dictionary

# def initialize_macros_csv():
#     with open('macro_list.csv', mode='a', newline='') as macro_list_file:
#         print("loading macro")
#         test = macro_places[1:]
#         test.insert(0, name_new_macro)
#         writer = csv.writer(macro_list_file, quotechar='"', quoting=csv.QUOTE_ALL)
#         writer.writerow(test)

button_addresses = {
    'B1': ['Entrée près de la porte'],
    'B2': ['Entrée vers le salon'],
    'B3': ['Corridor face à cuisine'],
    'B4': ['Salon'],
    'B5': ['Garde-Robe'],
    'B6': ['Corridor face à placard sono'],
    'B7': ['Sous le comptoir téléphone'],
    'B8': ['Sous le comptoir lavabos']
}
list_button_addresses = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
button_address = initialize_dicts(button_addresses, list_button_addresses)


motion_detect_addresses = {
    'D1': ['Garde-Robe'],
    'D2': ['Salle de Bain 1er Fond', 'Salle de Bain 1er Lavabo'],
    'D3': ['Corridor salle de bain'],
    'D4': ['Placard sono'],
    'D5': ['Salle invités Grand garde-robe'],
    'D6': ['Salle invités Petit garde-robe'],
    'D7': ['Laurent Garde-Robe'],
    'D8': ['Anne-Sophie Garde-Robe'],
    'D9': ['Anne-Sophie Rangement'],
    'D10': ['Lavage Plafond', 'Lavage Comptoir'],
    'D11': ['SdB 2 Toilette'],
    'D12': ['Maîtres Garde-Robe'],
    'D13': ['Maîtres Rangement'],
    'D14': ['Sous-Sol Marches', 'Sous-Sol Escalier Plafond'],
    'D15': ['Sous-Sol frigidaire'],
}
list_motion_detect_address = ['D1', 'D3', 'D2', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11',
                              'D12', 'D13', 'D14', 'D15']

motion_detect_address = initialize_dicts(motion_detect_addresses, list_motion_detect_address)

macros_nameses = {'All': [0, 'Garde-Robe', 'Entrée près de la porte', 'Entrée vers le salon', 'Corridor face à cuisine',
                            'Corridor face à placard sono', 'Salon', 'Sous le comptoir téléphone', 'Sous le comptoir lavabos',
                            'Ilôt central', 'Au dessus du lavabo', 'A côté du lavabo', 'Côté frigidaire', 'Côté salle à manger',
                            'Au-dessus de la table', 'Près de la fenêtre', 'Salle de Bain 1er Fond', 'Salle de Bain 1er Lavabo',
                            'Corridor statue', 'Corridor salle de bain', 'Murale bibliothèque vers sous-sol', 'Corridor bibliothèque vers sous-sol',
                            'Placard sono', 'Salle invités Au-dessus de la TV', 'Salle invités Au centre', 'Salle invités Au-dessus du lit',
                            'Salle invités Grand garde-robe', 'Salle invités Petit garde-robe', 'Marches 1', 'Marches 2',
                            'Laurent Au-dessus du lit', 'Laurent Au-dessus du bureau', 'Laurent Garde-Robe', 'Anne-Sophie Entrée',
                            'Anne-Sophie Garde-Robe', 'Anne-Sophie Rangement', 'Lavage Plafond', 'Lavage Comptoir', 'Statue',
                            'Mural Entrée chambre', 'SdB 2 Douche', 'SdB 2 Toilette', 'SdB 2 Comptoir', 'Maîtres Face à la fenêtre',
                            'Maîtres Au-dessus du lit', 'Maîtres Garde-Robe', 'Maîtres Rangement', 'Sous-Sol Marches',
                            'Sous-Sol Escalier Plafond', 'Sous-Sol Centre', 'Sous-Sol Près du mur', 'Sous-Sol Encastrés',
                            'Sous-Sol Près du panneau électrique', 'Sous-Sol frigidaire', 'Vide sanitaire Salle principale',
                            'Vide sanitaire géothermie', 'Vide sanitaire sous cuisine', 'Vide sanitaire hydrogène',
                            'Ext Entrée principale', 'Ext Entrée principale 2', 'Ext Entrée près du cabanon',
                            'Ext Entrée près du BBQ', 'Façade arrière', 'Terrain'],
                'Exemple': [0, 'Garde-Robe', 'Entrée près de la porte', 'Entrée vers le salon']}
list_macros_names = ['All', 'Exemple']
macros_names = initialize_dicts(macros_nameses, list_macros_names)


# # 'key': [brightness(int), places(int), places(int), ... ],
# places_name_brightness = {
#     'Garde-Robe': [0, 1, 3],
#     'Entrée près de la porte': [0, 2],
#     'Entrée vers le salon': [0, 3],
#     'Corridor face à cuisine': [0, 4],
# }
#
# places_name_brightness = collections.OrderedDict(places_name_brightness)


places_names = {
    'Garde-Robe': [0, 17],
    'Entrée près de la porte': [0, 0],
    'Entrée vers le salon': [0, 1],
    'Corridor face à cuisine': [0, 2],
    'Corridor face à placard sono': [0, 18],
    'Salon': [0, 3],
    'Sous le comptoir téléphone': [0, 19],
    'Sous le comptoir lavabos': [0, 20],
    'Ilôt central': [0, 4],
    'Au dessus du lavabo': [0, 21],
    'A côté du lavabo': [0, 22],
    'Côté frigidaire': [0, 23],
    'Côté salle à manger': [0, 24],
    'Au-dessus de la table': [0, 5],
    'Près de la fenêtre': [0, 6],
    'Salle de Bain 1er Fond': [0, 25],
    'Salle de Bain 1er Lavabo': [0, 25],
    'Corridor statue': [0, 26],
    'Corridor salle de bain': [0, 27],
    'Murale bibliothèque vers sous-sol': [0, 28],
    'Corridor bibliothèque vers sous-sol': [0, 28],
    'Placard sono': [0, 29],
    'Salle invités Au-dessus de la TV': [0, 7],
    'Salle invités Au centre': [0, 8],
    'Salle invités Au-dessus du lit': [0, 8],
    'Salle invités Grand garde-robe': [0, 30],
    'Salle invités Petit garde-robe': [0, 31],
    'Marches 1': [0, 32],
    'Marches 2': [0, 32],
    'Laurent Au-dessus du lit': [0, 9],
    'Laurent Au-dessus du bureau': [0, 9],
    'Laurent Garde-Robe': [0, 33],
    'Anne-Sophie Entrée': [0, 10],
    'Anne-Sophie Garde-Robe': [0, 34],
    'Anne-Sophie Rangement': [0, 35],
    'Lavage Plafond': [0, 36],
    'Lavage Comptoir': [0, 36],
    'Statue': [0, 37],
    'Mural Entrée chambre': [0, 38],
    'SdB 2 Douche': [0, 11],
    'SdB 2 Toilette': [0, 11],
    'SdB 2 Comptoir': [0, 39],
    'Maîtres Face à la fenêtre': [0, 12],
    'Maîtres Au-dessus du lit': [0, 12],
    'Maîtres Garde-Robe': [0, 40],
    'Maîtres Rangement': [0, 41],
    'Sous-Sol Marches': [0, 42],
    'Sous-Sol Escalier Plafond': [0, 42],
    'Sous-Sol Centre': [0, 13],
    'Sous-Sol Près du mur': [0, 13],
    'Sous-Sol Encastrés': [0, 13],
    'Sous-Sol Près du panneau électrique': [0, 13],
    'Sous-Sol frigidaire': [0, 43],
    'Vide sanitaire Salle principale': [0, 44],
    'Vide sanitaire géothermie': [0, 44],
    'Vide sanitaire sous cuisine': [0, 44],
    'Vide sanitaire hydrogène': [0, 44],
    'Ext Entrée principale': [0, 45],
    'Ext Entrée principale 2': [0, 45],
    'Ext Entrée près du cabanon': [0, 46],
    'Ext Entrée près du BBQ': [0, 47],
    'Façade arrière': [0, 48],
    'Terrain': [0, 49],
}

list_places_name = ['Garde-Robe', 'Entrée près de la porte', 'Entrée vers le salon', 'Corridor face à cuisine',
                    'Corridor face à placard sono', 'Salon', 'Sous le comptoir téléphone', 'Sous le comptoir lavabos',
                    'Ilôt central', 'Au dessus du lavabo', 'A côté du lavabo', 'Côté frigidaire', 'Côté salle à manger',
                    'Au-dessus de la table', 'Près de la fenêtre', 'Salle de Bain 1er Fond', 'Salle de Bain 1er Lavabo',
                    'Corridor statue', 'Corridor salle de bain', 'Murale bibliothèque vers sous-sol', 'Corridor bibliothèque vers sous-sol',
                    'Placard sono', 'Salle invités Au-dessus de la TV', 'Salle invités Au centre', 'Salle invités Au-dessus du lit',
                    'Salle invités Grand garde-robe', 'Salle invités Petit garde-robe', 'Marches 1', 'Marches 2',
                    'Laurent Au-dessus du lit', 'Laurent Au-dessus du bureau', 'Laurent Garde-Robe', 'Anne-Sophie Entrée',
                    'Anne-Sophie Garde-Robe', 'Anne-Sophie Rangement', 'Lavage Plafond', 'Lavage Comptoir', 'Statue',
                    'Mural Entrée chambre', 'SdB 2 Douche', 'SdB 2 Toilette', 'SdB 2 Comptoir', 'Maîtres Face à la fenêtre',
                    'Maîtres Au-dessus du lit', 'Maîtres Garde-Robe', 'Maîtres Rangement', 'Sous-Sol Marches',
                    'Sous-Sol Escalier Plafond', 'Sous-Sol Centre', 'Sous-Sol Près du mur', 'Sous-Sol Encastrés',
                    'Sous-Sol Près du panneau électrique', 'Sous-Sol frigidaire', 'Vide sanitaire Salle principale',
                    'Vide sanitaire géothermie', 'Vide sanitaire sous cuisine', 'Vide sanitaire hydrogène',
                    'Ext Entrée principale', 'Ext Entrée principale 2', 'Ext Entrée près du cabanon',
                    'Ext Entrée près du BBQ', 'Façade arrière', 'Terrain']
places_name = initialize_dicts(places_names, list_places_name)

