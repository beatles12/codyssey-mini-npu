import time

# ==========================================================
# [0] 설정값
# ==========================================================
EPSILON = 1e-9      # 두 점수 차이가 이보다 작으면 동점으로 본다
REPEAT = 10         # 성능 측정 반복 횟수


# ==========================================================
# [1] MAC 연산
# ==========================================================
def mac(pattern, filter_data):
    score = 0.0
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score += pattern[row][col] * filter_data[row][col]
    return score


# ==========================================================
# [2] 판정 (epsilon 동점 처리)
# ==========================================================
def decide(score_a, score_b, label_a, label_b, tie_text):
    if abs(score_a - score_b) < EPSILON:
        return tie_text
    elif score_a > score_b:
        return label_a
    else:
        return label_b


# ==========================================================
# [3] 사용자 입력 (3x3)
# ==========================================================
def input_matrix(name, size):
    print(f"{name} ({size}줄 입력, 공백 구분)")
    matrix = []
    while len(matrix) < size:
        raw = input().strip()
        if raw == "":
            print("입력 오류: 아무것도 입력되지 않았습니다.")
            continue
        row = raw.split()
        if len(row) != size:
            print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
            continue
        try:
            row = [float(value) for value in row]
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue
        matrix.append(row)
    print(f"✓ {name} 저장 완료 ({size}x{size})")
    return matrix


# ==========================================================
# [4] 성능 측정
# ==========================================================
def measure(pattern, filter_data):
    total_time = 0.0
    for i in range(REPEAT):
        start = time.perf_counter()
        mac(pattern, filter_data)
        end = time.perf_counter()
        total_time += (end - start)
    return (total_time / REPEAT) * 1000


# ==========================================================
# [5] 모드 1
# ==========================================================
def mode1():
    print("\n#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = input_matrix("필터 A", 3)
    print()
    filter_b = input_matrix("필터 B", 3)

    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = input_matrix("패턴", 3)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    avg_ms = measure(pattern, filter_a)
    result = decide(score_a, score_b, "A", "B", f"판정 불가 (|A-B| < {EPSILON})")

    print("\n#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{REPEAT}회): {avg_ms:.4f} ms")
    print(f"판정: {result}")

    print("\n#----------------------------------------")
    print(f"# [4] 성능 분석 (평균/{REPEAT}회)")
    print("#----------------------------------------")
    print("크기        평균 시간(ms)    연산 횟수")
    print("--------------------------------------")
    print(f"3x3         {avg_ms:>10.4f}    {3*3:>8}")


# ==========================================================
# [6] 메인
# ==========================================================
def main():
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ").strip()

    if choice == "1":
        mode1()
    elif choice == "2":
        print("(모드 2는 다음 단계에서 구현합니다)")
    else:
        print("잘못된 선택입니다. 1 또는 2를 입력하세요.")


main()