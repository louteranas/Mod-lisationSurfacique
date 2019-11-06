             
function I = bezierIsophote(N, S, L, c, epsilon, u, v)

I=[];
counter = 1;
for i = 1:length(u)
    for j = 1:length(v)
        % on evalue l'expression
        Nij = [N(i, j, 1) N(i, j, 2) N(i, j, 3)];
        Nij = Nij/norm(Nij);
        if abs(dot(Nij, L) - c) < epsilon 
            disp('coucou');
            I(counter, :) = S(i, j, :);
            counter = counter + 1;
        end
    end    
end
end
    