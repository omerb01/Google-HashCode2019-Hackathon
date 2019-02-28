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


def get_horizontals(dataset):
    result = []
    for id, orientation, num_of_tags, tags in dataset[1]:
        if orientation == 'H':
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


def create_slides_dataset(dataset):
    verticals_photos = get_verticals(dataset)
    horizontals_photos = get_horizontals(dataset)
    result = []
    result += create_random_combined_photos(verticals_photos)
    for photo in horizontals_photos:
        result.append((photo[0],))

    final_result = []
    for photos_tuple in result:
        try:
            photo_id1 = photos_tuple[0]
            photo_id2 = photos_tuple[1]
            photo1_tags = dataset[1][photo_id1][3]
            photo2_tags = dataset[1][photo_id2][3]
            union_tags = list(set(photo1_tags).union(photo2_tags))
            final_result.append((photos_tuple, union_tags))
        except IndexError:
            photo_id = photos_tuple[0]
            photo_tags = dataset[1][photo_id][3]
            final_result.append((photos_tuple, photo_tags))

    return final_result


def print_submission_file(submission_list):
    with open('submission.txt', 'w+') as file:
        file.write(len(submission_list))
        for result in submission_list:
            try:
                photo_id1 = result[0]
                photo_id2 = result[1]
                file.write(f'{photo_id1} {photo_id2}')
            except IndexError:
                photo_id = result[0]
                file.write(f'{photo_id}')


def get_num_intersect_tags_of_slides(slide1, slide2):
    random_slide_tags = slide1[1]
    partner_slide_tags = slide2[1]
    intersect_tags_list = list(set(random_slide_tags).intersection(partner_slide_tags))
    return len(intersect_tags_list)


def get_couple_slides_score(slide1, slide2):
    num_of_intersection = get_num_intersect_tags_of_slides(slide1, slide2)
    num_of_tags_in_slide1 = len(slide1[1])
    num_of_tags_in_slide2 = len(slide2[1])
    return min(num_of_intersection,
               num_of_tags_in_slide2 - num_of_intersection,
               num_of_tags_in_slide1 - num_of_intersection)


def create_random_slideshow(list_of_slides):
    result = []
    slide_show_score = 0
    random_slide = random.choice(list_of_slides)
    list_of_slides.remove(random_slide)
    while list_of_slides:
        partner_slides = []
        for partner_slide in list_of_slides:
            partner_slide_score = get_couple_slides_score(random_slide, partner_slide)
            partner_slides.append((partner_slide, partner_slide_score))

        if partner_slides:
            best_slide = max(partner_slides, key=lambda item: item[1])
            for slide in list_of_slides:
                if slide == best_slide[0]:
                    slide_show_score += best_slide[1]
                    list_of_slides.remove(slide)
                    result.append(random_slide[0])
                    random_slide = slide
    result.append(random_slide)
    return result, slide_show_score


def get_best_slideshow(list_of_slides):
    num_of_slides = len(list_of_slides)
    result = []
    for i in range(10):
        list_copy = [elem for elem in list_of_slides]
        result.append(create_random_slideshow(list_copy))
    best_slide_shows = max(result, key=lambda item: item[1])
    result = best_slide_shows[0]
    return result


if __name__ == '__main__':
    dataset = parse_txt('a_example.txt', line_manipulation)
    #dataset = parse_txt('c_memorable_moments.txt', line_manipulation)
    slides = create_slides_dataset(dataset)
    get_best_slideshow(slides)
    x = 0
