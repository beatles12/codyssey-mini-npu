import time
import json

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
# [3] 라벨 정규화
# ==========================================================
def normalize_label(raw):
    text = str(raw).strip().lower()
    if text == "+" or text == "cross":
        return "Cross"
    elif text == "x":
        return "X"
    else:
        return None


# ==========================================================
# [4] 데이터 로드
# ==========================================================
def load_data(path="data.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: {path} 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"오류: {path} 파일 형식이 올바르지 않습니다.")
        return None


def extract_size(key):
    parts = key.split("_")
    if len(parts) != 3:
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


# ==========================================================
# [5] 사용자 입력
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
# [6] 성능 측정
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
# [7] 모드 1 — 사용자 입력 (3x3)
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
# [8] 모드 2 — data.json 분석
# ==========================================================
def mode2():
    data = load_data()
    if data is None:
        return

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    # ----- [1] 필터 로드 -----
    print("\n#----------------------------------------")
    print("# [1] 필터 로드")
    print("#----------------------------------------")
    for filter_key in filters:
        labels = []
        for raw_label in filters[filter_key]:
            label = normalize_label(raw_label)
            if label is not None:
                labels.append(label)
        print(f"✓ {filter_key:<8} 필터 로드 완료 ({', '.join(labels)})")

    # ----- [2] 패턴 분석 -----
    print("\n#----------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#----------------------------------------")

    total = 0
    passed = 0
    fail_list = []

    for pattern_key in patterns:
        total += 1
        print(f"\n--- {pattern_key} ---")

        entry = patterns[pattern_key]
        pattern = entry.get("input")
        expected = normalize_label(entry.get("expected"))

        # 검증 1: 키에서 크기 추출
        size = extract_size(pattern_key)
        if size is None:
            reason = "키 형식 오류(size_N_idx 아님)"
            print(f"FAIL: {reason}")
            fail_list.append((pattern_key, reason))
            continue

        # 검증 2: 해당 크기 필터 존재
        filter_key = f"size_{size}"
        if filter_key not in filters:
            reason = f"{filter_key} 필터 없음"
            print(f"FAIL: {reason}")
            fail_list.append((pattern_key, reason))
            continue

        # 검증 3: 패턴/필터 크기 일치
        cross_filter = filters[filter_key].get("cross")
        x_filter = filters[filter_key].get("x")
        if len(pattern) != size or len(cross_filter) != size:
            reason = f"크기 불일치(패턴 {len(pattern)} vs 필터 {size})"
            print(f"FAIL: {reason}")
            fail_list.append((pattern_key, reason))
            continue

        # 검증 4: expected 라벨 해석 가능
        if expected is None:
            reason = f"expected 라벨 해석 불가({entry.get('expected')})"
            print(f"FAIL: {reason}")
            fail_list.append((pattern_key, reason))
            continue

        # MAC 연산 및 판정
        score_cross = mac(pattern, cross_filter)
        score_x = mac(pattern, x_filter)
        diff = abs(score_cross - score_x)
        result = decide(score_cross, score_x, "Cross", "X", "UNDECIDED")

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수:     {score_x}")

        if result == expected:
            passed += 1
            print(f"판정: {result} | expected: {expected} | PASS")
        else:
            if result == "UNDECIDED":
                reason = f"동점(UNDECIDED) 규칙에 따라 FAIL (|차이|={diff:.2e} < {EPSILON})"
            else:
                reason = f"판정({result}) != expected({expected})"
            fail_list.append((pattern_key, reason))
            print(f"판정: {result} | expected: {expected} | FAIL")
            print(f"      사유: {reason}")

    # ----- [3] 성능 분석 -----
    print("\n#----------------------------------------")
    print(f"# [3] 성능 분석 (평균/{REPEAT}회)")
    print("#----------------------------------------")
    print("크기        평균 시간(ms)    연산 횟수")
    print("--------------------------------------")
    for n in [3, 5, 13, 25]:
        dummy = [[1.0] * n for _ in range(n)]
        avg_ms = measure(dummy, dummy)
        size_text = f"{n}x{n}"
        print(f"{size_text:<12}{avg_ms:>10.4f}    {n*n:>8}")

    # ----- [4] 결과 요약 -----
    print("\n#----------------------------------------")
    print("# [4] 결과 요약")
    print("#----------------------------------------")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {len(fail_list)}개")

    if fail_list:
        print("\n실패 케이스:")
        for key, reason in fail_list:
            print(f"- {key}: {reason}")


# ==========================================================
# [9] 메인
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
        mode2()
    else:
        print("잘못된 선택입니다. 1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()