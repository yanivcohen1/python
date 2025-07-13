import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

# Generate a 1 kHz sine wave with noise
fs = 10_000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
signal =  0.2*np.sin(2 * np.pi * 1000 * t) + 0.7*np.random.normal(0, 1, len(t)) + \
          0.1*np.sin(2 * np.pi * 900 * t) + 0.1*np.sin(2 * np.pi * 1100 * t)

# Compute the FFT of the signal
fft_result = np.fft.rfft(signal)
freq = np.fft.rfftfreq(len(t), d=1/fs)

max_signal_freq = freq[np.argmax(np.abs(fft_result))]
# Design a bandpass filter
band_wide = 150 # in hz
lowcut, highcut = max_signal_freq-band_wide, max_signal_freq+band_wide  # Frequency range (Hz)
order = 4  # Filter order
nyq = 0.5 * fs
low = lowcut / nyq
high = highcut / nyq
b, a = butter(order, [low, high], btype='band')

# Apply the filter
filtered_signal = lfilter(b, a, signal)

# Plot the original signal, FFT, and filtered signal
plt.figure(figsize=(10, 6))
plt.subplot(4, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(freq, np.abs(fft_result), label='rFFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 1000)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(t, filtered_signal, label='Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

# Compute the FFT of the signal
fft_result2 = np.fft.fft(filtered_signal)

plt.subplot(4, 1, 4)
plt.plot(freq, np.abs(fft_result2[0:len(freq)]), label=f'FFT filtered wide {band_wide} hz')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 1000)
plt.legend()

plt.tight_layout()
plt.show()
