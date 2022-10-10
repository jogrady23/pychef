import yaml

RECIPE_PATHS = [
    'yaml_dir/baking.yaml',
    'yaml_dir/essentials.yaml',
    'yaml_dir/meals.yaml',
    'yaml_dir/snacks.yaml'
]

MEAL_FIELDS = ['name','ingredients','essentials','time','satisfies','min_quantity']
BAKING_FIELDS = ['name','ingredients','essentials','time']
SNACK_FIELDS = ['name','ingredients','essentials','time']

def generate_meal_plan(num_breakfast, num_lunch, num_dinner, num_snacks):
    # Generate the recipe dict
    recipes_dict = load_recipes()
    recipes_valid, invalid_dict = validate_recipes(recipes_dict)

    if not recipes_valid:
        print('INVALID RECIPES')
        print(invalid_dict)

    recipes_by_type = generate_dict_by_type(recipes_dict)

    # Generate the menu
    breakfast_meals = generate_menu(num_breakfast, recipes_by_type['breakfast'])

    # Generate the grocery list based on the meny

def generate_menu(num_meals, meal_options_dict):


def generate_dict_by_type(recipes_dict):
    breakfast_dict = {}
    lunch_dict = {}
    dinner_dict = {}

    for meal in recipes_dict['meals'].keys():
        meal_satisfies_list = recipes_dict['meals']['satisfies']
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
    