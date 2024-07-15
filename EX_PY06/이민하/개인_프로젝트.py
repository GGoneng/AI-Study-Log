"""
# 1. 음성 파일 읽기 
# 2. 음성 파일 자르기 
# 3. 파일 지연
# 4. 노이즈 추가
# 5. 사운드 재생
# 6. 그래프 출력
7. 그래프의 자기 상관 함수
8. 그래프 출력
9. 사운드 재생
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import random
import librosa

file_path = "C:\\Users\\KDP-2\\OneDrive\\바탕 화면\\EX_PY06\\이민하\\sample.wav"
save_path = "C:\\Users\\KDP-2\\OneDrive\\바탕 화면\\EX_PY06\\이민하\\"

def read_data(path):
    data, samplerate = librosa.load(path)
    if len(data.shape) == 2:
        data = data[:, 0]

    return samplerate, data


def cut_audio_data(file, save_path, start_time = 5, sec = 10):
    sample_data, samplerate = librosa.load(file)
    cut_data = sample_data[start_time * samplerate : (sec + start_time) * samplerate]
    wavfile.write(save_path + "cut_file.wav", samplerate, cut_data)
    print(f"Samplerate is {samplerate}")
# 파일 잘리는지 체크


def draw_wave(data):
    plt.subplot(2, 1, 1)
    plt.plot(data)
    plt.xlabel("time(sec) * samplerate (samplerate = 44100)")
    plt.ylabel("amplitude (Hz)")

    plt.subplot(2, 1, 2)
    plt.plot(data)
    plt.xlim(-500, 10000)
    plt.xlabel("time(sec) * samplerate (samplerate = 44100)")
    plt.ylabel("amplitude (Hz)")
    plt.show()


# def autocorrelation(data, original_data):
#     bt = data # 복소수 배열
#     pt = original_data
#     t_step = 0.001
#     tau = np.arange(0, 10 * samplerate, t_step)
#     result = []

#     for t in tau:
#         shift_samples = np.round(t / t_step).astype(int)
#         data_tau = np.roll(bt, -shift_samples)
#         rn_tau = np.sum(bt.conjugate() * data_tau) * t_step
#         result.append(rn_tau)
#     result = np.array(result)
#     print(result,len(result))
#     result_int16 = np.int16(result / np.max(np.abs(result)) * 32767)
#     wavfile.write(save_path + "result.wav", samplerate, result_int16)
#     return result

# # 예시 데이터
#     bt = data # 복소수 배열
#     pt = original_data
#     t_step = 0.1  # 시간 간격

# # tau 값 범위 설정
#     tau_values = np.arange(0, 10 * sr, t_step)

# # 각 tau 값에 대해 shift_samples 계산
#     shift_samples = np.round(tau_values / t_step).astype(int)

# # 모든 nt_tau 계산
#   # nt 배열을 tau_values 길이만큼 복사
#     bt_tau_matrix = np.zeros((len(tau_values), len(bt)), dtype=bt.dtype)
#     for i, shift in enumerate(shift_samples):
#         bt_tau_matrix[i] = np.roll(bt, -shift)
# # 모든 rn_tau 계산
#     rpb_matrix = np.conj(pt) * bt_tau_matrix
#     rpb_vector = np.sum(rpb_matrix) * t_step
#     wavfile.write(save_path + "result.wav", samplerate, rpb_vector.astype(np.int16))
#     print(rpb_vector)

#     return rpb_vector
    
def delay(data, samplerate):
    step = 0.001
    delay_time = (2 + 2 * random.random()) * samplerate
    delayed_data = np.roll(data, round(delay_time/step))
    wavfile.write(save_path + "delayed_file.wav", samplerate, delayed_data)

    return delayed_data

def add_noise(data):
    noise = np.random.normal(0, 1, len(data))
    noised_data = np.array(data) + noise
    wavfile.write(save_path + "delayed+noised_file.wav", samplerate, noised_data.astype(np.int16))
    return noised_data


if __name__ == "__main__":
    cut_audio_data(file_path, save_path)
    samplerate, original_data = read_data(save_path + "cut_file.wav")
    print(original_data, original_data.shape)
    draw_wave(original_data)
    
    delay(original_data, samplerate)
    samplerate, data = read_data(save_path + "delayed_file.wav")
    print(data)
    draw_wave(data)
    
    add_noise(data)
    samplerate, data = read_data(save_path + "delayed+noised_file.wav")
    print(data)
    draw_wave(data)
