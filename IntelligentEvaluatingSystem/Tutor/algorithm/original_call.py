from original_function import shortest_path,generate_responses


# categories = [[1, 1, 1, 0, 0, 0], [1, 0, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 1, 1], [1, 1, 0, 1, 0, 1]]
categories = [[0, 1, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 0, 0], [1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0]]
# categories = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 0, 0], [1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0]]
# categories = [[1, 1, 1]]
# categories = [[0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 1, 1], [1, 0, 0, 1, 0, 1], [0, 0, 1, 1, 1, 1]]
category_names = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
# category_names = ['Category A']
shortest_path_results = shortest_path(categories, category_names)
response_lists = generate_responses(shortest_path_results)
print(response_lists)