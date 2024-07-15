"""
# 1. 음성 파일 읽기 
# 2. 음성 파일 자르기 
# 3. 파일 지연
4. 노이즈 추가
5. 사운드 재생
6. 그래프 출력
7. 그래프의 자기 상관 함수
8. 그래프 출력
9. 사운드 재생
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import welch, correlate
import random
import librosa

file_path = "C:\\Users\\KDP-2\\OneDrive\\바탕 화면\\EX_PY06\\Project\\Shine.wav"
save_path = "C:\\Users\\KDP-2\\OneDrive\\바탕 화면\\EX_PY06\\Project\\"
sr = 4000

def read_data(path, sr = sr):
    data, samplerate = librosa.load(path, sr = sr)
    if len(data.shape) == 2:
        data = data[:, 0]

    return samplerate, data


def cut_audio_data(file, save_path, start_time = 60, sec = 10):
    sample_data, samplerate = librosa.load(file, sr = sr)
    cut_data = sample_data[start_time * samplerate : (sec + start_time) * samplerate]
    wavfile.write(save_path + "cut_file.wav", samplerate, cut_data)
    print(f"Samplerate is {samplerate}")
# 파일 잘리는지 체크


def draw_wave(x, y):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y)  # 절반만 표시 (대칭성 때문에)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.title('Spectrum of the Audio Signal')
    plt.grid()
    plt.show()

def delay(data, samplerate):
    step = 0.001
    delay_time = (2 + 2 * random.random()) * samplerate
    delayed_data = np.roll(data, round(delay_time/step))
    wavfile.write(save_path + "delayed_file.wav", samplerate, delayed_data)

    return delayed_data

def add_noise(data):
    noise = np.random.normal(0, 100, len(data))
    noised_data = np.array(data) + noise
    wavfile.write(save_path + "delayed+noised_file.wav", samplerate, noised_data.astype(np.int16))
    return noised_data

def translate(data, samplerate):
    fft_result = np.fft.fft(data)
    frequency = np.fft.fftfreq(len(data), 1 / samplerate)
    magnitude = np.abs(fft_result)

    return frequency, magnitude

def spectrum_return(data, samplerate):
    f, psd = welch(data, samplerate, nperseg=1024)
    return f, psd

def autocorrelation(data):
    result = np.correlate(data, data, mode = 'full')
    return result[result.size // 2:]

def calculate_power(data):
    power = np.mean(data**2)
    return power



if __name__ == "__main__":
    cut_audio_data(file_path, save_path)
    samplerate, original_data = read_data(save_path + "cut_file.wav")
    
    # 원본 신호의 자기상관
    original_autocorr = autocorrelation(original_data)
    draw_wave(np.arange(len(original_autocorr))/samplerate, original_autocorr)
    
    # 지연된 신호
    delayed_data = delay(original_data, samplerate)
    delayed_autocorr = autocorrelation(delayed_data)
    draw_wave(np.arange(len(delayed_autocorr))/samplerate, delayed_autocorr)

    # 노이즈가 추가된 신호
    noised_data = add_noise(delayed_data)
    noised_autocorr = autocorrelation(noised_data)
    draw_wave(np.arange(len(noised_autocorr))/samplerate, noised_autocorr)
    
    # 스펙트럼 분석
    f, psd = spectrum_return(noised_data, samplerate)
    draw_wave(f, psd)

    # 원본과 노이즈가 추가된 신호의 교차상관
    cross_corr = np.correlate(original_data, noised_data, mode='full')
    draw_wave(np.arange(len(cross_corr))/samplerate - len(original_data)/samplerate, cross_corr)