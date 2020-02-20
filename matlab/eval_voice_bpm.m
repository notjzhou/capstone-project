function eval_voice_bpm(file)
%     file = 'output.wav';
%     file = 'Samples/looperman-a-1540447-0013592-swalla2.wav';
%     file = 'Samples/Stronger1wav.wav';
    peaks = voice_tempo(file);
    beat_bpm = beat_detection;
    bps = beat_bpm / 60;
    fs = 44100;
    dt = 1/fs;
    t = 0:dt:(length(peaks)*dt)-dt;
%     hits_per_sec = 1:fs/bps:fs*32;
%     cnt = 1;
    % beat_dur is duration between each beat in number of samples
    % if bpm = 120 and fs = 44100, then bps = 2 and beat_dur = 22050
    beat_dur = round(fs / bps);
    beat_hit = false;
    missed_beats = zeros(1, length(t));
    hit_beats = zeros(1, length(t));
    cnt = 0;
    for n = 1:beat_dur:length(peaks)
        for lambda = -round(beat_dur*0.08):round(beat_dur*0.08)
%             disp(n+lambda)
            if 0 < n+lambda && n+lambda < length(peaks)...
                    && peaks(n+lambda) > 0
                beat_hit = true;
                break
            end
        end
        if beat_hit == false
            missed_beats(n) = 4;
            fprintf('Missed: %d (%f s)\n', n, n/fs);
        else
            fprintf('Hit:    %d (%f s)\n', n , n/fs);
            hit_beats(n) = 4;
            cnt = cnt + 1;
        end
        beat_hit = false;
    end
    plot(t, missed_beats, 'color', 'red', 'LineWidth', 2);
    plot(t, hit_beats, 'color', 'green', 'LineWidth', 2);
    hold off;
    if cnt > 4
        disp('On beat');
    end
end