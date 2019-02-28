print("Lets rule them all!")

print("I got 99 problems but commit ain't one")


def parse_txt(path, func):
    rows = []
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            rows.append(func(line))
    return rows
