from gurobipy import GRB, Model, quicksum
# define model


def define_model(notification_rates, time_between, medical_centers,
                 medics, modules, months, days, medical_centers_boxes):
    model = Model()

    # variables

    x = model.addVars(medics, months, days, modules, medical_centers, medical_centers_boxes, vtype=GRB.BINARY, name="x")
    delta = model.addVars(medical_centers, vtype=GRB.BINARY, name="delta")
    theta = model.addVars(medical_centers, vtype=GRB.BINARY, name="theta")

    model.update()

    # objective function

    obj = quicksum(750 * delta[center] + 100 * theta[center] for center in medical_centers)
    model.setObjective(obj, GRB.MINIMIZE)

    # restrictions

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] for box in medical_centers_boxes for center in medical_centers
            ) <= 1 for medic in medics for month in months for day in days for module in modules), 
            name='r1'
    )
    
    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] for medic in medics
        ) == 1 for month in months for day in days for module in modules for center in medical_centers for box in medical_centers_boxes),
        name='r2'
    )

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] for module in modules for center in medical_centers for box in medical_centers_boxes for day in range(d, d+5+1)
        ) == 1 for medic in medics for month in months for d in (1, 7, 13, 19)),
        name='r3'
    )

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] * notification_rates[medic] for month in months for day in days for module in modules for box in medical_centers_boxes for medic in medics
        )/(len(months) * len(days) * len(modules) * len(medical_centers_boxes)) <= 0.75 + 0.25 * (1 - delta[center]) for center in medical_centers),
        name='r4.1'
    )

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] * notification_rates[medic] for month in months for day in days for module in modules for box in medical_centers_boxes for medic in medics
        )/(len(months) * len(days) * len(modules) * len(medical_centers_boxes)) >= 0.75 * (1 - delta[center]) for center in medical_centers),
        name='r4.2'
    )

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] * notification_rates[medic] for month in months for day in days for module in modules for box in medical_centers_boxes for medic in medics
        )/(len(months) * len(days) * len(modules) * len(medical_centers_boxes)) <= 0.9 + 0.1 * (1 - theta[center]) for center in medical_centers),
        name='r5.1'
    )

    model.addConstrs(
        (quicksum(
            x[medic, month, day, module, center, box] * notification_rates[medic] for month in months for day in days for module in modules for box in medical_centers_boxes for medic in medics
        )/(len(months) * len(days) * len(modules) * len(medical_centers_boxes)) >= 0.9 - (1 - theta[center]) for center in medical_centers),
        name='r5.2'
    )

    model.addConstrs(
        (x[medic, month, day, 1, center1, box] + x[medic, month, day, 2, center2, box] <= 1 for month in months for day in days for module in modules for box in medical_centers_boxes for medic in medics for center1, center2 in ((center1, center2) for center1 in medical_centers for center2 in medical_centers if time_between[(center1, center2)])),
        name='r6'
    )

    model.addConstrs(
        (quicksum(x[medic, month, day, module, center, box] for box in medical_centers_boxes) == quicksum(x[medic, month, day + 6, module, center, box] for box in medical_centers_boxes) for month in months for day in range(1, 18+1) for module in modules for center in medical_centers for medic in medics),
        name='r7'
    )

    return model