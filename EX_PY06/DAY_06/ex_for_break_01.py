"""
제어문 - 반복문 중단 break
- 반복을 중단 시키는 조건문과 함께 사용 됨
"""

# [실습] 숫자 데이터의 합계가 30 이상이 되면 더 이상 합계를 하지 마세요.
# 숫자 데이터는 1 ~ 50으로 구성됨

nums = list(range(1, 51))
total = 0

for num in nums:
    total += num
    if total >= 30:
        break

print(f"total => {total} {1} ~ {num - 1} 까지의 합계")

# [실습] 4개 과목 점수가 있습니다.
#        과목 점수가 1과목이라도 40 미만이면 불합격입니다.
#        4개 과목 평균이 60점 이상이면 합격입니다.

score = [89, 39, 80, 77]
isPass = True

#과목별 40 미만 체크
for jumsu in score:
    if jumsu < 40:
        print("당신은 과락입니다.")
        isPass = False
        break
    print("모든 과목이 40점 이상입니다.")

if isPass:
    avg = sum(score) / len(score)
    if avg >= 60:
        print(F"당신은 {avg}점으로 합격입니다.")
    else:
        print(F"당신은 {avg}점으로 불합격입니다.")
else:
    print(F"당신은 40점 미만인 과목으로 불합격입니다.")