def mac(pattern, filter_data):
    score = 0

    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score += pattern[row][col] * filter_data[row][col]

    return score

def input_matrix(name):
    # 3×3 행렬을 한 줄씩 입력받는 함수
    print(f"{name}을 3줄 입력하세요. (숫자를 공백으로 구분)")

    matrix = []

    # 정상적인 행이 3개 모일 때까지 계속 입력받음
    while len(matrix) < 3:

        # 입력값의 앞뒤 공백 제거
        raw = input().strip()

        # 아무것도 입력하지 않고 Enter만 누른 경우
        if raw == "":
            print("입력 오류: 아무것도 입력되지 않았습니다.")
            continue

        # 공백을 기준으로 숫자 3개를 나눔
        row = raw.split()

        # 숫자 개수가 정확히 3개인지 확인
        if len(row) != 3:
            print("입력 형식 오류: 각 줄에 3개의 숫자를 입력하세요.")
            continue

        try:
            # 입력된 글자를 계산 가능한 실수(float)로 변환
            row = [float(value) for value in row]

        except ValueError:
            # abc 같은 문자가 들어온 경우
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue

        # 0과 1 이외의 숫자가 있는지 확인
        valid = True

        for value in row:
            if value != 0.0 and value != 1.0:
                valid = False

        # 0 또는 1이 아닌 값이 있으면 다시 입력
        if valid == False:
            print("입력 오류: 0 또는 1만 입력하세요.")
            continue

        # 정상적인 한 행을 matrix에 저장
        matrix.append(row)

    # 완성된 3×3 행렬을 함수 밖으로 전달
    return matrix
    

cross_filter = input_matrix("Cross 필터")
x_filter = input_matrix("X 필터")
pattern = input_matrix("패턴")

cross_score = mac(pattern, cross_filter)
x_score = mac(pattern, x_filter)

epsilon = 1e-9

if abs(cross_score - x_score) < epsilon:
    result = "UNDECIDED"
elif cross_score > x_score:
    result = "Cross"
else:
    result = "X"

print("Cross 점수:", cross_score)
print("X점수:", x_score)
print("판정:", result)