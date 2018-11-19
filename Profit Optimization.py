import pulp
import numpy as np
import scipy.stats as stats
import pandas as pd

#Employee Breakdown

"""The firm has a total of 150 employees. 
20 employees can only perform ESAs, 20 employees can only perform PCAs, and 30 employees can only perform Asset Assessments. 
Additionally, there are 10 employees who can perform both ESAs and PCAs, and 40 employees who can perform both PCAs and Asset Assessments, 
and 40 employees who can perform all three assessments. 
ESAs receive 2 time credits, PCAs receive 3 time credits, Asset receive 4 time credits.
There are a total of 20 time credits a month per employee. So there are 3000 total time credits.
Employee costs range based upon salary and selling prices of assessments range based on complexity of property."""

#Time Credits
Time_Emp = 20 #8 hour day equals one credit, five credits in a week, 20 a month
Total_Month_Credits = 3200 #20 credit hours a month times 150 employees
ESA_Time = .5 #Really 2 credits per ESA, however pulp doesnt allow for division with lpvariable
PCA_Time= .3 #Really 3 credits per PCA, however pulp doesnt allow for division with lpvariable
Asset_Time = .25 #Really 4 credits per asset, however pulp doesnt allow for division with lpvariable

#Level 1 Employees
ESA_Emp = 20
PCA_Emp = 20
Asset_Emp = 30
#Level 2 Employees
ESA_PCA_Emp = 10
PCA_Asset_Emp = 40
# Level 3 Employees
ESA_PCA_Asset_Emp = 40

#Assessment Costs Associated With Level 1 Employees From Cost Ranges
ENV_C = stats.randint.rvs(low=525, high=900, size=10000, random_state=4242)
ESA_Cost = np.mean(ENV_C)

PCA_C = stats.randint.rvs(low=700, high=1100, size=10000, random_state=4242)
PCA_Cost = np.mean(PCA_C)

Asset_C = stats.randint.rvs(low=750, high=1150, size=10000, random_state=4242)
Asset_Cost = np.mean(Asset_C)

#Assessment Costs Associated With Level 2 Employees From Cost Ranges
ESA_PCA_C = stats.randint.rvs(low=750, high=1150, size=10000, random_state=4242)
ESA_PCA_Cost = np.mean(ESA_PCA_C)

PCA_Asset_C = stats.randint.rvs(low=800, high=1200, size=10000, random_state=4242)
PCA_Asset_Cost = np.mean(PCA_Asset_C)

#Assessment Costs Associated With Level 3 Employees From Cost Ranges
ESA_PCA_Asset_C = stats.randint.rvs(low=900, high=1300, size=10000, random_state=4242)
ESA_PCA_Asset_Cost = np.mean(ESA_PCA_Asset_C)

#Selling Prices of Assessments From Price Ranges
ESA_Price = stats.randint.rvs(low=2000, high=2800, size=10000, random_state=4242)
ESA_P = np.mean(ESA_Price)
PCA_Price = stats.randint.rvs(low=2600, high=3600, size=10000, random_state=4242)
PCA_P = np.mean(PCA_Price)
Asset_Price = stats.randint.rvs(low=2900, high=3800, size=10000, random_state=4242)
Asset_P = np.mean(Asset_Price)

m = pulp.LpProblem("EMG Employee Assessment Distribution per Month", pulp.LpMaximize)

#Variables
ESA_L1 = pulp.LpVariable('Environmental Assessments:Level 1 Employees', lowBound=0, cat='Integer')
ESA_L2 = pulp.LpVariable('Environmental Assessments:Level 2 Employees', lowBound=0, cat='Integer')
ESA_L3 = pulp.LpVariable('Environmental Assessments:Level 3 Employees', lowBound=0, cat='Integer')
PCA_L1 = pulp.LpVariable('Property Assessments:Level 1 Employees', lowBound=0, cat='Integer')
PCA_L2 = pulp.LpVariable('Property Assessments:Level 2 Employees', lowBound=0, cat='Integer')
PCA_L3 = pulp.LpVariable('Property Assessments:Level 3 Employees', lowBound=0, cat='Integer')
Asset_L1 = pulp.LpVariable('Asset Assessments:Level 1 Employees', lowBound=0, cat='Integer')
Asset_L2 = pulp.LpVariable('Asset Assessments:Level 2 Employees', lowBound=0, cat='Integer')
Asset_L3 = pulp.LpVariable('Asset Assessments:Level 3 Employees', lowBound=0, cat='Integer')

#Profit Equations To Pass To The Obejective Function
ESA_Profit = pulp.lpSum([(ESA_L1*ESA_P) - (ESA_L1)*ESA_Cost +
                         (ESA_L2*ESA_P) - (ESA_L2)*ESA_PCA_Cost + 
                         (ESA_L3*ESA_P) - (ESA_L3)*ESA_PCA_Asset_Cost])

PCA_Profit = pulp.lpSum([(PCA_L1)*PCA_P - (PCA_L1)*PCA_Cost +
                         (PCA_L2)*PCA_P - (PCA_L2)*ESA_PCA_Cost + 
                         (PCA_L2)*PCA_P - (PCA_L2)*PCA_Asset_Cost +
                         (PCA_L3)*PCA_P - (PCA_L3)*ESA_PCA_Asset_Cost])

Asset_Profit = pulp.lpSum([(Asset_L1)*Asset_P - (Asset_L1)*Asset_Cost +
                         (Asset_L2)*Asset_P - (Asset_L2)*PCA_Asset_Cost + 
                         (Asset_L3)*Asset_P - (Asset_L3)*ESA_PCA_Asset_Cost])
    
# Objective Function
m += pulp.lpSum([ESA_Profit + PCA_Profit + Asset_Profit]), "Profit"

# Constraints
#Utilize all Level 1 employees
m += ESA_L1 == pulp.lpSum([(ESA_Emp*Time_Emp)*ESA_Time]), "Utilize All Level One ESA Employees for Environmental Assessments"
m += PCA_L1 == pulp.lpSum([(PCA_Emp*Time_Emp)*PCA_Time]), "Utilize All Level One PCA Employees for Property Assessments"
m += Asset_L1 == pulp.lpSum([(Asset_Emp*Time_Emp)*Asset_Time]), "Utilize All Level One Asset Employees for Asset Assessments"
m += pulp.lpSum([ESA_L1 + PCA_L1 + Asset_L1]) <= pulp.lpSum([(ESA_Emp*Time_Emp)*ESA_Time +
                (PCA_Emp*Time_Emp)*PCA_Time +
                (Asset_Emp*Time_Emp)*Asset_Time]), "Maximum Available Assessments For Level 1 Employees"

#Total level 2 assessments must be less than or equal to the max number of assessments (ESAs take 2 days, PCAs take 3 therefore more ESAs can be done)
m += pulp.lpSum([ESA_L2 + PCA_L2]) <= pulp.lpSum([(ESA_PCA_Emp*Time_Emp)*ESA_Time]), "Maximum Assessments for Level 2 ESA_PCA Employees"
m += pulp.lpSum([PCA_L2 + Asset_L2]) <= pulp.lpSum([(PCA_Asset_Emp*Time_Emp)*PCA_Time]), "Maximum Assessments for Level 2 PCA_Asset Employees"
m += pulp.lpSum([ESA_L3 + PCA_L3 + Asset_L3]) <= pulp.lpSum([(ESA_PCA_Asset_Emp*Time_Emp)*ESA_Time]), "Maximum Assessments for Level 3 ESA_PCA_Asset Employees"
m += pulp.lpSum([ESA_L1 + ESA_L2 + ESA_L3 + PCA_L1 + PCA_L2 + PCA_L3 + Asset_L1 + Asset_L2 + Asset_L3]) <= pulp.lpSum([(ESA_Emp*Time_Emp)*ESA_Time +
                (PCA_Emp*Time_Emp)*PCA_Time +
                (Asset_Emp*Time_Emp)*Asset_Time + 
                (ESA_PCA_Emp*Time_Emp)*ESA_Time + 
                (PCA_Asset_Emp*Time_Emp)*PCA_Time + 
                (ESA_PCA_Asset_Emp*Time_Emp)*ESA_Time])
m.solve()
print(pulp.LpStatus[m.status])
print("EMG Employee Assessment Distribution per Month")
print("Objective value: ${:,.2f} of Profit".format(round(pulp.value(m.objective))))
for variable in m.variables():
    print( "{} = {} Assessments".format(variable.name, round(variable.varValue)))

#Just messing with aesthetics at this point    
rows = []
for variable in m.variables():
    v = variable.name
    val =  round(variable.varValue)
    rows.append({"Assessments":val, "Employee Assessment Per Month":v})
    
    
df = pd.DataFrame(rows)
df.append(df.sum(numeric_only=True), ignore_index=True)
Total = (df['Assessments'].sum())
print(df)