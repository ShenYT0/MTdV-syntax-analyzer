%                                             0011100011111000
%                                               X
I
boucle si (0) fin } D }
boucle D si (1) fin } }
boucle D si (0) fin } }
%                                             0011100011111000
%                                                          X
D
1
%                                             0011100011111010
%                                                           X
G
boucle G si (0) fin } }
boucle G si (1) fin } }
%                                             0011100011111010
%                                                 X
boucle
  0
  % était-ce le dernier 1 ? si oui, la multiplication est terminée
  G
%                                             0011000011111010
%                                                X
  si (0) fin }
  D
%                                             0011000011111010
%                                                 X
  boucle D si (1) fin } }
  boucle D si (0) fin } }
  G
%                                             0011000011111010
%                                                         X
  boucle
    0
    % était-ce le dernier 1 ? si oui, la boucle sur le 2nd nombre est terminée
    G
%                                             0011000011110010
%                                                        X
    si (0) fin }

    D
    boucle D si (1) fin } }
    boucle D si (0) fin } }
%                                             001100001111001000
%                                                            X
    1
%                                             001100001111001100
%                                                            X
    boucle G si (0) fin } }
    boucle G si (1) fin } }
%                                             001100001111001100
%                                                        X
  }
  D
  1
%                                             0011000010000011111
%                                                     X
  boucle D si (1) fin } }
  G
%                                             0011000010000011111
%                                                          X
  boucle G si (1) fin } 1 }
%                                             0011000011111011111
%                                                     X
  boucle G si (1) fin } }
  %fin
%                                             0011000011111011111
%                                                X
%  I P
}
%                                             00000000111110111111111
%                                                X
boucle D si (1) fin } }
boucle 0 D si (0) fin } }
D
I
%                                             00000000000000111111111
%                                                                        X                    

#

