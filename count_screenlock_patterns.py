import itertools

def counter(pattern_length):
    invalid_patterns = [
            ("13", "2"), ("17", "4"), ("39", "6"), ("79", "8"),
            ("46", "5"), ("28", "5"), ("19", "5"), ("37", "5")
    ]
    invalid_patterns += [(invalid_pattern[0][::-1], invalid_pattern[1]) for invalid_pattern in invalid_patterns]

    total_possibilities, invalid_possibilities = 0, 0

    for possibility in itertools.permutations(list(range(1,10)), pattern_length):
        possibility = "".join([str(i) for i in possibility ])
        total_possibilities = total_possibilities + 1

        for invalid_pattern in invalid_patterns:
            if invalid_pattern[0] in possibility and invalid_pattern[1] not in possibility[:possibility.index(invalid_pattern[0])]:
                invalid_possibilities = invalid_possibilities + 1
                break

    return total_possibilities - invalid_possibilities

for i in range(1,10):
    print (" %s --> " % i, counter(i))
