% autre algorithme de duplication

% duplique un série de bâtons. La série est encadrée à droite et à gauche par un 0 au moins.
% Si l'oeil est positionné sur un 0, la série à dupliquer est vide.
% Si l'oeil est positionné sur un 1, la série à dupliquer est constituée de TOUS les bâtons
% à droite et à gauche de la position de l'oeil.

% -- Exemples de ruban d'entrée

   %  00111110000000  ou bien   00111110000000
   %    X                            X

% -- Dans ces deux exemples, la série à dupliquer est constitutée de 5 bâtons.

% Dans le ruban de sortie, la série initiale est séparée par un 0 de son double et l'oeil 
% est positionné sur le bâton le plus à gauche du double.
% -- Ruban de sortie des exemples précédents :

   %  00111110111110  
   %          X                            


si (0) fin} % arrêt immédiat si l'oeil est positionné sur un 0 (la série à dupliquer est vide)

% déplace l'oeil jusqu'au 0 à l'extrêmité droite de la série de bâtons
boucle 
  D 
  si (0) fin } 
}  
% puis se positionne sur la case immédiatement à droite
D 


boucle
  1
  boucle G si (0) fin }}
  boucle G si (1) fin }}
  G 
I
  si (0) fin } 
  D
  0
  boucle D si (1) fin }}
  boucle D si (0) fin }}
}

D
boucle D si (1) fin } 1 }
G
0
D
I



#