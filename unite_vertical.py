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
    random_slide = random.choice(list_of_slides)
    list_of_slides.remove(random_slide)
    while list_of_slides:
        partner_slides = []
        for partner_slide in list_of_slides:
            partner_slide_score = get_couple_slides_score(random_slide, partner_slide)
            partner_slides.append((partner_slide, partner_slide_score))

        if partner_slides:
            for i = 5
            best_slide = max(partner_slides, key=lambda item: item[1])
            for slide in list_of_slides:
                if slide == best_slide[0]:
                    list_of_slides.remove(slide)
                    result.append()
            result.append((random_slide[0], min_photo[0]))

    return result