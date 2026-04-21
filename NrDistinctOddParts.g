# Код для GAP System

NrDistinctOddPartsByK := function(n, k)
	local p, i, j, limit;
	
    p := List([1..n], _ -> List([1..k], _ -> 0));
    p[1][1] := 1;
	
    for i in [1..n] do
        limit := Minimum(k, i);
        for j in [1..limit] do
            if i > 2*j then
                p[i][j] := p[i][j] + p[i-2*j][j];
            fi;
            if i > 2*j-1 and j > 1 then
                p[i][j] := p[i][j] + p[i-(2*j-1)][j-1];
            fi;
        od;
    od;
    return p[n][k];
end;;

NrRestrictPartsByK := function(n, k)
    local p, m, i;
    
    p := ListWithIdenticalEntries(n + 1, 0);
    p[1] := 1;
    
    for m in [1..k] do
        for i in [m + 1..n + 1] do
            p[i] := p[i] + p[i - m];
        od;
    od;
    
    return p[n + 1];
end;;

NrDistinctOddParts := function(n)
	local i, result, kbound;
	
	result := 0;
	kbound := RootInt(n);
	for i in [1..kbound] do
		if IsEvenInt(n - i) then
			result := result + NrDistinctOddPartsByK(n, i);
		fi;
	od;
	
	return result;
end;;

NrRestrictParts := function(n)
	local i, result, kbound;
	
	result := 0;
	kbound := RootInt(n);
	for i in [1..kbound] do
		if IsEvenInt(n - i) then
			result := result + NrRestrictPartsByK((n - i * i) / 2, i);
		fi;
	od;
	
	return result;
end;;

NrMod4Parts := function(n)
	local i, num, eq, result;
	
	result := 0;
	eq := n mod 4;
	num := RootInt(n);
	
	for i in [1..num] do
		if eq = (i mod 4) then
			result := result + NrDistinctOddPartsByK(n, i);
		fi;
	od;
	
	return result;
end;;

NrMod4Parts2 := function(n)
	local i, num, eq, result;
	
	result := 0;
	eq := n mod 4;
	num := RootInt(n);
	
	for i in [1..num] do
		if eq = (i mod 4) then
			result := result + NrRestrictPartsByK((n - i * i) / 2, i);
		fi;
	od;
	
	return result;
end;;

NrMod4Parts(999);
NrMod4Parts2(999);
NrDistinctOddParts(1000);
NrRestrictParts(1000);
