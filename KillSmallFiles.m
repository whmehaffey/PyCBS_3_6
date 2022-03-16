temp=dir('*.rec');
cutoff=6284000

for i=1:length(temp);

    a=dir(temp(i).name(1:end-4))
    if a.bytes < cutoff
        delete(temp(i).name(1:end-4));
        delete(temp(i).name);
    end;
    
end;
