import math
from typing import List, Tuple


def calculate_total_responses(categories):
    return [sum(category) for category in categories]


# def calculate_ability_parameter(total_responses, num_categories, num_questions):
#     return math.log(sum(total_responses) / (num_categories * num_questions) / (1 - sum(total_responses) / (num_categories * num_questions)))

def calculate_ability_parameter(total_responses, num_categories, num_questions):
    try:
        return math.log(sum(total_responses) / (num_categories * num_questions) / (1 - sum(total_responses) / (num_categories * num_questions)))
    except:
        if(sum(total_responses)==0):
            return -4
        else:
            return 4


# def calculate_lesson_difficulty(category_responses, num_questions: int):
#     try:
#         return math.log((1 - (sum(category_responses) / num_questions)) / (sum(category_responses) / num_questions))
#     except:
#         print("I am -4")
#         return -4

def calculate_lesson_difficulty(category_responses, num_questions: int):
    try:
        return math.log((1 - (sum(category_responses) / num_questions)) / (sum(category_responses) / num_questions))
    except:
            if all(response == 0 for response in category_responses):
                return 4
            else:
                return -4


def calculate_correctness_prob(a, lesson_difficulty):
    return ((math.e) ** (a - lesson_difficulty)) / (1 + (math.e) ** (a - lesson_difficulty))


def filter_categories(correctness_prob):
    return [i for i in range(len(correctness_prob)) if correctness_prob[i] < 0.70]


def sort_categories(filtered_categories, category_names, correctness_prob):
    info = []
    for j in filtered_categories:
        info.append((category_names[j], correctness_prob[j] * (1 - correctness_prob[j])))
    info.sort(key=lambda x: x[1])
    return info


def shortest_path(categories, category_names):
    total_responses = calculate_total_responses(categories)
    print(total_responses)
    print(sum(total_responses))
    num_categories = len(categories)
    print(num_categories)
    num_questions = len(categories[0])
    print(num_questions)
    a = calculate_ability_parameter(total_responses, num_categories, num_questions)
    print(a)
    lesson_difficulty = [calculate_lesson_difficulty(categories[i], num_questions) for i in range(num_categories)]
    print(lesson_difficulty)
    correctness_prob = [calculate_correctness_prob(a, lesson_difficulty[i]) for i in range(num_categories)]
    print(correctness_prob)
    filtered_categories = filter_categories(correctness_prob)
    print(filtered_categories)
    shortest_path = sort_categories(filtered_categories, category_names, correctness_prob)
    print(shortest_path)
    return shortest_path

# def generate_responses(shortest_path_results):
#     response_lists = []
#     for result in shortest_path_results:
#         value = result[1]
#         if value < 0.05:
#             response_lists.append(['H', 'H', 'H', 'M', 'M', 'M'])
#         elif value < 0.2:
#             response_lists.append(['H', 'H', 'M', 'M', 'M', 'E'])
#         elif value < 0.5:
#             response_lists.append(['H', 'M', 'M', 'M', 'E', 'E'])
#         elif value < 0.8:
#             response_lists.append(['M', 'M', 'E', 'E', 'E', 'E'])
#         else:
#             response_lists.append(['E', 'E', 'E', 'E', 'E', 'E'])
#     return response_lists

# def generate_responses(shortest_path_results: List[Tuple[str, float]]) -> List[Tuple[str, float, List[str]]]:
#     response_combinations = []
#     for course_info in shortest_path_results:
#         course_name = course_info[0]
#         course_info_factor = course_info[1]
#         if course_info_factor < 0.05:
#             response_combinations.append((course_name, course_info_factor, ["E"]*6))
#         elif course_info_factor < 0.2:
#             response_combinations.append((course_name, course_info_factor, ["E"]*3 + ["M"]*3))
#         elif course_info_factor < 0.5:
#             response_combinations.append((course_name, course_info_factor, ["E"]*2 + ["M"]*2 + ["H"]*2))
#         else:
#             response_combinations.append((course_name, course_info_factor, ["E", "M", "H", "M", "M", "H"]))
#     return response_combinations

def generate_responses(shortest_path_results: List[Tuple[str, float]]) -> List[Tuple[str, float, List[str]]]:
    response_combinations = []
    for course_info in shortest_path_results:
        course_name = course_info[0]
        course_info_factor = course_info[1]
        if course_info_factor < 0.05:
            response_combinations.append((course_name, course_info_factor, ["E"]*3))
        elif course_info_factor < 0.2:
            response_combinations.append((course_name, course_info_factor, ["E"]*2 + ["M"]*1))
        elif course_info_factor < 0.5:
            response_combinations.append((course_name, course_info_factor, ["E"]*1 + ["M"]*1 + ["H"]*1))
        else:
            response_combinations.append((course_name, course_info_factor, ["M", "M", "H"]))
    return response_combinations