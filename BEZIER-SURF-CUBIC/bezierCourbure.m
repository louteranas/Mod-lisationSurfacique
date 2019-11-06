function Courbures = bezierCourbure(N, B, u, v)

Courbures=[];

% Matrice de changement de base
M = [
    1   0   0  0;
   -3   3   0  0;
    3  -6   3  0;
   -1   3  -3  1
];

MT = M'; % transpose de M

%% la premiere etape est de calculer H et G 
%%  on a besoin des derive de X par rapport a  u et v 
for i = 1:length(u)
    for j = 1:length(v)
        U  = [1  u(i)  u(i)^2  u(i)^3];
        DU = [0 1 2*u(i) 3*(u(i)^2)];
        DUU = [0 0 2 6*(u(i))];
        
        VT = [1 v(j) v(j)^2 v(j)^3]'; 
        DVT = [0  1  2*v(j)  3*v(j)^2]';
        DVVT = [0  0  2  6*v(j)]';
        
        for k = 1:3 % evaluation en (u,v) pour les 3 dimensions
            Xu(i, j, k) = DU * M * B(:,:,k) * MT * VT;
            Xuu(i, j, k) = DUU * M * B(:,:,k) * MT * VT;
            
            Xuv(i, j, k) = DU * M * B(:,:,k) * MT * DVT;
            
            Xv(i, j, k) = U * M * B(:,:,k) * MT * DVT;
            Xvv(i, j, k) = U * M * B(:,:,k) * MT * DVVT;
        end 
        % G matrice
        G = [
            dot(Xu(i, j, :), Xu(i, j, :)) dot(Xu(i, j, :), Xv(i, j, :));
            dot(Xv(i, j, :), Xu(i, j, :)) dot(Xv(i, j, :), Xv(i, j, :))
        ];
        % H matrice 
        H = [
            dot(Xuu(i, j, :), N(i, j, :)) dot(Xuv(i, j, :), N(i, j, :));
            dot(Xuv(i, j, :), N(i, j, :)) dot(Xvv(i, j, :), N(i, j, :))
        ];
        
        %%  K1 et K2 sont  les valeurs propre de H.G-1
        res = H/G;
        ValP = eig(res);
        k1 = ValP(1);
        k2 = ValP(2);
        disp(k1*k2);
        Courbures(i, j) = k1*k2;
    end    
end
end
    