from gurobipy import GRB, Model
# define model


def define_model(notification_rates, time_between, ges_diagnostic_rates, medical_centers,
                 medics, modules, months, days, medical_centers_boxes):
    model = Model()

    #variables

    model.addVar()

    x_mpdqcb = model.addVar(vtype=GRB.BINARY, name="Xmpdqcb")
    delta_c = model.addVar(vtype=GRB.BINARY, name="delta c")
    theta_c = model.addVar(vtype=GRB.BINARY, name="theta c")

    model.update()
    #funcion bojetivo
    obj = quicksum(750 * delta_c)
    model.setObjective(obj, GRB.MINIMIZE)

    #restricciones
    #retornar el modelo

    return model