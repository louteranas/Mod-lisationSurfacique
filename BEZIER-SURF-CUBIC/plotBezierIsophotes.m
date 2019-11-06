%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% plot d'une surface de Bezier composee de np patches
%
% Un patch de Bezier bicubique est defini par 16 points de controle de R^3
% stockes dans une matrice 4 x 4 x 3
%
% Input:
%  - Matrice B avec les 16 points de controle d'un patch de Bezier bicubique.
%    Un point de controle a 3 coordonnees (x,y,z)
%    La taille de B est 4 x 4 x 3 
%      B(:,:,k) : matrice 4x4 de points de controle de la keme dimension, k=1,2,3 
%      B(:,:,1): matrice 4x4 de x-coordonnes des points de controle 
%      B(:,:,2): matrice 4x4 de y-coordonnes des points de controle 
%      B(:,:,3): matrice 4x4 de z-coordonnes des points de controle
%      B(i,j,:): 3 coordonnes du point de controle Bij
%  - Matrice S : points calcules sur la surface
%    La structure de S est similaire a celle de B.
%
% Visualisations proposees
%  - reseau de controle
%  - wireframe
%  - smooth shading with color
%  - smooth shading with wires
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function plotBezierSurface3D(B,S, I, I2 ,I3, I4, I5, I6, I7, I8, I9)

[~, ~, ~, npl]=size(B);
[n,  ~]  = size(I);
% % np: number of patches

str1='\bf Control Point';
str2='\bf Control Polygon';
str3='\bf Surface (bi-directional Bezier curve)';


% %----------------------------------------------- 
% % Surface avec interpolated shading
figure, hold on
axis equal;
np = 1;
for k=1:np
    surface(S(:,:,1,k),S(:,:,2,k),S(:,:,3,k))
    if size(I(:,:, k)) ~= 0
        plot3(I(:,1, k), I(:,2,k), I(:,3,k),'Color','[0 0.4470 0.7410]');
    end
    if size(I2(:,:, k)) ~= 0
        plot3(I2(:,1, k), I2(:,2,k), I2(:,3,k),'Color','[0.8500 0.3250 0.0980]');
    end
    if size(I3(:,:, k)) ~= 0
        plot3(I3(:,1, k), I3(:,2,k), I3(:,3,k),'Color','[0.9290 0.6940 0.1250]');
    end
    if size(I4(:,:, k)) ~= 0
        plot3(I4(:,1, k), I4(:,2,k), I4(:,3,k),'Color','[0.4940 0.1840 0.5560]');
    end
    if size(I5(:,:, k)) ~= 0
        plot3(I5(:,1, k), I5(:,2,k), I5(:,3,k),'Color','[0.4660 0.6740 0.1880]');
    end
    if size(I6(:,:, k)) ~= 0
        plot3(I6(:,1, k), I6(:,2,k), I6(:,3,k),'Color','[0.3010 0.7450 0.9330]');
    end
    if size(I7(:,:, k)) ~= 0
        plot3(I7(:,1, k), I7(:,2,k), I7(:,3,k),'Color','[0.6350 0.0780 0.1840]');
    end
    if size(I8(:,:, k)) ~= 0
        plot3(I8(:,1, k), I8(:,2,k), I8(:,3,k),'Color','[0.8500 0.3250 0.0980]');
    end
    if size(I9(:,:, k)) ~= 0
        plot3(I9(:,1, k), I9(:,2,k), I9(:,3,k),'Color','[0.8500 0.3250 0.0980]');
    end
end
shading interp
title('\bf Isophotes lines for c values ranging from 0.05 to 0.5 with 0.05 step');
view(3); box;  view(21,19)
