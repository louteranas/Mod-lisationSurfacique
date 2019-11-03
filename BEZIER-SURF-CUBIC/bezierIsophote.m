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
                
function X = bezierIsophote(N, S, L, c, epsilon, u, v)

X=[];
counter = 1;
for i = 1:length(u)
    for j = 1:length(v)
        % on evalue l'expression
        Nij = [N(i, j, 1) N(i, j, 2) N(i, j, 3)];
        Nij = Nij/norm(Nij);
        if abs(dot(Nij, L) - c) < epsilon 
            X(counter, :) = S(i, j, :);
            counter = counter + 1;
        endif
    end    
end
end
    