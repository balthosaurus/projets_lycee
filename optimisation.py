########## Modules ##########
import random
#import matplotlib.pyplot as plt
#from matplotlib.widgets import Button,RadioButtons
#from matplotlib.backend_bases import MouseButton
import time
#############################



########## Fonction de copie de matrice ##########
def copie_matrice(matrice):   # On crée la fonction servant à copier une grille entrée
    '''Fonction qui prend en argument une matrice et la copie dans une autre.'''
    n = len(matrice)
    copie = list()
    for lignes in range(n):
        copie.append(matrice[lignes][:])    
    return copie
##################################################





########## Produit scalaire vecteurs noyau ##########
## On rentre les quatres vecteurs du noyau de la matrice resolution 4x4
vecteurs_noyaux = \
    	[[0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0], \
         [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0], \
         [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0], \
         [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1]]

### On calcul le produit scalaire de la matrice A et des matrices formées avec les vecteurs du noyau
def produit_scalaire(vecteurs_noyaux, matrice):
    A = list ()
    for i in range (4):
        A += matrice[i]
    s = 0
    validité = True
    for vecteurs in vecteurs_noyaux :
        for lignes in range (16):
            s += ( vecteurs [ lignes ] * A[ lignes ])
        if s%2 != 0:
            validité = False
    return validité
#####################################################


def generation(taille):   # On génère un grille de taille 3 ou 4
    global vecteurs_noyaux
    '''Fonction qui prend en argument une taille et qui retourne une grille de 
       jeu aléatoire de la taille souhaitée sous forme de matrice.'''
    if taille == 3:   
        grille = [[0 for _ in range(3)] for _ in range(3)]
        for lignes in range(3):
            for colonnes in range(3):
                case = random.randint(0, 1)
                grille[lignes][colonnes] = case
        if grille == [[0 for _ in range(3)] for _ in range(3)]: 
            return generation(taille)
        
    elif taille == 4:
        grille = [[0 for _ in range(4)] for _ in range(4)]
        for lignes in range(4):
            for colonnes in range(4):
                case = random.randint(0, 1)
                grille[lignes][colonnes] = case
        if grille == [[0 for _ in range(4)] for _ in range(4)] or produit_scalaire(vecteurs_noyaux, grille) == False: 
            return generation(taille)
    return grille










met = False
    


########## Grille 4x4 : brute-force ##########
def appui(matrice, parcours = [[-1, -1]], iteration = 0):   # Une liste de liste rempli de 1 pour une longueur non-nul lors du "for i in..."
    '''Fonction qui prend en argument une matrice, un historique de parcours et
       une itération et qui simule un appui sur chaque case à l'iteration 
       actuelle.'''
    global met
    n = len(matrice)
    longueur = len(parcours)   # Taille du parcours, nombre de cases parcourus
    liste_grille = list()
    
    liste = list()   # On crée la liste servant à enregistrer les toutes premières positions
    if iteration == 0:   # On utilise ce critère pour créer la première liste des positions
        for lignes in range(n):
            for colonnes in range(n):
                liste.append([lignes, colonnes])            
    
    i = 0            
    
    for lignes in range(n):
        for colonnes in range(n):
            
                                  
            copie = copie_matrice(matrice)   # On copie la grille pour ne pas appuyer sur toute les case de la même grille
            copie_parcours = copie_matrice(parcours)   # On copie le parcours pour ne pas y entrer toutes les positions mais bien celle prise
            copie_parcours = copie_parcours + [[]]   # On concatène une liste vide pour pouvoir ajouter la case touchée, et ceci à chaque iteration
            
            valeur = True   # On met valeur à False par defaut
            for case in range(longueur):   
#                if parcours[case][0] == lignes and parcours[case][1] == colonnes :   # Méthode 1
                if lignes < parcours[case][0] or lignes <= parcours[case][0] and colonnes <= parcours[case][1] :   # Méthode 2
                    met = True   # Lié à la méthode 2 (sert à afficher quelle méthode est utilisé)
                    valeur = False
                
            if valeur is True:
                
                copie[lignes][colonnes] = (copie[lignes][colonnes]+1)%2
                if lignes+1 < n: 
                    copie[lignes+1][colonnes] = (copie[lignes+1][colonnes]+1)%2
                if lignes-1 >= 0:
                    copie[lignes-1][colonnes] = (copie[lignes-1][colonnes]+1)%2
                if colonnes+1 < n:
                    copie[lignes][colonnes+1] = (copie[lignes][colonnes+1]+1)%2
                if colonnes-1 >= 0:
                    copie[lignes][colonnes-1] = (copie[lignes][colonnes-1]+1)%2 
                    
                copie_parcours[longueur] = [lignes, colonnes]   # On ajoute la case touchée au parcours
                    
                if iteration == 0:   
                    copie_parcours[0] = liste[i]   # On rentre les premières cases appuyées dans le parcours                    
                    del copie_parcours[1]   # On supprime donc les -1...
                i+=1
                    
                liste_grille.append([copie, copie_parcours, iteration])   # On incrémentera "iteration" de 1 (elle ne dépassera donc pas n²)    
    return liste_grille


# On crée deux fonctions (dont une récursive) qui relancent le programme jusqu'à ce que la solution soit trouvée (ou non !)

def compilation(liste_de_grille):
    '''Fonction qui prend en argument une liste de grille et qui relance la 
       fonction "appui" pour chacune des grilles.'''
    liste = list()
#    print(), print(len(liste_de_grille))
    for listes in liste_de_grille :   # On trie toute les variables
        grille = listes[0]
        parcours = listes[1]    
        iteration = listes[2] + 1
        n = len(grille)
#        for i in grille:
#            print(i)
#        print()
        
        if grille == [[0 for _ in range(n)] for _ in range(n)]:
            return [True, parcours]
        elif iteration >= 16:
            return [False, parcours]
        
        nouvelle_grille = appui(grille, parcours, iteration)
        liste += brute_force(nouvelle_grille)   # On ajoute en bout de liste car on ne veut pas segmenter par cases
    return compilation(liste)
        
        
def brute_force(liste_de_grille):
    '''Fonction qui prend en argument une liste de grille et qui relance la 
       fonction "appui" pour chaqu'une des grilles
       (fonction complémentaire de "compilation").'''
    nouvelle_grille = list()   # On ajoute dans cette liste les grilles crées  
    for listes in liste_de_grille : 
        grille = listes[0]
        parcours = listes[1]    
        iteration = listes[2] 
        
        nouvelle_grille.append([grille, parcours, iteration])
    
    return nouvelle_grille
##############################################



################## EXECUTION ##################
    
grille = generation(4)

print(), print("grille de départ :")
for lignes in grille:
    print(lignes)
print()

debut=time.time()
sol = compilation(appui(grille))[1]
fin=time.time()

if met is False:
    print(), print("METHODE 1 :"), print()
else:
    print(), print("METHODE 2 :"), print()
    
print("La solution est :", sol, "\nCela a mis", fin-debut, "secondes.")
