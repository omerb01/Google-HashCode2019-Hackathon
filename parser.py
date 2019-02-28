path = 'b_small.in'


def parse_txt(path, func):
    rows = []
    lines = [line.rstrip('\n') for line in open(path)]
    title = lines[0].split(' ')
    for line in lines[1:]:
        rows.append(func(line))
    return title, rows


def line_manipulation(line: str):
    # TODO: manipulation of a line
    return list(line)


print(parse_txt(path, line_manipulation))