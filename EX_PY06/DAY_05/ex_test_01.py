"""
[실습1] 글자를 입력 받습니다
        입력 받은 글자(숫자 제외)를 코드 값을 출력
        합니다.
"""

alphabet = input("글자 입력 (a ~ z, A ~ Z) : ")
if len(alphabet) == 1 and ('a' <= alphabet <= 'z' or 'A' <= alphabet <= 'Z'):
    print(F"{alphabet}의 코드값 : {ord(alphabet)}")

else :
    print("1개의 알파벳 문자만 입력해야 합니다.\n입력된 데이터 확인하세요.")
# 문자 ==> 코드값 변환 내장 함수 : ord (문자 1개)


# 두개 이상의 문자를 받았을 때,
# data = "AB"
# data = list(map(ord, data))
# print(data)


"""
[실습2] 점수를 입력 받은 후 학점을 출력합니다.
- 학점 : A+, A, A-, B+, B, B-, C+, C, C-,
        D+, D, D-, F
"""

score = int(input("점수를 입력하세요 : "))
grade = ""

if score < 0 or score > 100:
    print(F"{score}은 잘못 입력된 점수 입니다.")

if score > 95: grade = "A+"
elif score == 95: grade = "A"
elif score >= 90: grade = "A-"
elif score > 85: grade = "B+"
elif score == 85: grade = "B"
elif score >= 80: grade = "B-"
elif score > 75: grade = "C+"
elif score == 75: grade = "C"
elif score >= 70: grade = "C-"
elif score > 65: grade = "D+"
elif score == 65: grade = "D"
elif score >= 60: grade = "D-"
else: grade = "F"

print(f"{score} 점의 성적은 {grade}입니다.")



# if score > 100 or score < 0:
#     print(F"{score}점은 잘못된 입력입니다.")

# elif score >= 96:
#     print(F"{score}점의 성적은 A+입니다.")

# elif score >= 95:
#     print(F"{score}점의 성적은 A입니다.")

# elif score >= 90:
#     print(F"{score}점의 성적은 A-입니다.")

# elif score >= 86:
#     print(F"{score}점의 성적은 B+입니다.")

# elif score >= 85:
#     print(F"{score}점의 성적은 B입니다.")

# elif score >= 80:
#     print(F"{score}점의 성적은 B-입니다.")

# elif score >= 76:
#     print(F"{score}점의 성적은 C+입니다.")

# elif score >= 75:
#     print(F"{score}점의 성적은 C입니다.")

# elif score >= 70:
#     print(F"{score}점의 성적은 C-입니다.")

# elif score >= 66:
#     print(F"{score}점의 성적은 D+입니다.")

# elif score >= 65:
#     print(F"{score}점의 성적은 D입니다.")

# elif score >= 60:
#     print(F"{score}점의 성적은 D-입니다.")

# else:
#     print(F"{score}점의 성적은 F입니다.")