from parameters import notification_rates, time_between, medical_centers, medics, modules, months, days, medical_centers_boxes
from model import define_model

params = {
    'notification_rates': notification_rates,
    'time_between': time_between,
    'medical_centers': medical_centers,
    'medics': medics,
    'modules': modules,
    'months': months,
    'days': days,
    'medical_centers_boxes' : medical_centers_boxes
}

print('defining model')
model = define_model(**params)
print('model ready')

print('optimizing')
model.optimize()
print('🎈')

# Mostrar los valores de las soluciones
model.printAttr("X")

print("\n-------------\n")
# Imprime las holguras de las restricciones (0 significa que la restricción es activa.
for constr in model.getConstrs():
    print(constr, constr.getAttr("slack"))