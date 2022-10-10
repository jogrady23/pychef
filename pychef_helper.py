import yaml
import random

ASCII_ART = """
  ____  ____   __ __   ___   ____     ___         __   ____  ____          __   ___    ___   __  _      __ 
 /    ||    \ |  |  | /   \ |    \   /  _]       /  ] /    ||    \        /  ] /   \  /   \ |  |/ ]    |  |
|  o  ||  _  ||  |  ||     ||  _  | /  [_       /  / |  o  ||  _  |      /  / |     ||     ||  ' /     |  |
|     ||  |  ||  ~  ||  O  ||  |  ||    _]     /  /  |     ||  |  |     /  /  |  O  ||  O  ||    \     |__|
|  _  ||  |  ||___, ||     ||  |  ||   [_     /   \_ |  _  ||  |  |    /   \_ |     ||     ||     \     __ 
|  |  ||  |  ||     ||     ||  |  ||     |    \     ||  |  ||  |  |    \     ||     ||     ||  .  |    |  |
|__|__||__|__||____/  \___/ |__|__||_____|     \____||__|__||__|__|     \____| \___/  \___/ |__|\_|    |__|
                                                                                                           
"""

RECIPE_PATHS = [
    'yaml_dir/baking.yaml',
    'yaml_dir/essentials.yaml',
    'yaml_dir/meals.yaml',
    'yaml_dir/snacks.yaml'
]

IGNORE_MEAL = 'template'

MEAL_FIELDS = ['name','ingredients','essentials','time','satisfies','min_quantity']
BAKING_FIELDS = ['name','ingredients','essentials','time']
SNACK_FIELDS = ['name','ingredients','essentials','time']

def generate_meal_plan(num_breakfast, num_lunch, num_dinner, num_snacks, num_baking):
    # Generate the recipe dict
    recipes_dict = load_recipes()
    recipes_valid, invalid_dict = validate_recipes(recipes_dict)

    if not recipes_valid:
        print('INVALID RECIPES')
        print(invalid_dict)

    recipes_by_type = generate_dict_by_type(recipes_dict)
    recipe_name_map_dict = generate_name_mapping_dict(recipes_dict)

    # Generate the menu
    breakfast_meals, breakfast_grocery_meals = generate_menu(num_breakfast, recipes_by_type['breakfast'], recipe_name_map_dict)
    lunch_meals, lunch_grocery_meals = generate_menu(num_lunch, recipes_by_type['lunch'], recipe_name_map_dict)
    dinner_meals, dinner_grocery_meals = generate_menu(num_dinner, recipes_by_type['dinner'], recipe_name_map_dict)
    snacks, snacks_grocery_meals = generate_menu(num_snacks, recipes_dict['snacks'], recipe_name_map_dict)
    baking, baking_grocery_meals = generate_menu(num_baking, recipes_dict['baking'], recipe_name_map_dict)
    essentials = recipes_dict['essentials']['essentials']

    # Generate the grocery list based on the menu
    ingredients_list, essentials_list = generate_grocery_list(recipes_dict,
                                                              meal_list=breakfast_grocery_meals + lunch_grocery_meals + dinner_grocery_meals,
                                                              snack_list=snacks_grocery_meals,
                                                              baking_list=baking_grocery_meals,
                                                              essentials_list=essentials)
    # Generate the visual friendly menu
    return {
        'breakfast': succinct_list(breakfast_meals),
        'lunch': succinct_list(lunch_meals),
        'dinner': succinct_list(dinner_meals),
        'snacks': succinct_list(snacks),
        'baking': succinct_list(baking),
        'ingredients': succinct_list(ingredients_list),
        'essentials': succinct_list(essentials_list)
    }

def print_meal_plan(chef_dict):
    print(ASCII_ART)

    print('\n=================')
    print('MEAL PLAN')
    print('=================')

    print('\nBreakfast:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['breakfast']]

    print('\nLunch:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['lunch']]

    print('\nDinner:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['dinner']]

    print('\nSnacks:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['snacks']]

    print('\nBaking:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['baking']]

    print('\n=================')
    print('INGREDIENTS')
    print('=================')

    print('\nGet each time:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['ingredients']]

    print('\nCheck stock:')
    print('----------------')
    [print('- ' + x) for x in chef_dict['essentials']]


def generate_name_mapping_dict(recipes_dict):
    mapping_dict = {}
    for meal_type in recipes_dict.keys():
        for meal in recipes_dict[meal_type].keys():
            if type(recipes_dict[meal_type][meal]) == dict:
                mapping_dict[meal] = recipes_dict[meal_type][meal]['name']
    return mapping_dict


def generate_grocery_list(reciples_dict, meal_list, snack_list, baking_list, essentials_list):
    parent_essentials_list = essentials_list
    parent_ingredients_list = []

    # For each meal, load in meal, identify options, add to ingredient list
    mapping_dict = {
        'meals': meal_list,
        'snacks': snack_list,
        'baking': baking_list
    }
    for key in mapping_dict.keys():
        active_list = mapping_dict[key]
        active_recipe_dict = reciples_dict[key]

        for meal in active_list:
            meal_info = active_recipe_dict[meal]
            meal_ingredients_list = []
            for ingredient in meal_info['ingredients']:
                if type(ingredient) == str:
                    meal_ingredients_list.append(ingredient)
                else:
                    sampled_thing = random.choice(ingredient['options'])
                    if type(sampled_thing) == str:
                        meal_ingredients_list.append(sampled_thing)
                    else:
                        [meal_ingredients_list.append(x) for x in sampled_thing[list(sampled_thing.keys())[0]]]
            [parent_ingredients_list.append(x) for x in meal_ingredients_list]
            if meal_info['essentials'] is not None:
                [parent_essentials_list.append(x) for x in meal_info['essentials']]

    return parent_ingredients_list, parent_essentials_list

def succinct_list(input_list):
    indiv_items = sorted(list(set(input_list)))
    final_list = []
    for item in indiv_items:
        final_list.append(item + ' (x' + str(input_list.count(item)) + ')')
    return final_list

def generate_menu(num_meals, meal_options_dict, name_map_dict):
    remaining_meals = num_meals
    meal_list = []
    meal_grocery_list = []
    meal_options = list(meal_options_dict.keys())
    while remaining_meals > 0:
        test_meal = random.choice(meal_options)
        if 'min_quantity' in meal_options_dict[test_meal].keys():
            quantity = meal_options_dict[test_meal]['min_quantity']
        else:
            quantity = 1
        [meal_list.append(name_map_dict[test_meal]) for i in range(quantity)]
        meal_grocery_list.append(test_meal)
        remaining_meals -= quantity
    return meal_list, meal_grocery_list

def generate_snacks(num_snacks, snack_options_dict):
    remaining_snacks = num_snacks
    snacks_list = []
    snack_options = list(snack_options_dict.keys())
    while remaining_snacks > 0:
        test_meal = random.choice(snack_options)
        quantity = 1
        [snacks_list.append(test_meal) for x in range(quantity)]
        remaining_snacks -= quantity
    return snacks_list

def generate_dict_by_type(recipes_dict):
    breakfast_dict = {}
    lunch_dict = {}
    dinner_dict = {}

    for meal in recipes_dict['meals'].keys():
        meal_satisfies_list = recipes_dict['meals'][meal]['satisfies']
        if 'breakfast' in meal_satisfies_list:
            breakfast_dict[meal] = recipes_dict['meals'][meal]
        if 'lunch' in meal_satisfies_list:
            lunch_dict[meal] = recipes_dict['meals'][meal]
        if 'dinner' in meal_satisfies_list:
            dinner_dict[meal] = recipes_dict['meals'][meal]

    return {'breakfast': breakfast_dict,
            'lunch': lunch_dict,
            'dinner': dinner_dict}

# Load in recipes
def load_recipes():
    recipes_dict = {}
    for path in RECIPE_PATHS:
        recipe_type = path.split('.')[0].split('/')[-1]
        with open(path, "r") as stream:
            recipes_dict[recipe_type] = yaml.safe_load(stream)
    return recipes_dict

# Validate recipe types
def validate_recipes(recipes_dict):
    meals_valid = True
    snacks_valid = True
    baking_valid = True
    
    meals_dict = recipes_dict['meals']
    snacks_dict = recipes_dict['snacks']
    baking_dict = recipes_dict['baking']
    
    # Validate meals
    invalid_meals = []
    for key in meals_dict.keys():
        temp_dict = meals_dict[key]
        if sorted(list(temp_dict.keys())) != sorted(MEAL_FIELDS):
            meals_valid = False
            invalid_meals.append(key)
    
    # Validate baking
    invalid_baking = []
    for key in baking_dict.keys():
        temp_dict = baking_dict[key]
        if sorted(list(temp_dict.keys())) != sorted(BAKING_FIELDS):
            baking_valid = False
            invalid_baking.append(key)
            
    # Validate snacks
    invalid_snacks = []
    for key in snacks_dict.keys():
        temp_dict = snacks_dict[key]
        if sorted(list(temp_dict.keys())) != sorted(SNACK_FIELDS):
            snacks_valid = False
            invalid_snacks.append(key)
    
    overall_valid = meals_valid and snacks_valid and baking_valid
    invalid_dict = {
        'meals': invalid_meals,
        'snacks': invalid_snacks,
        'baking': invalid_baking
    }
    
    return overall_valid, invalid_dict

if __name__ == '__main__':
    test = generate_meal_plan(4, 4, 5, 4, 2)
    print_meal_plan(test)
    