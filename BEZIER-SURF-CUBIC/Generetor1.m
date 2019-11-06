close all, clear all


fileID = fopen('surface2', 'w');
formatSpec = '%e \t%e \t%e \n';
xC = 3;
yC = 4;
zC = 5;
for k=0:3
    yC = yC + 1;
    for i=0:3
        if yC == 6 
            fprintf(fileID,formatSpec,xC + i, yC, zC - 4);
        else
            fprintf(fileID,formatSpec,xC + i, yC, zC); 
        end      
    end
end
yC = yC - 1;
for k=0:3
    yC = yC + 1;
    for i=0:3
        if yC == 10 
            fprintf(fileID,formatSpec,xC + i, yC, zC +4);
        else
            fprintf(fileID,formatSpec,xC + i, yC, zC); 
        end      
    end
end

fclose(fileID);