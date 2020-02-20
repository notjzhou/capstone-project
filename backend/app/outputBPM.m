function test_out = outputBPM(test_array)
    test_out = 0;
    for val = 1:length(test_array)
        test_out = test_out + test_array(val);
    end
    test_out = test_out / length(test_array);
end