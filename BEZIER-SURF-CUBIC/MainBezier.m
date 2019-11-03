close all, clear all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calcul et visualisation de surfaces de Bezier
%
% Input: fichoer ascii avec 16xnp points de controle
%
% Les patches sont individuellement evalues en un 
% nombre fixe de parametres (u,v).
%
% Parametres: 
% num_p : nombre de valeurs de parametres = nombre de points de controle
% num_n : nombre de normales calcules (pour le calcul des isophotes)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%BezierSurf = load('surface1');  % read control points
%BezierSurf = load('surface2'); % read control points
%BezierSurf = load('surface4'); % read control points
BezierSurf = load('surface1'); % read control points
%load('teapot'); %loading matrix B
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
num_p=20;                    % nombre de valeurs de parametre en direction u et v
num_n=20;		     % plus num_p est grand plus la surface paraitra lisse
			     % et plus le calcul sera long

%-------------------------------------------------
[nb,~] = size(BezierSurf) % nombre de points de controle dans le fichier
np = floor(nb/16) % nombre de patches composant la surface
                   % Il faudrait verivier que nb est un multiple de 16 %
% Matrice B des points de controle
for k=1:np
  for i=1:4
    for j=1:4
      B(i,j,1,k) = BezierSurf((i-1)*4+j+(k-1)*16,1);
      B(i,j,2,k) = BezierSurf((i-1)*4+j+(k-1)*16,2);
      B(i,j,3,k) = BezierSurf((i-1)*4+j+(k-1)*16,3);
    end
  end
end


% La matrice B stocke tous les points de controle de tous les patchs
% B(:,:,:,k) sont tous les points de controle du patch k
% La dimension de B(:,:,:,k) est 4 x 4 x 3, i.e., 16 points de controle
% a 3 coordonnees (x,y,z)

% B(:,:,1,k): x-coordonnes des points de controle du patch k comme matrice 4 x 4
% B(:,:,2,k): y-coordonnes des points de controle du patch k comme matrice 4 x 4
% B(:,:,3,k): z-coordonnes des points de controle du patch k comme matrice 4 x 4

% ------------------------------------
% num_p+1 valeurs de parametres uniformes: 0,1,2,...,num_p en u et v
u = linspace(0,1,num_p); 
v = u; 

%  ------------------------------------
% Cubic Bezier patches 
for k=1:np
    S(:,:,:,k)=bezierPatchEval(B(:,:,:,k),u,v); %evaluation du patch k en (num_p+1) x (num_p+1) points
end


% % ------------------------------------
% % Normal vectors of Cubic Bezier patches 
nu=linspace(0,1,num_n); nv=nu;  %parametrisation uniforme (num_n+1)x (num_n+1) valeurs de parametre
for k=1:np
  N(:,:,:,k)=bezierPatchNormal(B(:,:,:,k),nu,nv); %vecteurs normal du patch 
end



% ------------------------------------
% Computing Isophotes
L  = [0 1 0];
L = L/norm(L);
c = 0.1;
epsilon = 0.05;
for k =1:np
    I(:, :, k) =bezierIsophote(N(:,:,:,k), S(:,:,:,k), L, c, epsilon, u,  v);
end



% ------------------------------------
% Computing courbure

Courbure =[]
for k =1:np
    Courbure(:, :, k) =bezierCourbure(N(:,:,:,k), B(:,:,:,k), u,  v);
end

% ------------------------------------
% Visualisation d'un patch/surface de Bezier
%plotBezierPatch3D(B(:,:,:,2),S(:,:,:,2)) % plot d'un seul patch k
%quiver3(S(:,:,1,1), S(:,:,2,1), S(:,:,3,1), N(:,:,1,1), N(:,:,2,1), N(:,:,3,1))
plotBezierSurface3D(B,S, N,I)		   % plot de tous les np patches