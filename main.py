import random


def parse_txt(path, func):
    pictures = []
    lines = [line.rstrip('\n') for line in open(path)]
    num_of_pictures = lines[0].split(' ')[0]
    for i, line in enumerate(lines[1:]):
        pictures.append(func(line, i))
    return num_of_pictures, pictures


def line_manipulation(line: str, i):
    line_split = line.split(' ')
    orientation = line_split[0]
    num_of_tags = int(line_split[1])
    tags = line_split[2:]
    return (i, orientation, num_of_tags, tags)


def get_verticals(dataset):
    result = []
    for id, orientation, num_of_tags, tags in dataset[1]:
        if orientation == 'V':
            result.append((id, orientation, num_of_tags, tags))
    return result


def get_num_intersect_tags(photo1, photo2):
    photo1_tags = photo1[3]
    photo2_tags = photo2[3]
    intersect_tags_list = list(set(photo1_tags).intersection(photo2_tags))
    return len(intersect_tags_list)


def get_num_union_tags(photo1, photo2):
    photo1_tags = photo1[3]
    photo2_tags = photo2[3]
    union_tags_list = list(set(photo1_tags).union(photo2_tags))
    return len(union_tags_list)


def get_num_dif_first_tags(photo1, photo2):
    photo1_tags = photo1[3]
    photo2_tags = photo2[3]
    union_tags_list = list(set(photo1_tags).union(photo2_tags).difference(photo2_tags))
    return len(union_tags_list)


def get_num_dif_second_tags(photo1, photo2):
    photo1_tags = photo1[3]
    photo2_tags = photo2[3]
    union_tags_list = list(set(photo1_tags).union(photo2_tags).difference(photo1_tags))
    return len(union_tags_list)


def sort_photos_by_common_num(vertical_photos):
    # result format: (id, sorted_photos_by_common_num)
    result = []
    for photo in vertical_photos:
        sorted_photos = []
        for id, orientation, num_of_tags, tags in vertical_photos:
            num_common_tags = get_num_intersect_tags(photo, (id, orientation, num_of_tags, tags))
            sorted_photos.append((id, num_common_tags))
        sorted_photos.sort(key=lambda item: item[1])
        sorted_photos = [id for id, common_num in sorted_photos]
        result.append((photo[0], sorted_photos))

    return result


def create_random_combined_photos(vertical_photos):
    result = []
    while vertical_photos:
        random_photo = random.choice(vertical_photos)
        vertical_photos.remove(random_photo)
        photos = []
        for id, orientation, num_of_tags, tags in vertical_photos:
            num_common_tags = get_num_intersect_tags(random_photo, (id, orientation, num_of_tags, tags))
            photos.append((id, num_common_tags))
        if photos:
            min_photo = min(photos, key=lambda item: item[1])
            for photo in vertical_photos:
                if photo[0] == min_photo[0]:
                    vertical_photos.remove(photo)
            result.append((random_photo[0], min_photo[0]))

    return result


# def sort_photos_by_balance(photos):
#     # result format: (id, sorted_photos_by_common_num)
#     result = []
#     for photo in photos:
#         sorted_photos = []
#         for id, orientation, num_of_tags, tags in photos:
#             num_intersect_tags = get_num_intersect_tags(photo, (id, orientation, num_of_tags, tags))
#             num_diff_first_tags = get_num_dif_first_tags(photo, (id, orientation, num_of_tags, tags))
#             num_diff_second_tags = get_num_dif_second_tags(photo, (id, orientation, num_of_tags, tags))
#             sorted_photos.append((id, num_common_tags))
#         sorted_photos.sort(key=lambda item: item[1])
#         sorted_photos = [id for id, common_num in sorted_photos]
#         result.append((photo[0], sorted_photos))
#
#     return result


if __name__ == '__main__':
    # dataset = parse_txt('a_example.txt', line_manipulation)
    dataset = parse_txt('c_memorable_moments.txt', line_manipulation)
    verticals_photos = get_verticals(dataset)
    create_random_combined_photos(verticals_photos)

    x = 0
