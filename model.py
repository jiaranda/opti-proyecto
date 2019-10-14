from gurobipy import GRB, Model, quicksum
# define model


def define_model(
    medical_centers,
    medics,
    modules,
    days,
    notification_rates,
    time_between,
    medical_centers_boxes,
    fine_cost,
    action_plan_cost
    ):

    model = Model()

    # variables

    x = model.addVars(medics, medical_centers, days, modules, vtype=GRB.BINARY, name="x")
    delta = model.addVars(medical_centers, vtype=GRB.BINARY, name="delta")
    theta = model.addVars(medical_centers, vtype=GRB.BINARY, name="theta")

    model.update()

    # objective function

    obj = quicksum(fine_cost * delta[center] + action_plan_cost * theta[center] for center in medical_centers)
    model.setObjective(obj, GRB.MINIMIZE)

    # restrictions
    # for medic in medics for center in medical_centers for day in days for module in modules

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] for center in medical_centers
            ) <= 1 for medic in medics for day in days for module in modules), 
            name='r1'
    )
    
    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] for medic in medics
        ) == medical_centers_boxes[center] for center in medical_centers for day in days for module in modules),
        name='r2'
    )

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] for center in medical_centers for day in days for module in modules
        ) <= 10 for medic in medics),
        name='r3'
    )

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] * notification_rates[medic] for medic in medics for day in days for module in modules
        )/(len(days) * len(modules) * medical_centers_boxes[center]) <= 0.75 + 0.25 * (1 - delta[center]) for center in medical_centers),
        name='r4.1'
    )

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] * notification_rates[medic] for medic in medics for day in days for module in modules
        )/(len(days) * len(modules) * medical_centers_boxes[center]) >= 0.75 * (1 - delta[center]) for center in medical_centers),
        name='r4.2'
    )

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] * notification_rates[medic] for medic in medics for day in days for module in modules
        )/(len(days) * len(modules) * medical_centers_boxes[center]) <= 0.9 + 0.1 * (1 - theta[center]) for center in medical_centers),
        name='r5.1'
    )

    model.addConstrs(
        (quicksum(
            x[medic, center, day, module] * notification_rates[medic] for medic in medics for day in days for module in modules
        )/(len(days) * len(modules) * medical_centers_boxes[center]) >= 0.9 * (1 - theta[center]) for center in medical_centers),
        name='r5.2'
    )

    model.addConstrs(
        (x[medic, center, day, 1] + x[medic, center, day, 2] <= 1 for medic in medics for center in medical_centers for day in days for module in modules),
        name='r6'
    )

    return model