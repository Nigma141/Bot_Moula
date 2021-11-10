from discord_slash.utils.manage_components import *

regleMsg = f':heart: :orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart:  :blue_heart: ' \
           f':green_heart: :yellow_heart:  :orange_heart: :heart: \n' \
           f'                                    **Regle** \n' \
           f' Alors le boston des thuisses la regle c est \n' \
           f':dollar: faire un max de moulaga :dollar: \n' \
           f'voici les regles de ce serveur:\n ' \
           f':rainbow: sqrt(85)\n ' \
           f':rainbow: gagner de la moula \n ' \
           f':rainbow: gagner de la moula \n ' \
           f':rainbow: gagner de la moula \n ' \
           f':heart: :orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart:  :blue_heart: :green_heart: :yellow_heart:  :orange_heart: :heart: '

BienvenuMsg = f'Sal s jeune Boston des thuisses dans cette incroyable serveur\n' \
              f' Te voici dans ton salon privé ou tu pourras réaliser tout tes filouteries \n' \
              f' le but est simple se faire un max de Moulaga a la cote de la finance \n' \
              f'tu pars avec 1000 euros a toi de faire les bons investissments \n ' \
              f'les actions accessible pour le moment sont les entreprises du CAC40 '

BienvenuMsgAll = f'Nous accueillons aujourd hui un,une ou non binaire jeune boston \n'


def MessCompt(liste):
    print(liste)
    Mess = f'\n   <:lingots:904461381041016882>     Tu possède actuellement  : \n' \
           f':blue_book: sur ton compte : **' + str(liste[0]) + f'** € \n' \
                                                                f':green_book: dans ton portefeuille : **' + str(
        liste[1]) + f'** €'
    return (Mess)


def gestionListe(liste, index):
    options = [create_select_option('Retour', value=str(1))]
    for i in range(index, min(index+24, len(liste[index:]))):
        options += [create_select_option(str(liste[i-1]), value=str(i+1))]
    if len(liste[index:]) > 24:
        options[-1] = create_select_option("autre ...", value=str(25))
        fini=False
    else:
        fini =True
    return (options,fini)