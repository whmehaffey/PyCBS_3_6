for i=1:length(bad)    
    delete(bad{i});
    delete([bad{i}(1:end-5) '.tmp'])
   delete([bad{i}(1:end-5) '.rec'])
end;

