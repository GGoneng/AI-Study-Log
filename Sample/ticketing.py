import pyautogui
import time
import keyboard

click_x = 800
click_y = 600

running = False  # 실행 여부 상태 변수

print("▶ 's' 키로 시작/중지, 'q' 키로 종료합니다.")

while True:
    if keyboard.is_pressed('q'):
        print("⏹ 종료합니다.")
        break

    # 실행 토글
    if keyboard.is_pressed('s'):
        running = not running
        print("▶ 실행 중..." if running else "⏸ 일시정지")
        time.sleep(0.5)  # 키 입력 중복 방지

    if running:

        time.sleep(1)

        # 클릭
        pyautogui.moveTo(click_x, click_y)
        pyautogui.click()
        pyautogui.press('enter')
        print("[작동] 클릭 완료")

        # 반복 주기 조절
        time.sleep(0.5)  # 매 3초마다 동작
        

