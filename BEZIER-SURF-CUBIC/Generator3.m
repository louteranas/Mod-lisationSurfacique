close all, clear all


fileID = fopen('surface4', 'w');
formatSpec = '%e \t%e \t%e \n';
xC = 3;
yC = 4;
zC = 5;
for k=0:3
    for i=0:3
       fprintf(fileID,formatSpec,xC + i, yC , zC + k);
    end
end

for k=0:3
    for i=0:3
       fprintf(fileID,formatSpec,xC , yC + i, zC +k);
    end
end

for k=0:3
    for i=0:3
        fprintf(fileID,formatSpec,xC + 3, yC + i, zC +k);
    end
end

for k=0:3
    for i=0:3
       fprintf(fileID,formatSpec,xC + i, yC+3, zC + k);
    end
end