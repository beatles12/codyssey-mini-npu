def mac(pattern, filter_data):
    score = 0

    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score += pattern[row][col] * filter_data[row][col]

    return score

pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

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