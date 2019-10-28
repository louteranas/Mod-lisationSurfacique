%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Evaluation d'un patch de Bezier aux parametres u,v
%
% Input:
%  - matrix B de 16 points de controle de dim 3
%     chaque point de controle a 3 coordonnes (x,y,z)
%     taille de B: 4x4x3
%     B(:,:,k) keme coordonnes des16  points de controle, k=1,2,3
%     B(i,j,:) les 3 coordonnes du point de controle b_ij
%  - u Vecteur de |u|=length(u) valeurs de parametre en u
%  - v Vecteur de |v|=length(v) valeurs de parametre en v

% Output:
%  - matrix S avec la grille de |u|x|v| points 3D sur la surface
%    La structure de S est similaire a celle de B.
%    Taille de S: |u|x|v|x3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function N = bezierPatchNormal(B,u,v)

    N=[];
    Xu=[];
    Xv=[];
    
    % Matrice de changement de base
    M = [
        1   0   0  0;
       -3   3   0  0;
        3  -6   3  0;
       -1   3  -3  1
        ];
    
    P3 = [
          1  0  0;
         -2  2  0;
          1 -2  1;
    ]
    
    MT = M'; % transpose de M
    PT = P3'; % transpose de P3
    
    for i = 1:length(u)
        for j = 1:length(v)
            U  = [1 u(i) u(i)^2 u(i)^3];
            DU = [1 u(i) u(i)^2];
            VT = [1 v(j) v(j)^2 v(j)^3]'; 
            DVT = [1 v(j) v(j)^2];
            for k = 1:3 % evaluation en (u,v) pour les 3 dimensions
                A1 = [];
                A1(i,j)  = B(mod(i+1, length(u)), j, k) - B(i, j, k);
                A2 = [];
                A2(i,j)  = B(i, mod(j+1, length(u)), k) - B(i, j, k);
                Xu = 3 * DU * P3 * A1 * MT * VT;
                Xv = 3 * U * M * A2 * PT * DVT;
                N(i,j,k) = [Xu/length(Xu *Xv) Xv/length(Xu *Xv);
            end         
        end    
    end
    