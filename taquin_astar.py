import copy
import time
# données des noeuds
F, G, H, JEU, PAPA = 0, 1, 2, 3, 4
# La liste des noeuds développés
# F cout tottale
# G cout de déplacement
# H Evaluation de l'heuristique
# Jeu l'état du noeud
# Noeud Pere


class Solveur:
    '''
    Le solveur de taquin
    '''

    def __init__(self, taquin):
        self.openList = []
        self.closedList = []
        self.nb_coups = 0
        self.taquinInitial = taquin
        self.numeroCaseVide = taquin.numeroCaseVide
        self.taille = len(taquin.jeu)
        # on met l'etat initial
        # openList comporte la liste des noeuds developpés
        self.openList.append([0, 0, 0, taquin.jeu, None])

    def dep_gauche(self, taquin, noeudCourant, colonne, ligne):

        if colonne > 0 and taquin[ligne][colonne - 1] == self.numeroCaseVide:
            tq = copy.deepcopy(taquin)
            tq[ligne][colonne], tq[ligne][colonne -
                                          1] = tq[ligne][colonne-1], tq[ligne][colonne]
            g = noeudCourant[G] + 1
            h = self.heuristique(tq)
            if not tq in self.closedList:
                i = self.indiceDansListeOuverte(tq)
                if i == -1:
                    self.openList.append(
                        [g + h, g, h, tq, noeudCourant])

                elif g + h < self.openList[0][F]:
                    self.openList[i] = [
                        g + h, g, h, tq, noeudCourant]

    def dep_droite(self, taquin, noeudCourant, colonne, ligne):
        if colonne < self.taille - 1 and taquin[ligne][colonne + 1] == self.numeroCaseVide:

            tq = copy.deepcopy(taquin)
            tq[ligne][colonne], tq[ligne][colonne +
                                          1] = tq[ligne][colonne+1], tq[ligne][colonne]
            g = noeudCourant[G]+1
            h = self.heuristique(tq)
            if not tq in self.closedList:
                i = self.indiceDansListeOuverte(tq)
                if i == -1:
                    self.openList.append([g+h, g, h, tq, noeudCourant])
                elif g+h < self.openList[i][F]:
                    self.openList[i] = [g + h, g, h, tq, noeudCourant]

    def dep_haut(self, taquin, noeudCourant, colonne, ligne):
        if ligne > 0 and taquin[ligne-1][colonne] == self.numeroCaseVide:
            tq = copy.deepcopy(taquin)
            tq[ligne][colonne], tq[ligne-1][colonne] = tq[ligne -
                                                          1][colonne], tq[ligne][colonne]
            g = noeudCourant[G]+1
            h = self.heuristique(tq)
            if not tq in self.closedList:
                i = self.indiceDansListeOuverte(tq)
                if i == -1:
                    self.openList.append([g+h, g, h, tq, noeudCourant])
                elif g+h < self.openList[i][F]:
                    self.openList[i] = [g + h, g, h, tq, noeudCourant]

    def dep_bas(self, taquin, noeudCourant, colonne, ligne):
        if ligne < self.taille - 1 and taquin[ligne+1][colonne] == self.numeroCaseVide:
            tq = copy.deepcopy(taquin)
            tq[ligne][colonne], tq[ligne+1][colonne] = tq[ligne +
                                                          1][colonne], tq[ligne][colonne]
            g = noeudCourant[G]+1
            h = self.heuristique(tq)
            if not tq in self.closedList:
                i = self.indiceDansListeOuverte(tq)
                if i == -1:
                    self.openList.append([g+h, g, h, tq, noeudCourant])
                elif g+h < self.openList[i][F]:
                    self.openList[i] = [g + h, g, h, tq, noeudCourant]

    def resoudre(self):
        print("Recherche de la solution...")

        while len(self.openList) > 0:
            self.nb_coups += 1

            noeudCourant = self.openList.pop(0)
            taquin = noeudCourant[JEU]

            if noeudCourant[JEU] == self.taquinInitial.etatF:
                return noeudCourant

            # genere toute les possibilité du graphe d'état
            for ligne in range(0, self.taille):
                for colonne in range(0, self.taille):
                    self.dep_gauche(taquin, noeudCourant, colonne, ligne)
                    self.dep_droite(taquin, noeudCourant, colonne, ligne)
                    self.dep_bas(taquin, noeudCourant, colonne, ligne)
                    self.dep_haut(taquin, noeudCourant, colonne, ligne)

            self.openList.sort()

        print(None)

    def indiceDansListeOuverte(self, jeu):
        for i in range(0, len(self.openList)):
            if self.openList[i][3] == jeu:
                return i
        return -1

    def heuristique(self, taquin):
        i = 0
        for ligne in range(0, self.taille):
            for colonne in range(0, self.taille):
                if taquin[ligne][colonne] != self.taquinInitial.etatF[ligne][colonne]:
                    i += 1
        return i


class Taquin:
    '''
    Le jeu en lui meme
    '''

    def __init__(self, jeu=None):
        if jeu != None:
            self.setJeu(jeu)
        self.etatF = []

    def __repr__(self):
        return '\n'.join(''.join(str(i)) for i in self.jeu)

    def setJeu(self, jeu):
        self.jeu = [list(i) for i in jeu]
        self.numeroCaseVide = len(self.jeu) - 1

        # pour ne pas le recalculer a chaque fois
    def setEtatfin(self, etatf):
        self.etatF = etatf

    def setNumeroCaseVide(self, i):
        self.numeroCaseVide = i

    def printEtatFini(self):
        print('\n' + '\n'.join(''.join(str(i)) for i in self.etatF))

    def termine(self):
        return [i for i in self.jeu] == self.etatF

    def resoudre(self):
        solveur = Solveur(self)
        res = solveur.resoudre()
        if res == None:
            print("Pas de solution trouvee")
            return
        print("Solution trouvee")

        L = []
        while res[PAPA] != None:
            L.append(res[PAPA])
            res = res[PAPA]
        L.reverse()

        for elem in L:
            print("\n \n E", elem[G])
            print("Coût totale F : {} \t Coût du déplacement : {}  \t Coût heuristique : {}".format(
                elem[F], elem[G], elem[H]))

            print('\n' + '\n'.join(''.join(str(i)) for i in elem[JEU]))
        self.printEtatFini()


'''
E0 = 
[[1, 3, 0], 
[8, 2, 4], 
[7, 6, 5]]

Ef = 
[[1, 2, 3],
[7, 0, 4],
[8, 5, 6]]
'''

if __name__ == "__main__":
    # Instanciation du taquin
    tq = Taquin()
    tq.setJeu([[2, 8, 3],
               [1, 6, 4],
               [7, 0, 5]])  # etat initiale du taquin
    tq.setNumeroCaseVide(0)  # le numero de la case qui se compre comme vide
    tq.setEtatfin([[1, 2, 3],
                   [8, 0, 4],
                   [7, 6, 5]])  # etat finale
    start = time.time()
    tq.resoudre()
    end = time.time()
    print("Taquin solved in {}".format(end - start))
