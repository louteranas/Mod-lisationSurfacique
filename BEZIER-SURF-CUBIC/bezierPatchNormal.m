function N = bezierPatchNormal(B,u,v)

N=[];
%Xu=[];
%Xv=[];

% Matrice de changement de base
M = [
    1   0   0  0;
   -3   3   0  0;
    3  -6   3  0;
   -1   3  -3  1
];

MT = M'; % transpose de M

for i = 1:length(u)
    for j = 1:length(v)
        U  = [1  u(i)  u(i)^2  u(i)^3];
        DU = [0 1 2*u(i) 3*(u(i)^2)];
        VT = [1 v(j) v(j)^2 v(j)^3]'; 
        DVT = [0  1  2*v(j)  3*v(j)^2]';
        for k = 1:3 % evaluation en (u,v) pour les 3 dimensions
            Xu(i, j, k) = DU * M * B(:,:,k) * MT * VT;
            Xv(i, j, k) = U * M * B(:,:,k) * MT * DVT;
        end       
        N(i, j, :) = cross(Xu(i, j, :), Xv(i, j, :), 3)%/norm(cross(Xu(i, j, :), Xv(i, j, :), 3))
    end    
end
end
    