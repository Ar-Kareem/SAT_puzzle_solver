from ortools.sat.python import cp_model


def and_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target <= c)
    model.Add(target >= sum(cs) - len(cs) + 1)


def or_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target >= c)
    model.Add(target <= sum(cs))
