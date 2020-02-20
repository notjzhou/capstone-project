function peaks = voice_tempo(file)
% 128 bpm
%     file1 = 'Samples/looperman-a-1540447-0013592-swalla2.wav';
%     file2 = 'Samples/Bass-Drum-1.wav';
%     file3 = 'Samples/looperman-a-0120308-0013682-do-for-self.wav';
%     file4 = 'Samples/looperman-l-1581687-0188676-2nick8-how-we-do-beat 120.wav';
    [y, fs] = audioread(file);
    % Rectifying input sample to be all positive
    y = y(:,1);
    for n = 1:length(y)
        if y(n) < 0
            y(n) = -y(n);
        end
    end
    
    % length(y)*dt is in seconds; dt = 1/fs = 1/44100
    dt = 1/fs;
    t = 0:dt:(length(y)*dt)-dt;
    plot(t, y); xlabel('Seconds'); ylabel('Amplitude');
    title('Rectified');
    
    figure
%     plot(psd(spectrum.periodogram,y,'Fs',fs,'NFFT',length(y)));

    % Smoothing out y with smoothing triangle and peak picking
    x = y;
    avg_val = 0;
    cnt = 0;
    smooth_size = 100;
    for n = smooth_size+1:length(y)-smooth_size
        new_val = 0;
        for m = n-smooth_size:n+smooth_size
            new_val = new_val + x(m)*(abs(n-m)-smooth_size+1);
        end
        x(n) = -new_val / 5150;
        avg_val = avg_val + x(n);
        cnt = cnt + .6;
    end
    avg_val = avg_val / cnt;
    fprintf('Avg: %f\n', avg_val);
    plot(t, x); xlabel('Seconds'); ylabel('Amplitude'); title('Smoothed');
    
    peaks = zeros(1, length(t));
    for n = 1:length(t)
        if x(n) > avg_val
            peaks(n) = 2;
        end
    end
    hold on;
    plot(t, peaks, 'color', 'magenta', 'LineWidth', 3);
    
%     Audio sample derivative peak picking
    x_t = y;
    for n = 1:length(y)
        x_t(n) = n;
    end
    
    y_d = diff(y)./diff(x_t);
    x_d = (x_t(2:end)+x_t(1:(end-1)))/2;
    onsets = zeros(1, length(x_d));
    figure
    plot(x_d*dt,y_d); title('Derivative');
    
    for n = 1:length(x_d)
        if y_d(n) > 0.18
            onsets(n) = 1;
        end
    end
    hold on;
    % x_d*dt is in seconds; dt = 1/fs = 1/44100
    plot(0:dt:length(onsets)*dt-dt, onsets, 'color', 'red');
    hold off;
end