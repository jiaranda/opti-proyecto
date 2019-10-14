from parameters import medical_centers, medics, modules, days, notification_rates, time_between, medical_centers_boxes, fine_cost, action_plan_cost
from model import define_model

params = {
    'medical_centers': medical_centers,
    'medics': medics,
    'modules': modules,
    'days': days,
    'notification_rates': notification_rates,
    'time_between': time_between,
    'medical_centers_boxes': medical_centers_boxes,
    'fine_cost': fine_cost,
    'action_plan_cost': action_plan_cost
}

print('defining model')
model = define_model(**params)
print('model ready')

print('optimizing')
model.optimize()
print('🎈')

model.printAttr("X")

print("\n-------------\n")
# for constr in model.getConstrs():
#     print(constr, constr.getAttr("slack"))