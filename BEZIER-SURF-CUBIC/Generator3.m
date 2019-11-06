close all, clear all


fileID = fopen('surface4', 'w');
formatSpec = '%e \t%e \t%e \n';
xC = 3;
yC = 4;
zC = 5;
for k=0:3
    for i=0:3
       %if i == 1 && k == 1
       %   fprintf(fileID,formatSpec,xC + i, yC +1 , zC + k); 
       %end
       if i == 2 && k == 2
          fprintf(fileID,formatSpec,xC + i, yC-10 , zC + k);
       else
          fprintf(fileID,formatSpec,xC + i, yC , zC + k);
       end
    end
end
