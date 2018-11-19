# Maximum Profit Optimization

The objective of this project was to distribute environmental, property, and asset assessments for the company Environmental Management Group (EMG) based on employee level and assessment time credits to maximize profit. The following constraints applied:

- Level 1 employees can only conduct level 1 assessments.
- Level 2 employees can conduct both level 1 and level 2 assessments.
- Level 3 employees can conduct all 3 levels of assessments.
- There are only 3,200 time credits allotted per month.

A linear optimization model was built in Python to address this problem. The model displayed the following results:

- <b>Objective value: $2,621,709 of profit per month</b>
- Asset assessments: L1 employees = 150 assessments
- Asset assessments: L2 employees = 140 assessments
- Asset assessments: L3 employees = 400 assessments

- Environmental assessments: L1 employees = 200 assessments
- Environmental assessments: L2 employees = 0 assessments
- Environmental assessments: L3 employees = 0 assessments

- Property assessments: L1 employees = 120 assessments
- Property assesments: L2 employees = 100 assessments
- Property assesments: L3 employees = 0 assessments
