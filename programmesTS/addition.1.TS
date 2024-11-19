% réalise la somme de deux nombres.
% les nombres doivent être séparés par un moins un 0
% l'oeil doit être positionné sur le premier bâton du premier nombre

I
                                                         %  00111001111100
                                                         %    X
% déplacement de l'oeil à l'extrêmité droite du 1er nombre
boucle 
  si (0) fin }
  D
}
                                                         %  00111001111100
                                                         %       X
% l'oeil est sur un 0
boucle
  boucle 
    D
    si (1) fin }
  }

                                                         %  00111001111100
                                                         %         X

  % l'oeil est sur le bâton le plus à gauche du 2nd nombre
  % remplacement par un 0
  0
                                                         %  00111000111100
                                                         %         X

  % était-ce le dernier bâton du 2nd nombre ? si oui, arrêt de la boucle
  D
  si (0) fin }
  % ajout d'un bâton à la fin du 1er nombre
  boucle 
    G
    si (1) fin }
  }
  D
  1
                                                         %  00111100111100
                                                         %       X

  % positionnement de l'oeil sur le premier 0 qui suit le premier nombre
  D
                                                         %  00111100111100
                                                         %       X
} 

% positionnement de l'oeil au début du résultat
boucle 
  G
  si (1) fin }
}
boucle 
  G
  si (0) fin }
}
D

I

#