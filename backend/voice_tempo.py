import numpy as np
import scipy.io.wavfile
import matplotlib
import math
import time

def eval_voice_bpm(file, bpm):
    # file = 'output.wav'
    # file = 'Samples/looperman-a-1540447-0013592-swalla2.wav'
    # file = 'Samples/Stronger1wav.wav'

    peaks = voice_tempo(file)
    # beat_bpm = 128
    bps = bpm / 60
    fs = 44100
    dt = 1/fs
    max_t = (len(peaks)*dt)-dt
    t = np.arange(0, max_t, dt)
    hits_per_sec = np.arange(0, fs*32, fs/bps)
    cnt = 1

    # beat_dur is duration between each beat in number of samples
    # if bpm = 120 and fs = 44100, then bps = 2 and beat_dur = 22050
    beat_dur = round(fs / bps)
    beat_hit = False
    missed_beats = np.zeros(len(t))
    hit_beats = np.zeros(len(t))
    bt_hits = 0
    bt_misses = 0
    cnt_pause = 0

    for n in range(0, len(peaks), beat_dur):
        for d in range(-round(beat_dur*0.08), round(beat_dur*0.08)):
            if ((0 < n+d) and (n+d < len(peaks) and peaks[n+d] > 0)):
                beat_hit = True
                break
        if beat_hit == False:
            cnt_pause += 1
            if (cnt_pause > 3):
                missed_beats[n-1] = 0
                missed_beats[n-2] = 0
            else:
                missed_beats[n] = 4
                bt_misses += 1
        else:
            hit_beats[n] = 4
            bt_hits += 1
        beat_hit = False

    # plot(t, missed_beats, 'color', 'red', 'LineWidth', 2)
    # plot(t, hit_beats, 'color', 'green', 'LineWidth', 2)
    # hold off

    acc = bt_hits / (bt_hits + bt_misses)
    print("Accuracy: " + str(acc * 100) + "%")
    return acc

def voice_tempo(file):
    # 128 bpm
    # file1 = 'Samples/looperman-a-1540447-0013592-swalla2.wav'
    # file2 = 'Samples/Bass-Drum-1.wav'
    # file3 = 'Samples/looperman-a-0120308-0013682-do-for-self.wav'
    # file4 = 'Samples/looperman-l-1581687-0188676-2nick8-how-we-do-beat 120.wav'
    fs, data = scipy.io.wavfile.read(file)
    # Rectifying

    # data = data[:,0]
    y = np.full_like(data, 0);
    for n in np.arange(len(y)):
        if data[n] < 0:
            y[n] = -y[n]
        else:
            y[n] = data[n]

    # length(y)*dt is in seconds; dt = 1/fs = 1/44100
    dt = 1/fs
    t = np.arange(0, (len(y)*dt)-dt, dt)
    print("len(t)")
    print(len(t));

    start = time.time()

    # Smoothing out y with smoothing triangle and peak picking
    x = y
    avg_val = 0
    cnt = 0
    smooth_size = 3
    for n in range(smooth_size+1, len(y)-smooth_size):
        new_val = 0
        for m in range(n-smooth_size, n+smooth_size):
            new_val = new_val + x[m]*(abs(n-m)-smooth_size+1)
        x[n] = -new_val / 9
        avg_val = avg_val + x[n]
        cnt = cnt + .6

    avg_val = avg_val / cnt
    print("Avg: " + str(avg_val))
    end = time.time()
    print("Time: " + str(end - start) + " s")

    peaks = np.zeros(len(t))
    print("len(peaks): " + str(len(peaks)));
    for n in range(1, len(t)):
        if x[n] > avg_val:
            peaks[n] = 2;

    return peaks


