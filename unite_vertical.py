import random

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
    return result, slide_show_score

def get_best_slideshow(list_of_slides):
    num_of_slides = len(list_of_slides)
    result = []
    for i in range(num_of_slides):
        list_copy = [elem for elem in list_of_slides]
        result.append(create_random_slideshow(list_copy))
    best_slide_shows = max(result, key=lambda item: item[1])
    return best_slide_shows[0]

