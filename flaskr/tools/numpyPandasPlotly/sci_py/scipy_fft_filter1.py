import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq
# Generate a 1 kHz sine wave with noise
fs = 10_000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
signal =  0.2*np.sin(2 * np.pi * 1000 * t) + 0.7*np.random.normal(0, 1, len(t)) + \
          0.1*np.sin(2 * np.pi * 900 * t) + 0.1*np.sin(2 * np.pi * 1100 * t)

# Compute the FFT of the signal
fft_result = fft(signal)
freq = fftfreq(len(t), d=1/fs)

# Design a bandpass filter
filter_wide = 110
max_signal_freq = np.abs(freq[np.argmax(np.abs(fft_result))])
lowcut, highcut = max_signal_freq-filter_wide, max_signal_freq+filter_wide  # Frequency range (Hz)
sig_rfft_filtered = fft_result.copy()
sig_rfft_filtered[(freq < lowcut) | (freq > highcut)] = 0
sig_lfft_filtered = fft_result.copy()
sig_lfft_filtered[(freq > -lowcut) | (freq < -highcut)] = 0
sig_fft_filtered = sig_rfft_filtered + sig_lfft_filtered

# get the filtered signal in time domain
filtered_signal = ifft(sig_fft_filtered)

# Plot the original signal, FFT, and filtered signal
plt.figure(figsize=(10, 7))
plt.subplot(6, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(6, 1, 2)
plt.plot(freq, np.abs(fft_result), label='FFT original')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
# plt.ylim(0, 1000)
plt.xlim(0, 2000)
plt.legend()

plt.subplot(6, 1, 3)
plt.plot(t, filtered_signal, label='Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(6, 1, 4)
plt.plot(freq, np.abs(sig_fft_filtered), label=f'FFT filtered wide {filter_wide}hz')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
# plt.ylim(0, 1000)
plt.xlim(0, 2000)
plt.legend()

threshold = 300
sig_fft_filtered_clear = np.where(np.abs(sig_fft_filtered) < threshold, 0, sig_fft_filtered)
sig_filtered_clean = ifft(sig_fft_filtered_clear)

plt.subplot(6, 1, 5)
plt.plot(t, sig_filtered_clean, label='clean signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
# plt.ylim(0, 1000)
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(6, 1, 6)
plt.plot(freq, np.abs(sig_fft_filtered_clear), label=f'FFT clean under {threshold}')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
# plt.ylim(0, 1000)
plt.xlim(0, 2000)
plt.legend()

plt.tight_layout()
plt.show()
