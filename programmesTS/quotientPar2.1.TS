% calcul du quotient par 2
% nb : il faut laisser au moins deux cases libres à gauche de l'oeil
% le principe de l'algorithme est de mettre à 0 un bâton sur 2 puis de "serrer"
% les bâtons restants vers la gauche

%                          nombre pair        0011111110000
%                          nombre impair      0011111111000
%                                               X

boucle
  D
  0
  D
%                          nombre pair        0010101110000
%                          nombre impair      0010101111000
%                                                   X
  si (0) fin }
}
I

% à partir d'ici, la distinction pair/impair n'a plus lieu d'être
%                                             0010101010000
%                                                       X
G
boucle
%                                             0010101010000
%                                                      X
  G
  I
  boucle G si (0) fin } }
%                                             0010101100000
%                                                  X
  G
  si (0) fin }
  D
%                                             0010101100000
%                                                  X
  1 
  boucle D si (0) fin } }
%                                             0010111100000
%                                                     X
  G 0
%                                             0010111000000
%                                                    X
}
D
D

I
#




