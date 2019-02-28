path = 'a_example.txt'


def parse_txt(path, func):
    pictures = []
    lines = [line.rstrip('\n') for line in open(path)]
    num_of_pictures = lines[0].split(' ')
    for line in lines[1:]:
        pictures.append(func(line))
    return num_of_pictures, pictures


def line_manipulation(line: str):
    line_split = line.split(' ')
    orientation = line_split[0]
    num_of_tags = int(line_split[1])
    tags = line_split[2:]
    return [orientation, num_of_tags, tags]


print(parse_txt(path, line_manipulation))