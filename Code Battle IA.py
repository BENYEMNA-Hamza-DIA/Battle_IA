# -*- coding: utf-8 -*-
"""
Created on Sat May  8 23:36:34 2021

@author: BURY Jean-Baptiste BREGER Aymeric BENYEMNA Hamza
"""

import math
import numpy as np
import time


#%% Initialisation et copie



def Creation_plateau():
    plateau=np.empty([12,12],str)
    for i in range(12):
        for j in range(12):
            plateau[i][j]='-'
    
    return plateau

#on affiche le plateau a,vec le numero des lignes et des colonnes
def Affichage(plateau):
    i=0
    while(i<=12):
        j=0
        while(j<=12):
            if(i<1 and j>=0):
                if(j==0):
                    print(' ',end='\t')
                else:
                    print(j,end='\t')
            elif(i>=1 and j<1):
                print(i,end='\t')
            elif(i>=1 and j>=1):
                print(plateau[i-1][j-1],end='\t')    
            j+=1
        print('\n')
        i+=1

        
def Copie_plateau(plateau):
    copie=np.copy(plateau)
    return copie  


#%% Fonctions auxiliaires 




#retourne la liste de toutes les cases vides qui sont voisines des cases non vides
def Coups_possibles(plateau,CoupsJoues):
    choix=[]
    for c in CoupsJoues:
        i=c[0]
        j=c[1]
        if i<=10:
            if plateau[i+1][j] == '-' and not([i+1,j] in choix):
                choix.append([i+1,j])
            if j<=10:
                if plateau[i+1][j+1] =='-' and not([i+1,j+1] in choix):
                    choix.append([i+1,j+1])
                if plateau[i][j+1] == '-' and not([i,j+1] in choix):
                    choix.append([i,j+1])
                if j>=1:
                    if plateau[i+1][j-1] == '-' and not([i+1,j-1] in choix):
                        choix.append([i+1,j-1])
        elif j<=10 and not([i,j+1] in choix):
            if plateau[i][j+1] == '-':
                choix.append([i,j+1])
        if i>=1:
            if plateau[i-1][j] == '-' and not([i-1,j] in choix):
                choix.append([i-1,j])
            if j>=1:
                if plateau[i-1][j-1] =='-' and not([i-1,j-1] in choix):
                    choix.append([i-1,j-1])
                if plateau[i][j-1] == '-' and not([i,j-1] in choix):
                    choix.append([i,j-1])
            if j<=10:
                if plateau[i-1][j+1] == '-' and not([i-1,j+1] in choix):
                    choix.append([i-1,j+1])
        elif j>=1:
            if plateau[i][j-1] == '-' and not([i,j-1] in choix):
                choix.append([i,j-1])
    return choix


#permet d'evaluer une liste de coups en fonction d'un plateau de départ

def Eval(plateau,win,depth,coups):
    #si on peut gagner en  coup il faut absolument jouer celui ci, on retourne donc une valeur énorme
    if win!= 0 and len(coups) == 1:
        return 500000*win
    #on donne plus d'importance à la victoire si elle arrive plus rapidement
    elif win!= 0 and len(coups) <= depth:
        return win*400*(1+depth) + Score(plateau,coups)    
    elif win!= 0 and depth != 0:
        return win*200*(1+depth) + Score(plateau,coups)
        
    return win*150*(1+depth) + Score(plateau,coups)



#permet de connaitre le nb de cases vides
def Cases_vides(plateau):
    p=0
    for i in range(12):
        for j in range(12):
            if (plateau[i][j]=='-'):
                p+=1
    return p


#%% MinMaxAlphaBeta

#minmax recursif

def MinMaxAlphaBeta(plateau,CoupsJoues,depth,player,coups,alpha,beta):
    win = Win(plateau)
    
    if depth == 0 or win != 0 or Cases_vides(plateau)==0:
        return [Eval(plateau,win,depth,coups),coups]
    
    if player == 'O':
        
        maxEval = [-math.inf,coups]

        for v in Coups_possibles(plateau,CoupsJoues):   
            plateau_temp = Copie_plateau(plateau) 
            plateau_temp[v[0]][v[1]] = player
            eval_temp = MinMaxAlphaBeta(plateau_temp,CoupsJoues+[[v[0],v[1]]],depth-1,'X',coups+[[[v[0],v[1]],player]],alpha,beta)           
            if maxEval[0] < eval_temp[0]:
                maxEval[0] = eval_temp[0]
                maxEval[1] = []
                for c in eval_temp[1]:
                    maxEval[1]+=[[[c[0][0],c[0][1]],c[1]]] 
            alpha = max(alpha,eval_temp[0])
            if beta<=alpha:
                break
        return maxEval
    else:
        minEval = [math.inf,coups]

        for v in Coups_possibles(plateau,CoupsJoues): 
            plateau_temp = Copie_plateau(plateau)
            plateau_temp[v[0]][v[1]] = player
            eval_temp = MinMaxAlphaBeta(plateau_temp,CoupsJoues+[[v[0],v[1]]],depth-1,'O',coups+[[[v[0],v[1]],player]],alpha,beta)
            if minEval[0] > eval_temp[0]:
                minEval[0] = eval_temp[0]
                minEval[1] = []
                for c in eval_temp[1]:
                    minEval[1]+=[[[c[0][0],c[0][1]],c[1]]]   
            beta = min(beta,eval_temp[0])
            if beta<=alpha:
                break
        return minEval 

                       

#%% Action et Resul

#permet au joueur de saisri le coup qu'il veut jouer

def Action_joueur(plateau):
    a=[]
    y = eval(input("Saisir sur quelle colonne jouer :   "))-1
    while(y < 0 or y >= 12):
        y = eval(input("Veuillez saisir à nouveau sur quelle colonne jouer :   "))-1
    x = eval(input("Saisir sur quelle ligne jouer :   "))-1
    while(x < 0 or x >= 12):
        x = eval(input("Veuillez saisir à nouveau sur quelle ligne jouer :   "))-1
    a.append(x)
    a.append(y)
    return a

#retourne le coup que l'ia 

def Action_IA(plateau,player,profondeur,CoupsJoues):
    if Cases_vides(plateau)==144:
        m=("debut")
        coup = [5,5]
    else:
        m = MinMaxAlphaBeta(plateau,CoupsJoues,profondeur,player,[],-math.inf,math.inf)
        coup = m[1][0][0]
    return coup

#saisie sécurisé pour le joueur

def Resul_Joueur(plateau, a):
    while(plateau[a[0]][a[1]] != '-'):    
        print('\n'+"Impossible de jouer ce joup : réessayez")
        a = Action_joueur(plateau)
    plateau[a[0]][a[1]]='O'


def Resul_IA(plateau, a, player, profondeur,CoupsJoues):
    while(plateau[a[0]][a[1]]!='-'):
        a=Action_IA(plateau,player,profondeur,CoupsJoues)
    plateau[a[0]][a[1]] = player               


#%% Gagnant et fin de partie


#retoune +1 si O gnage, -1 si X gagne et 0 sinon

def Win(plateau):
    x = 'X'
    o = 'O'
    i = 0
    while i < 12 :
        j = 0
        while j < 12 : 
            
            if plateau[i][j] != '-':
                if i<= 8:
                    if [plateau[i][j],plateau[i+1][j],plateau[i+2][j],plateau[i+3][j]] == [x,x,x,x]:
                        return -1
                    if [plateau[i][j],plateau[i+1][j],plateau[i+2][j],plateau[i+3][j]] == [o,o,o,o]:
                        return 1
                    if  j <= 8 :
                        if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [x,x,x,x] or [plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2],plateau[i+3][j+3]] == [x,x,x,x]:
                            return -1
                        if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [o,o,o,o] or [plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2],plateau[i+3][j+3]] == [o,o,o,o]:
                            return 1
                    if  j >= 3:
                        if [plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2],plateau[i+3][j-3]] == [x,x,x,x]:
                            return -1
                        if [plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2],plateau[i+3][j-3]] == [o,o,o,o]:
                            return 1
                elif  j <= 8:
                    if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [x,x,x,x]:
                        return -1
                    if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [o,o,o,o]:
                        return 1
            j+=1
        i+=1
    return 0



#permet de savoir si le joueur rentré en parametre a gagné la partie, légèrement plus rapide que win lorsqu'on veut savoir si un joueur en particulier à gagné

def Winner(plateau,player):
    x = player
    i = 0
    while i < 12 :
        j = 0
        while j < 12 : 
            
            if plateau[i][j] == x:
                if i<= 8:
                    if [plateau[i][j],plateau[i+1][j],plateau[i+2][j],plateau[i+3][j]] == [x,x,x,x]:
                        return True
                    if  j <= 8 :
                        if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [x,x,x,x] or [plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2],plateau[i+3][j+3]] == [x,x,x,x]:
                            return True
                    if j >= 3:
                        if [plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2],plateau[i+3][j-3]] == [x,x,x,x]:
                            return True
                if  j <= 8:
                    if [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] == [x,x,x,x]:
                        return True            
            j+=1
        i+=1
    return False




#permet de savoir si la partie est fini, win correspond au resultat de la fonction winner
def TerminalTest(plateau,win):
    if(Cases_vides(plateau)==0) or win:
        return True
    else:
        return False

#%% Simulation : idée d'optimisation que l'on a délaissé par manque d'efficacité temporelle

# Pour chacune des parties, des profondeurs différentes sont joués pour
# obtenir des résultats différents afin de pourvoir comparer ces résultats
def Simulation(plateau):
    #Initialisation
    i=1
    simul=[]
    choix=[] 
    while(i<=3):
        if(i==1):
            profondeur1=3
            profondeur2=3
        elif(i==2):
            profondeur1=4
            profondeur2=3
        elif(i==3):
            profondeur1=3
            profondeur2=4

        plateau_simul=Copie_plateau(plateau)
        player = 'X'
        coups=[]
        tours=1
        win = Winner(plateau_simul,player)
        #Tour par tour
        while(TerminalTest(plateau_simul,win)==False):
            if(player == 'X'):
                a_IA1=Action_IA(plateau_simul,player,profondeur1)
                Resul_IA(plateau_simul, a_IA1, player, profondeur1)
                coups.append([a_IA1,'X'])
                win=Winner(plateau_simul, player)
                TerminalTest(plateau_simul,win)
                player = 'O'
            
            else:
                a_IA2=Action_IA(plateau_simul, player, profondeur2)
                Resul_IA(plateau_simul, a_IA2, player, profondeur2)
                coups.append([a_IA2,'O'])
                win=Winner(plateau_simul, player)
                TerminalTest(plateau_simul, win)
                player = 'X'
            tours+=0.5
        score=Score(plateau_simul,coups)
        simul.append((coups,score))
        i+=1
    Affichage(plateau_simul)
    print(sorted(simul, key= lambda x:x[1]))
    choix = sorted(simul, key= lambda x:x[1])[0][0][0][0]
    return choix
            

  

#%% Partie

def Partie(profondeur):
    #Initialisation
    plateau = Creation_plateau()
    tours=2
    Affichage(plateau)
    CoupsJoues=[]
    print("L'IA joue les X"+'\n'+"Le joueur joue les O")
    player = input("Saisir qui joue en 1er : saisir 'O' pour Joueur | 'X' pur l'IA :  ")
    while (player!='X' and player!='O'):
        print('\n'+"Saisie incorrecte")
        player = input("Saisir à nouveau qui joue en 1er : saisir 'O' pour Joueur | 'X' pur l'IA :  ")
    
    win = False
    winner = '-'
    #Tour par tour
    while(TerminalTest(plateau,win)==False):
        print('\n'+"Tour "+str(tours//2))
        if(player == 'O'):
            print('\n'+"C'est au joueur de jouer")   
            a_player=Action_joueur(plateau)
            Resul_Joueur(plateau,a_player)
            win=Winner(plateau,player)
            CoupsJoues.append(a_player)
            if win:
                winner = player
            print('\n'+"Le coup du joueur a été joué en "+'[ ligne = '+str(a_player[0]+1)+' , colonne = '+str(a_player[1]+1)+']')
            player = 'X'
        
        else:
            print('\n')
            input("Appuyer sur 'Entrée' pour lancer l'IA ")
            print('\n'+"C'est à l'IA de jouer")
            tps1 = time.time()
            a_IA=Action_IA(plateau,player,profondeur,CoupsJoues)
            Resul_IA(plateau, a_IA, player, profondeur,CoupsJoues)
            win=Winner(plateau,player)
            CoupsJoues.append(a_IA)
            if win:
                winner=player
            tps2 = time.time()
            print('\n'+"Le coup de l'IA a été joué en "+'[ligne='+str(a_IA[0]+1)+' , colonne='+str(a_IA[1]+1)+']')
            print("T=",tps2-tps1)
            player = 'O'
        print('\n')
        tours+=1
        Affichage(plateau)
    #Fin
    print('\n'+"La partie est finie")
    
    if(winner == 'X'):
        print('\n'+"L'IA a gagné")
    elif(winner == 'O'):
        print('\n'+"Joueur a gagné")
    else:
        print('\n'+"Match nul")
  
#%% Score

def Score(plateau,coups):
    score = 0
    x ='X'
    o= 'O'
    n = len(coups)
    cpt = 0

    
    
    #points attribués pour chaque type d'alignement
    
    a = 20 #[x,x], [o,o]
    b = 60 #[x,x,x], [o,o,o]
    c = 41 #[x,o,o],[o,o,x],[o,x,x],[x,x,o]
    d = 140 #[o,o,o,x],[o,o,x,o],[o,x,o,o],[x,o,o,o],[o,x,x,x],[x,o,x,x,x],[x,x,o,x],[x,x,x,o]
    e = 50 #[-,x,x,x,-],[-,o,o,o,-]   (2*b ?)
    f = 15 #[x,-,x], [o,-,o]
    g = 41 #[o,x,o],[x,o,x]   
    
    for cp in coups:
        i = cp[0][0]
        j = cp[0][1]
        plateau[i][j] = '-'
    for cp in coups:
        i = cp[0][0]
        j = cp[0][1]
        plateau[i][j] = cp[1]
        
    #diagonale1 = \
        
    #diagonale2 = /
        
        if i>=1:
            
            case = [plateau[i-1][j],plateau[i][j]] #colonne
            if case == [x,x]:
                 score -= a*(1+(n-cpt)/n)
            elif case == [o,o]:
                 score += a*(1+(n-cpt)/n)
            if j >=1 :
                case = [plateau[i][j-1],plateau[i][j]] #ligne
                if case == [x,x] :
                    score-=a*(1+(n-cpt)/n)
                elif case == [o,o] :
                    score+=a*(1+(n-cpt)/n)
                
                case = [plateau[i-1][j-1],plateau[i][j]] #diagonale1
                if  case == [x,x]:
                    score-=a*(1+(n-cpt)/n)
                elif case == [o,o]:
                    score+=a*(1+(n-cpt)/n)
            if j <= 10:
                case = [plateau[i-1][j+1],plateau[i][j]] #digonale2
                if case == [x,x]:
                    score-=a*(1+(n-cpt)/n)
                elif case == [o,o]:
                    score+=a*(1+(n-cpt)/n)

                    
        
            if i>=2:
                case = [plateau[i-2][j],plateau[i-1][j],plateau[i][j]] #colonne
                if case  == [x,x,x] :
                     score-=b*(1+(n-cpt)/n)
                elif case == [x,x,o] :
                     score+=c*(1+(n-cpt)/n)
                elif case == [x,o,x] :
                    score+=g*(1+(n-cpt)/n)
                elif case == [o,x,x] :
                    score+=c*(1+(n-cpt)/n)
                elif case == [x,'-',x] :
                    score-=f*(1+(n-cpt)/n)
                elif case == [o,o,o] :
                     score+=b*(1+(n-cpt)/n)
                elif case == [o,o,x] :
                    score-=c*(1+(n-cpt)/n)
                elif case == [o,x,o] :
                    score-=g*(1+(n-cpt)/n)
                elif case == [x,o,o] :
                    score-=c*(1+(n-cpt)/n)
                elif case == [o,'-',o] :
                    score+=f*(1+(n-cpt)/n)
                if j>=2:
                    case = [plateau[i-2][j-2],plateau[i-1][j-1],plateau[i][j]] #diagonale1
                    if case == [x,x,x] :
                        score-=b*(1+(n-cpt)/n)
                    elif case == [x,x,o] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,o,x] :
                        score+=g*(1+(n-cpt)/n)
                    elif case == [o,x,x] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,'-',x] :
                        score-=f*(1+(n-cpt)/n)
                    elif case == [o,o,o] :
                        score+=b*(1+(n-cpt)/n)
                    elif case == [o,o,x] :
                        score-=g*(1+(n-cpt)/n)
                    elif case == [o,x,o] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [x,o,o] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,'-',o] :
                        score+=f*(1+(n-cpt)/n)
                        
                    case = [plateau[i][j-2],plateau[i][j-1],plateau[i][j]] #ligne
                    if case == [x,x,x] :
                        score-=b*(1+(n-cpt)/n)   
                    elif case == [x,x,o] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,o,x] :
                        score+=g*(1+(n-cpt)/n)
                    elif case == [o,x,x] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,'-',x] :
                        score-=f*(1+(n-cpt)/n)
                    elif case == [o,o,o] :
                        score+=b*(1+(n-cpt)/n)   
                    elif case == [o,o,x] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,x,o] :
                        score-=g*(1+(n-cpt)/n)
                    elif case == [x,o,o] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,'-',o] :
                        score+=f*(1+(n-cpt)/n)
                if j<=9:
                    case = [plateau[i-2][j+2],plateau[i-1][j+1],plateau[i][j]] #diagonale2
                    if case == [x,x,x] :
                        score-=b*(1+(n-cpt)/n)   
                    elif case == [x,x,o] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,o,x] :
                        score+=g*(1+(n-cpt)/n)
                    elif case == [o,x,x] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,'-',x] :
                        score-=f*(1+(n-cpt)/n)
                    elif case == [o,o,o] :
                        score+=b*(1+(n-cpt)/n)   
                    elif case == [o,o,x] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,x,o] :
                        score-=g*(1+(n-cpt)/n)
                    elif case == [x,o,o] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,'-',o] :
                        score+=f*(1+(n-cpt)/n)
                if i>=3:
                    case = [plateau[i-3][j],plateau[i-2][j],plateau[i-1][j],plateau[i][j]] #colonne
                    if case == [x,x,x,o]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [x,x,o,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [x,o,x,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [o,x,x,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [o,o,o,x]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [o,o,x,o]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [o,x,o,o]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [x,o,o,o]:
                        score -= d*(1+(n-cpt)/n)
                        
                    if j>=3:
                        case = [plateau[i][j-3],plateau[i][j-2],plateau[i][j-1],plateau[i][j]] #ligne
                        if case == [x,x,x,o] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x] :
                            score-=d*(1+(n-cpt)/n)
                                                
                        case = [plateau[i-3][j-3],plateau[i-2][j-2],plateau[i-1][j-1],plateau[i][j]] #diagonale1
                        if case == [x,x,x,o]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score-=d*(1+(n-cpt)/n)    
                    if j<=8:
                        case =  [plateau[i-3][j+3],plateau[i-2][j+2],plateau[i-1][j+1],plateau[i][j]] #diagonale2
                        if case == [x,x,x,o]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score-=d*(1+(n-cpt)/n)
                   
                                          
        elif j>=1:
            case = [plateau[i][j-1],plateau[i][j]] #ligne
            if case == [x,x] :
                score-=a*(1+(n-cpt)/n)
            elif case == [o,o] :
                score+=a*(1+(n-cpt)/n)
            if j>=2:
                case = [plateau[i][j-2],plateau[i][j-1],plateau[i][j]] #ligne
                if  case == [x,x,x] :
                    score-=b*(1+(n-cpt)/n)   
                elif case == [x,x,o] :
                    score+=c*(1+(n-cpt)/n)
                elif case == [x,o,x] :
                    score+=g*(1+(n-cpt)/n)
                elif case == [o,x,x] :
                    score+=c*(1+(n-cpt)/n)
                elif case == [x,'-',x] :
                    score-=f*(1+(n-cpt)/n)
                elif case == [o,o,o] :
                    score+=b*(1+(n-cpt)/n)   
                elif case == [o,o,x] :
                    score-=c*(1+(n-cpt)/n)
                elif case == [o,x,o] :
                    score-=g*(1+(n-cpt)/n)
                elif case == [x,o,o] :
                    score-=c*(1+(n-cpt)/n)
                elif case == [o,'-',o] :
                    score+=f*(1+(n-cpt)/n)
                if j>=3:
                    case = [plateau[i][j-3],plateau[i][j-2],plateau[i][j-1],plateau[i][j]] #ligne
                    if case == [x,x,x,o] :
                        score+=d*(1+(n-cpt)/n)
                    elif case == [x,x,o,x] :
                        score+=d*(1+(n-cpt)/n)
                    elif case == [x,o,x,x] :
                        score+=d*(1+(n-cpt)/n)
                    elif case == [o,x,x,x] :
                        score+=d*(1+(n-cpt)/n)
                    elif case == [x,o,o,o] :
                        score-=d*(1+(n-cpt)/n)
                    elif case == [o,x,o,o] :
                        score-=d*(1+(n-cpt)/n)
                    elif case == [o,o,x,o] :
                        score-=d*(1+(n-cpt)/n)
                    elif case == [o,o,o,x] :
                        score-=d*(1+(n-cpt)/n)



                
        if i<= 10:
                case = [plateau[i][j],plateau[i+1][j]] #colonne
                if case == [x,x]:
                    score -= a*(1+(n-cpt)/n)
                elif case == [o,o]:
                    score += a*(1+(n-cpt)/n)
                if j <= 10 :
                    case = [plateau[i][j],plateau[i][j+1]] #ligne
                    if case == [x,x] :
                        score-=a*(1+(n-cpt)/n)
                    elif case :
                        score+=a*(1+(n-cpt)/n)
                    case = [plateau[i][j],plateau[i+1][j+1]] #diagonale1  
                    if case == [x,x]:
                        score-=a*(1+(n-cpt)/n)
                    elif case == [o,o]:
                        score+=a*(1+(n-cpt)/n)
                if j >= 1:
                    case = [plateau[i][j],plateau[i+1][j-1]] #diagonale2
                    if  case == [x,x]:
                        score-=a*(1+(n-cpt)/n)
                    elif case == [o,o]:
                        score+=a*(1+(n-cpt)/n)
                if i>=1:
                    case = [plateau[i-1][j],plateau[i][j],plateau[i+1][j]] #colonne
                    if case == [x,x,x] :
                        score-=b*(1+(n-cpt)/n)
                    elif case == [x,x,o] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [x,o,x] :
                        score+=g*(1+(n-cpt)/n)
                    elif case == [o,x,x] :
                        score+=c*(1+(n-cpt)/n)
                    elif case == [o,o,o] :
                        score+=b*(1+(n-cpt)/n)
                    elif  case == [o,o,x] :
                        score-=c*(1+(n-cpt)/n)
                    elif case == [o,x,o] :
                        score-=g*(1+(n-cpt)/n)
                    elif case == [x,o,o] :
                        score-=c*(1+(n-cpt)/n)
                            
                    
                    if j >= 1 and j<=10:
                        case = [plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1]] #diagonale1
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [o,x,x] :                        
                            score+=c*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)
                            
                        case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [o,x,x] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)

                        case = [plateau[i+1][j-1],plateau[i][j],plateau[i-1][j+1]] #diagonale2
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [o,x,x] :                        
                            score+=c*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)
                        
                            
                if i>=2:
                    case = [plateau[i-2][j],plateau[i-1][j],plateau[i][j],plateau[i+1][j]] #colonne
                    if case == [x,x,x,o]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [x,x,o,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [x,o,x,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [o,x,x,x]:
                        score +=d*(1+(n-cpt)/n)
                    elif case == [o,o,o,x]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [o,o,x,o]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [o,x,o,o]:
                        score -= d*(1+(n-cpt)/n)
                    elif case == [x,o,o,o]:
                        score -= d*(1+(n-cpt)/n)
                        
                        
                    if j<=9 and j>=1:
                        case = [plateau[i-2][j+2],plateau[i-1][j+1],plateau[i][j],plateau[i+1][j-1]] #diagonale 2
                        if case == [x,x,x,o]:
                            score+=d*(1+(n-cpt)/n)
                        elif  case == [x,x,o,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif  case == [o,x,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif  case == [o,o,o,x]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score-=d*(1+(n-cpt)/n)
                    if j>=2 and j<=10:
                        case =  [plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                        if case == [x,x,x,o] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x] :
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o] :
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x] :
                            score-=d*(1+(n-cpt)/n)
                        
                        case = [plateau[i-2][j-2],plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1]] #diagonale1
                        if case == [x,x,x,o]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x]:
                            score+=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score-=d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score-=d*(1+(n-cpt)/n)
                    if i>= 3:
                            case = [plateau[i-3][j],plateau[i-2][j],plateau[i-1][j],plateau[i][j],plateau[i+1][j]] #colonne
                            if case == ['-',x,x,x,'-']:
                                score -=e*(1+(n-cpt)/n)
                            elif case == ['-',o,o,o,'-']:
                                score +=e*(1+(n-cpt)/n)
                            if j>=3 and j<=10:
                                case = [plateau[i][j-3],plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                                if case == ['-',x,x,x,'-'] :
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-'] :
                                    score+=e*(1+(n-cpt)/n)
                                
                                case = [plateau[i-3][j-3],plateau[i-2][j-2],plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1]] #diagonale1
                                if case == ['-',x,x,x,'-']:
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-']:
                                    score+=e*(1+(n-cpt)/n)

                            if j<=8 and j>=1:
                                case = [plateau[i-3][j+3],plateau[i-2][j+2],plateau[i-1][j+1],plateau[i][j],plateau[i+1][j-1]] #diagonale2
                                if case == ['-',x,x,x,'-']:
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-']:
                                    score+=e*(1+(n-cpt)/n)    
                    
                    
                if i<= 9:
                    case = [plateau[i][j],plateau[i+1][j],plateau[i+2][j]] #colonne
                    if case == [x,x,x]:
                        score -= b*(1+(n-cpt)/n)
                    elif case == [o,x,x]:
                        score += c*(1+(n-cpt)/n)
                    elif case == [x,x,o]:
                        score += c*(1+(n-cpt)/n)
                    elif case == [x,o,x]:
                        score += g*(1+(n-cpt)/n)
                    elif case == [x,'-',x]:
                        score -= f*(1+(n-cpt)/n)
                    elif case == [o,o,o]:
                        score += b*(1+(n-cpt)/n)
                    elif case == [x,o,o]:
                        score -= c*(1+(n-cpt)/n)
                    elif case == [o,o,x]:
                        score -= c*(1+(n-cpt)/n)
                    elif case == [o,x,o]:
                        score -= g*(1+(n-cpt)/n)
                    elif case == [o,'-',o]:
                        score += f*(1+(n-cpt)/n)
                    
                    if j <= 9 :
                        case = [plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif case == [o,x,x] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [x,'-',x] :
                            score-=f*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [o,'-',o] :
                            score+=f*(1+(n-cpt)/n)
                        
                        case = [plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2]] #diagonale1
                        if  case == [x,x,x]:
                            score-=b*(1+(n-cpt)/n)
                        elif case == [o,x,x]:
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,x,o]:
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x]:
                            score+=g*(1+(n-cpt)/n)
                        elif case == [x,'-',x]:
                            score-=f*(1+(n-cpt)/n)
                        elif case == [o,o,o]:
                            score+=b*(1+(n-cpt)/n)
                        elif case == [x,o,o]:
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,o,x]:
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o]:
                            score-=g*(1+(n-cpt)/n)
                        elif case == [o,'-',o]:
                            score+=f*(1+(n-cpt)/n)
                    if j >= 2:
                        case = [plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2]] #diagonale2
                        if case == [x,x,x]:
                            score-=b*(1+(n-cpt)/n)
                        elif case == [o,x,x]:
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,x,o]:
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x]:
                            score+=g*(1+(n-cpt)/n)
                        elif case == [x,'-',x]:
                            score-=f*(1+(n-cpt)/n)
                        elif case == [o,o,o]:
                            score+=b*(1+(n-cpt)/n)
                        elif case == [x,o,o]:
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,o,x]:
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o]:
                            score-=g*(1+(n-cpt)/n)
                        elif case == [o,'-',o]:
                            score+=f*(1+(n-cpt)/n)
                    if i>= 1:
                        case = [plateau[i-1][j],plateau[i][j],plateau[i+1][j],plateau[i+2][j]] #colonne
                        if case == [x,x,x,o]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score -= d*(1+(n-cpt)/n)
                        if j>=1 and j<=9:
                            case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                            if case == [x,x,x,o] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x] :
                                score-=d*(1+(n-cpt)/n)
                            
                            case = [plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2]] #diagonale1
                            if case == [x,x,x,o]:
                                score+=d*(1+(n-cpt)/n)
                            elif  case == [x,x,o,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif  case == [o,o,o,x]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif  case == [o,x,o,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o]:
                                score-=d*(1+(n-cpt)/n)
                        if j<=10 and j>=2:
                            case = [plateau[i-1][j+1],plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2]] #diagonale2
                            if case == [x,x,x,o]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif  case == [o,x,o,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o]:
                                score-=d*(1+(n-cpt)/n)
                        if i>= 2:
                            case = [plateau[i-2][j],plateau[i-1][j],plateau[i][j],plateau[i+1][j],plateau[i+2][j]] #colonne
                            if  case == ['-',x,x,x,'-']:
                                score -=e*(1+(n-cpt)/n)
                            elif case == ['-',o,o,o,'-']:
                                score +=e*(1+(n-cpt)/n)
                            if j>=2 and j<=9:
                                case = [plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                                if case == ['-',x,x,x,'-'] :
                                    score-=e*(1+(n-cpt)/n)
                                elif  case == ['-',o,o,o,'-'] :
                                    score+=e*(1+(n-cpt)/n)
                                
                                case = [plateau[i-2][j-2],plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2]] #diagonale1
                                if case == ['-',x,x,x,'-']:
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-']:
                                    score+=e*(1+(n-cpt)/n)

                                case = [plateau[i-2][j+2],plateau[i-1][j+1],plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2]] #diagonale2
                                if case == ['-',x,x,x,'-']:
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-']:
                                    score+=e*(1+(n-cpt)/n)
                            
                            
                        
                    if i<= 8:
                        case = [plateau[i][j],plateau[i+1][j],plateau[i+2][j],plateau[i+3][j]] #colonne
                        if case == [x,x,x,o]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [x,x,o,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [x,o,x,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [o,x,x,x]:
                            score +=d*(1+(n-cpt)/n)
                        elif case == [o,o,o,x]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [o,o,x,o]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [o,x,o,o]:
                            score -= d*(1+(n-cpt)/n)
                        elif case == [x,o,o,o]:
                            score -= d*(1+(n-cpt)/n)
                        if j <= 8 :
                            case = [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] #ligne
                            if case == [x,x,x,o] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x] :
                                score-=d*(1+(n-cpt)/n)
                             
                            case = [plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2],plateau[i+3][j+3]] #diagonale1
                            if case == [x,x,x,o]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o]:
                                score-=d*(1+(n-cpt)/n)
                
                            if i>=1:
                                case = [plateau[i-1][j],plateau[i][j],plateau[i+1][j],plateau[i+2][j],plateau[i+3][j]] #colonne
                                if case == ['-',x,x,x,'-']:
                                    score -=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-']:
                                    score +=e*(1+(n-cpt)/n)
                                if j>=1:
                                    case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] #ligne
                                    if case == ['-',x,x,x,'-'] :
                                        score-=e*(1+(n-cpt)/n)
                                    elif case == ['-',o,o,o,'-'] :
                                        score+=e*(1+(n-cpt)/n)
                                   
                                    case = [plateau[i-1][j-1],plateau[i][j],plateau[i+1][j+1],plateau[i+2][j+2],plateau[i+3][j+3]] #diagonale1
                                    if case == ['-',x,x,x,'-']:
                                        score-=e*(1+(n-cpt)/n)
                                    elif case == ['-',o,o,o,'-']:
                                        score+=e*(1+(n-cpt)/n)
                                if j>=3 and j<=10:
                                    
                                    case = [plateau[i-1][j+1],plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2],plateau[i+3][j-3]] #diagonale2
                                    if case == ['-',x,x,x,'-']:
                                        score-=e*(1+(n-cpt)/n)
                                    elif case == ['-',o,o,o,'-']:
                                        score+=e*(1+(n-cpt)/n)
                                
                        if j >= 3:
                            case = [plateau[i][j],plateau[i+1][j-1],plateau[i+2][j-2],plateau[i+3][j-3]] #diagonale2
                            if case == [x,x,x,o]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x]:
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o]:
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x]:
                                score-=d*(1+(n-cpt)/n)
                 
                             
                                                                                        
                elif j <= 10:
                    case = [plateau[i][j],plateau[i][j+1]] #ligne
                    if case == [x,x]:
                        score-=15*(1+(n-cpt)/n)
                    elif case == [o,o]:
                        score+=15*(1+(n-cpt)/n)
                    if j >= 1:
                        case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif  case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [o,x,x] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)
                        if j>=2 :
                            case = [plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                            if case == [x,x,x,o] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x] :
                                score-=d*(1+(n-cpt)/n)
                            if j>=3:
                                case = [plateau[i][j-3],plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1]] #ligne
                                if case == ['-',x,x,x,'-'] :
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-'] :
                                    score+=e*(1+(n-cpt)/n)
                    if j <= 9:
                        case = [plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                        if case == [x,x,x] :
                            score-=b*(1+(n-cpt)/n)
                        elif case == [o,x,x] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,x,o] :
                            score+=c*(1+(n-cpt)/n)
                        elif case == [x,o,x] :
                            score+=g*(1+(n-cpt)/n)
                        elif case == [x,'-',x] :
                            score-=f*(1+(n-cpt)/n)
                        elif case == [o,o,o] :
                            score+=b*(1+(n-cpt)/n)
                        elif case == [o,o,x] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [x,o,o] :
                            score-=c*(1+(n-cpt)/n)
                        elif case == [o,x,o] :
                            score-=g*(1+(n-cpt)/n)
                        elif case == [o,'-',o] :
                            score+=f*(1+(n-cpt)/n)
                        if j>=1:
                            case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                            if case == [x,x,x,o] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x] :
                                score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o] :
                                score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x] :
                                score-=d*(1+(n-cpt)/n)
                            if j>=2 :
                                case = [plateau[i][j-2],plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2]] #ligne
                                if case == ['-',x,x,x,'-'] :
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-'] :
                                    score+=e*(1+(n-cpt)/n)
                            
                        if j <= 8:
                            case = [plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] #ligne
                            if case == [x,x,x,o] :
                                    score+=d*(1+(n-cpt)/n)
                            elif case == [x,x,o,x] :
                                    score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,x,x] :
                                    score+=d*(1+(n-cpt)/n)
                            elif case == [o,x,x,x] :
                                    score+=d*(1+(n-cpt)/n)
                            elif case == [x,o,o,o] :
                                    score-=d*(1+(n-cpt)/n)
                            elif case == [o,x,o,o] :
                                    score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,x,o] :
                                    score-=d*(1+(n-cpt)/n)
                            elif case == [o,o,o,x] :
                                    score-=d*(1+(n-cpt)/n)
                            if j>=1:
                                case = [plateau[i][j-1],plateau[i][j],plateau[i][j+1],plateau[i][j+2],plateau[i][j+3]] #ligne
                                if case == ['-',x,x,x,'-'] :
                                    score-=e*(1+(n-cpt)/n)
                                elif case == ['-',o,o,o,'-'] :
                                    score+=e*(1+(n-cpt)/n)
        cpt+=1    
    return score

        
#%% Main

Partie(4)