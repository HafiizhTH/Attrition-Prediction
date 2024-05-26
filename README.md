
## Submission 1: Solving Human Resources Problems

## Business Understanding

Jaya Jaya Maju is a multinational company that has been established since 2000. It has more than 1000 employees spread across the country. 

### Business Problems

Jaya Jaya Maju Company, although it has grown into a fairly large company, still faces challenges in managing its employees. This results in a high attrition rate of more than 10%. So, this project focuses on efforts to reduce the attrition rate.

Because, if the attrition rate problem is not addressed immediately, it is feared that more and more employees will leave the company. This will impact the company's operations and require new recruitment efforts to fill the job positions left behind.

### Project Scope

The focus of this project is to solve business problems with the following steps: 
1. Identify the factors that affect the high attrition rate.   
2. Create a business dashboard to monitor and provide insights to the Human Resources Department regarding the problem of high attrition rate.   
3. Build a machine learning model to help the Human Resources Department predict employee data, so that they can take proactive action against employees who are indicated to be leaving the company.

### Preparation

The dataset used in this project is sourced from dicoding. You can download the dataset by clicking the following link: [click here](https://github.com/dicodingacademy/dicoding_dataset/tree/main/employee).

To get started with our project, follow these installation steps:
- Clone the project repository from our gitHub repository:
```
git clone https://github.com/HafiizhTH/Human_Resources.git
```

Setup environment - Anaconda:
- Open Anaconda Terminal
- Run the following command to create a new environment:
```
conda create --name main-ds python=3.11
```
- Activate the virtual environment by running the following command:
```
conda activate main-ds
```
- Install the library to use:
```
pip install -r requirements.txt
```
Run streamlit app
```
Streamlit run app.py
```

## Business Dashboard

A business dashboard was created to monitor the various factors that influence the attrition rate. The dashboard provides comprehensive data visualization, enabling the human resources department to identify trends and make decisions based on the insights gained. If you would like to access the dashboard [click here](https://lookerstudio.google.com/u/0/reporting/3c9fe1a9-6b15-4bb8-9451-fd2746127e5c/page/n3Q0D).

![image](https://github.com/HafiizhTH/Human_Resources/assets/96015981/6b06a268-d566-4d4e-9f3b-8b9890a5a82a)

In the Dashboard visualization to be able to analyze employees in the company jaya jaya maju there are several features:
- **Filter and Data Control**: serves to facilitate the search and analysis of specific data based on date, department, jobrole, and employee status.
- **View Total**: serves to see the number and average of employee attrition, employee performance, monthly rates, daily rates
- **Pie Chart**: Used to see the comparison and percentage of data based on gender, marital status, job level, department, work life balance, employee performance, employee overtime.
- **Bar Chart**: Used to view the distribution of data based on education level, field of education, work experience, age, distance of residence, length of working in the company, employee participation, length of working with manager, employee satisfaction.

## Testing Model

If you want to try using the model to predict employee attrition. [click here](https://attrition-prediction.streamlit.app/)

![image](https://github.com/HafiizhTH/Human_Resources/assets/96015981/b083eb07-1ba8-4c41-a4ae-9ac455c1e75c)

In the attrition prediction model testing display, there are several pages as follows:
- **Prediction**: There are 2 ways that you can use, namely single-predict (manual input) or multiple-predict (dataset upload).
- **Employee Information**: There are 2 ways you can use to view data that has been uploaded, namely viewing from descriptive data or visualization data.
- **FAQ**: Contains a list of questions and answers to help you run this application.

## Conclusion

Based on data analysis, some of the factors that could potentially affect the attrition rate are:
- Very high rate of employees working overtime.
- Low monthly income and salary increases.  

If viewed based on the characteristics of employees who experience attrition, such as:
- **Number of Employees Leaving**: A total of 179 employees have left out of a total of 1058 employees.
- **Gender**: Employees who left were dominated by men as many as 108 people, compared to women as many as 71 people.
- **Job Level**: The most employees who left were at the basic level, totaling 108 people.
- **Department**: The department with the highest attrition rate is Research & Development, with 107 people leaving, compared to other departments.
- **Age**: Most employees who left were in the age range of 30-40 years old.
- **Job Position**: The position with the highest attrition rate is Laboratory Technician, with 49 people leaving.
- **Employees Working Overtime**: 54% of employees who left were those who frequently worked overtime.
- **Work-Life Balance**: Employees who left were dominated by those who had an excellent work-life balance with 94 people. In addition, employees with good, outstanding, and low work-life balance were 45, 22, and 18 respectively.
- **Distance of Residence**: A total of 72 employees who left had a residential distance to the office of 0-5 km.
- **Total Length of working**: Employees with a total tenure of 0-5 years are more likely to leave, with a total of 121 people, compared to those who worked for 11-20 years, 6-10 years, and >20 years.
- **Engagement in Work**: Employees with high engagement had a higher percentage of exits at 92 compared to medium, low, and very high engagement.
- **Work Environment Satisfaction**: Employees who left tended to have high satisfaction with the work environment at 62.
- **Work Relationship Satisfaction**: Employees who left tended to have very high job relationship satisfaction (52 people). For employees with high and low job relationship satisfaction, the percentage is not much different from very high job relationship satisfaction.

### Recomandation

- **Overtime Work Policy Evaluation**: Review the company's policy on overtime work. If possible, try to limit excessive overtime work, as it can lead to fatigue and decreased productivity, as well as cause employee dissatisfaction. 
- **Compensation System Review**: Review the company's salary structure and salary increase policy. Ensure that employees feel valued and rewarded according to their contribution and performance. If possible, consider adjusting salary policies or providing additional incentives for employees who do a good job.
- **Employee Development Programs**: Implement training and development programs that can help employees improve their skills and abilities. This can not only improve employee performance, but also increase their attachment to the company.
- **Balanced Work Culture**: Build a work culture that encourages work-life balance. Implement work environments such as working time flexibility, working from home, and flexible leave to help reduce burnout and stress associated with their work.
- Improve communication between management and employees to better understand their needs and expectations.
- **Monitor and Assess Changes**: After implementing changes, it is important to regularly monitor and evaluate their impact. If possible, conduct surveys or interviews with employees to get feedback on the effectiveness of the changes that have been made.