from parameters import medics
import pandas as pd
import json

def get_model_output(model):

    variables = model.getVars()

    optimal_solution_x = dict()
    fine = dict()
    action_plan = dict()
    count = 1
    for var in variables:
        if 'x' in var.varName and int(var.x) != 0:
            indices = var.varName.strip('x').strip('[]').split(',')
            optimal_solution_x[count] = {
                'name': 'x',
                'medic': int(indices[0]),
                'medical_center': indices[1],
                'day': int(indices[2]),
                'module': int(indices[3]),
                'value': var.x
            }
            count += 1
        elif 'delta' in var.varName and int(var.x) != 0:
            medical_center = var.varName.strip('delta').strip('[]')
            fine[count] = {
                'name': 'delta',
                'medical_center': medical_center,
                'value': var.x
            }
            count += 1
        elif 'theta' in var.varName and int(var.x) != 0:
            medical_center = var.varName.strip('theta').strip('[]')
            action_plan[count] = {
                'name': 'theta',
                'medical_center': medical_center,
                'value': var.x
            }
            count += 1

    optimal_solution_x = pd.DataFrame.from_dict(optimal_solution_x, orient='index')
    fine = pd.DataFrame.from_dict(fine, orient='index')
    action_plan = pd.DataFrame.from_dict(action_plan, orient='index')


    schedules = dict()
    for medic in medics:
        medic_schedule = optimal_solution_x[optimal_solution_x['medic'] == medic]
        schedules[medic] = medic_schedule.drop(columns=['value', 'medic', 'name']).sort_values(by=['day', 'module'])

    for k, v in schedules.items():
        schedules[k] = v.to_dict('records')

    with open('./schedule.json', 'w') as file:
        file.write(json.dumps(schedules))




