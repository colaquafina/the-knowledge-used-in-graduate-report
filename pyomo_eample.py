import numpy as np
import pyomo.environ as pyo


model=pyo.ConcreteModel()

#binary
model.metal_binary=pyo.Set(initialize=[i for i in range(4)])
model.x=pyo.Var(model.metal_binary,within=pyo.Binary,initialize=1)
#continous
model.metal_continous=pyo.Set(initialize=[i for i in range(4)])
model.y=pyo.Var(model.metal_continous,bounds=(0,10),within=pyo.NonNegativeReals,initialize=5)

weight_binary_total=np.array([5,3,4,6])

weight_binary_carbon=np.array([5,4,5,3])/100
weight_continous_carbon=np.array([8,7,6,3])/100
weight_continous_moly=np.array([6,7,8,9])/100
weight_binary_moly=np.array([3,3,4,4])/100
cost_binary=np.array([350,330,310,280])
cost_continous=np.array([500,450,400,100])
model.obj=pyo.Objective(
    expr=sum(cost_binary[i]*model.x[i] for i in model.x)+sum(cost_continous[j]*model.y[j] for j in model.y),
    sense=pyo.minimize
)

model.c1=pyo.Constraint(
    expr=sum(weight_binary_total[i]*model.x[i] for i in model.x)+sum(model.y[j] for j in model.y)==25
    )

model.c2=pyo.Constraint(
    expr=sum(weight_binary_carbon[i]*model.x[i] for i in model.x)+sum(weight_continous_carbon[j]*model.y[j] for j in model.y)==1.25
    )

model.c3=pyo.Constraint(
    expr=sum(weight_binary_moly[i]*model.x[i] for i in model.x)+sum(weight_continous_moly[j]*model.y[j] for j in model.y)==1.25
    )

opt=pyo.SolverFactory('gurobi').solve(model,tee=True)
opt.write()
# print(pyo.value(model.obj))
# print(pyo.value(model.x))
    
# print(' ')
# print(pyo.value(model.y))
x_opt=np.array([pyo.value(model.x[i]) for i in range(4)])
y_opt=np.array([pyo.value(model.y[i]) for i in range(4)])
obj_values=pyo.value(model.obj)
print(x_opt)
print(y_opt)
print(obj_values)