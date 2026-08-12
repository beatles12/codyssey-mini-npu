def mac(pattern, filter_data):
    score = 0

    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score += pattern[row][col] * filter_data[row][col]

    return score

def input_matrix(name):
    print(f"{name}을 3줄 입력하세요.")

    matrix = []

    for _ in range(3):
        row = input().split()
        row = [float(value) for value in row]
        matrix.append(row)

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