
# [실습] 숫자를 입력 받아서 음이 아닌 정수와 음수 구분하기


num = int(input("숫자를 입력하시오 : "))

if num >= 0:
    print(f"숫자 {num}은 음이 아닌 정수 입니다.")
else:
    print(f"숫자 {num}은 음수 입니다.")

# [실습] 점수를 입력 받아서 합격과 불합격 출력
# - 합격 : 60점 이상

score = int(input("점수를 입력하시오. : "))
if score >= 60:
    print(F"점수 {score}점으로 합격입니다.")
else:
    print(F"점수 {score}점으로 불합격입니다.")

# [실습] 점수를 입력 받아서 학점 출력
# - 학점 : A, B, C, D, F

score2 = int(input("점수를 입력하시오. : "))
if score2 >= 90:
    print(F"점수 {score2}점으로 A입니다.")

elif score2 >= 80:
    print(F"점수 {score2}점으로 B입니다.")

elif score2 >= 70:
    print(F"점수 {score2}점으로 C입니다.")

elif score2 >= 60:
    print(F"점수 {score2}점으로 D입니다.")

else:
    print(F"점수 {score2}점으로 F입니다.")
