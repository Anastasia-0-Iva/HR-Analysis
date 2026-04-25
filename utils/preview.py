import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


df = pd.read_excel(r'C:\Users\Анастасия\OneDrive\Desktop\[SW.BAND] Hr data_satisfaction.xlsx')

columns = df.columns.tolist() # Колонки в документе

# Гендерное распределение
gender = df['Gender'].unique() # ['Female', 'Male']
count_gender_women = list(df['Gender']).count('Female') # 588
count_gender_men = list(df['Gender']).count('Male') # 882

# Средний возраст
mean_age = round(df['Age'].mean()) # 37
mean_age_women = round(df[df['Gender'] == 'Female']['Age'].mean()) # 37
mean_age_men = round(df[df['Gender'] == 'Male']['Age'].mean()) # 37

# Отделы и позиции
departments = df['Department'].unique() # 'Sales', 'Research & Development', 'Human Resources'
departments_count = df['Department'].value_counts() # Кол-во сотрудников в отделах
role = df['JobRole'].unique() # 'Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Healthcare Representative', 'Manager', 'Sales Representative', 'Research Director', 'Human Resources'
role_count = df['JobRole'].value_counts() # Кол-во сотрудников на разных позициях

# Финансы
avg_income = round(df['MonthlyIncome'].mean(), 1) # Средняя зп по компании 6502.9
departments_income = df.groupby('Department')['MonthlyIncome'].mean().round(2) # Средняя зп по отделам. {'Sales': 6959.17, 'Research & Development': 6281.25, 'Human Resources': 6654.51}
role_income = df.groupby('JobRole')['MonthlyIncome'].mean().round(2) # Средняя зп по должностям


# Производительность труда
performance_ration = round(df['PerformanceRating'].mean(), 1) # Общая - 3.2
departments_performance_ration = df.groupby('Department')['PerformanceRating'].mean() # По отделам (у всех 3)
role_performance_ration = df.groupby('JobRole')['PerformanceRating'].mean() # По должностям (варьируется от 3 до 4)


# Как долго в среднем работают
avg_experience = round(df['YearsAtCompany'].mean()) # 7 лет
avg_experience_departments = df.groupby('Department')['YearsAtCompany'].mean().round() # По отделам (все 7 лет)
avg_experience_role = df.groupby('JobRole')['YearsAtCompany'].mean().round() # По должностям (от 3 до 14)


#____________Основные показатели для выявления удовлетворённости сотрудников_________

e_satisfaction = dict(zip(df['EmployeeNumber'], df['EnvironmentSatisfaction'])) # Словарь типа {'id': Удовлетворенность окружающей средой}
avg_e_satisfaction = round(df['EnvironmentSatisfaction'].mean(), 2) # Среднее - 2.72

j_satisfaction = dict(zip(df['EmployeeNumber'], df['JobSatisfaction'])) # Словарь типа {'id': Удовлетворенность работой}
avg_j_satisfaction = round(df['JobSatisfaction'].mean(), 2) # Среднее - 2.73

r_satisfaction = dict(zip(df['EmployeeNumber'], df['RelationshipSatisfaction'])) # Словарь типа {'id': Удовлетворенность отношениями}
avg_r_satisfaction = round(df['RelationshipSatisfaction'].mean(), 2) # Среднее - 2.71

wl_balance = dict(zip(df['EmployeeNumber'], df['WorkLifeBalance'])) # Словарь типа {'id': Баланс рабочей жизни}
avg_wl_balance = round(df['WorkLifeBalance'].mean(), 2) # Среднее - 2.76

#____________________________________________________________________________________

# Соотношение сотрудников по уровню общей удовлетворённости

perfect_satisfaction = [] # Сотрудники с высшей оценкой удовлетворённости (0)
normal_satisfaction = [] # Сотрудники со средней оценкой удовлетворённости (164)
low_satisfaction = [] # Сотрудники с низкой оценкой удовлетворённости (1306)

overall_satisfaction_level = {} # Словарь типа {'id': ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']}

for index, row in df.iterrows():
    key = row['EmployeeNumber']
    value = [row['EnvironmentSatisfaction'], row['JobSatisfaction'], row['RelationshipSatisfaction']]
    overall_satisfaction_level[key] = value

for key, value in overall_satisfaction_level.items():
    if sum(value) == 15:
        perfect_satisfaction.append(key)
    if sum(value) >= 11:
        normal_satisfaction.append(key)
    else:
        low_satisfaction.append(key)


procent_perfect_sf = (len(perfect_satisfaction) / len(df['EmployeeNumber'])) * 100 # 0.0%
procent_normal_sf = round((len(normal_satisfaction) / len(df['EmployeeNumber'])) * 100, 1) # 11.2%
procent_low_sf = round((len(low_satisfaction) / len(df['EmployeeNumber'])) * 100, 1) # 88.8%


# Соотношение отделов по уровню общей удовлетворённости
perfect_satisfaction_departament = Counter()
normal_satisfaction_departament = Counter()
low_satisfaction_departament = Counter()

departament_statisfection = {} # Словарь типа {'Department': {'id: ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']}}
for index, row in df.iterrows():
    key = row['Department']
    value = overall_satisfaction_level
    departament_statisfection[key] = value


# Кол-во вхождений по отделам
for index, row in df.iterrows():
    key = row['Department']
    value = row['EnvironmentSatisfaction'] + row['JobSatisfaction'] + row['RelationshipSatisfaction']
    if value == 15:
        perfect_satisfaction_departament[key] += 1
    elif value >= 11:
        normal_satisfaction_departament[key] += 1
    else:
        low_satisfaction_departament[key] += 1


# Соотношение должностей по уровню общей удовлетворённости
perfect_satisfaction_role = Counter()
normal_satisfaction_role = Counter()
low_satisfaction_role = Counter()

role_statisfaction = {} # Словарь типа {'JobRole': {'id: ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']}}
for index, row in df.iterrows():
    key = row['JobRole']
    value = overall_satisfaction_level
    role_statisfaction[key] = value

# Кол-во вхождений по должностям
for index, row in df.iterrows():
    key = row['JobRole']
    value = row['EnvironmentSatisfaction'] + row['JobSatisfaction'] + row['RelationshipSatisfaction']
    if value == 15:
        perfect_satisfaction_role[key] += 1
    elif value >= 11:
        normal_satisfaction_role[key] += 1
    else:
        low_satisfaction_role[key] += 1

# Корреляции между уровнями оценки и зп

corr_es = df['EnvironmentSatisfaction'].corr(df['MonthlyIncome']) # зп -> Удовлетворенность окружающей средой (-0.00)
corr_js = df['JobSatisfaction'].corr(df['MonthlyIncome']) # зп -> Удовлетворенность работой (-0.00)
corr_rs = df['RelationshipSatisfaction'].corr(df['MonthlyIncome']) # зп -> Удовлетворенность отношениями (0.02)

#---------------------ВИЗУАЛИЗАЦИЯ------------------------------

# Гендерное соотношение коллектива (Круговая диаграмма)
#labels = ['Мужчины', 'Женщины']
#value = [count_gender_men, count_gender_women]
#colors = ['b', 'm']
#plt.pie(value, labels=labels, colors=colors, autopct='%1.0f%%')
#plt.title('Гендерное соотношение коллектива')
#plt.show()

# Гендерный средний возраст (Скрипичная диаграмма)
#sns.violinplot(x='Gender', y='Age', data=df, palette=['m', 'b'])
#plt.title('Гендерный средний возраст')
#plt.show()

# Кол-во сотрудников в отделах (Столбчатая диаграмма)
#categories = ['Research & Development', 'Sales', 'Human Resources']
#value = departments_count
#plt.bar(categories, value, color=['yellow', 'orange', 'red'])
#plt.title('Кол-во сотрудников в отделах')
#plt.show()

# Кол-во сотрудников на разных позициях (Горизонтальный столбчатый график)
#categories = ['Sal Exec', 'Res Sci', 'Lab Tech', 'Manuf Dir', 'HC Rep', 'Manager', 'Sales Rep', 'Res Dir', 'HR']
#value = role_count
#plt.barh(categories, value, color='black')
#plt.title('Кол-во сотрудников на разных позициях')
#plt.show()

# Зп по отделам (Столбчатая диаграмма)
#categories = ['Research & Development', 'Sales', 'Human Resources']
#value = departments_income
#plt.bar(categories, value, color=['yellow', 'orange', 'red'])
#plt.title('Средняя зп по отделам')
#plt.show()

# Зп по должностям (Горизонтальный столбчатый график)
#categories = ['Sal Exec', 'Res Sci', 'Lab Tech', 'Manuf Dir', 'HC Rep', 'Manager', 'Sales Rep', 'Res Dir', 'HR']
#value = role_income
#plt.barh(categories, value, color='#8DA47E')
#plt.title('Средняя зп по должностям')
#plt.show()

# Производительность труда (отделы) / (Горизонтальный столбчатый график)
#categories = ['Res&Dev', 'Sales', 'Hum Res']
#value = departments_performance_ration
#plt.barh(categories, value, color=['yellow', 'orange', 'red'])
#plt.title('Производительность труда каждого отдела')
#plt.show()

# Производительность труда (должности) / (Горизонтальный столбчатый график)
#categories = ['Sal Exec', 'Res Sci', 'Lab Tech', 'Manuf Dir', 'HC Rep', 'Manager', 'Sales Rep', 'Res Dir', 'HR']
#value = role_performance_ration
#plt.barh(categories, value, color='#264653')
#plt.title('Производительность труда для каждой должности')
#plt.show()

# Годы в компании - отделы (среднее) / (Линейный график)
#categories = ['Research & Development', 'Sales', 'Human Resources']
#value = avg_experience_departments
#plt.errorbar(categories, value, color='gray')
#plt.title('Стаж работы в компании (Отделы)')
#plt.show()

# Годы в компании - должности (среднее) / (Столбчатая диаграмма)
#categories = ['Sal Exec', 'Res Sci', 'Lab Tech', 'Manuf Dir', 'HC Rep', 'Manager', 'Sales Rep', 'Res Dir', 'HR']
#value = avg_experience_role
#plt.bar(categories, value, color='#F4A261')
#plt.title('Стаж работы в компании (Должности)')
#plt.xticks(rotation=35)
#plt.show()

# Сотрудники по уровню удовлетворённости (Ящик с усами)
#labels = ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']
#value = df[['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']]
#plt.boxplot(value, labels=labels)
#plt.title('Уровень удовлетворенности в коллективе')
#plt.show()

# Сравнение отделов по уровню удовлетворенности / (Столбчатая диаграмма)
department_stf = df.groupby('Department')[['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']].sum().sum(axis=1) # Удовлетворенность каждого отдела

#categories = ['Human Resources', 'Research & Development', 'Sales']
#value = department_stf
#plt.bar(categories, value, color=['yellow', 'orange', 'red'])
#plt.title('Сравнение отделов по уровню удовлетворенности')
#plt.show()


# Сравнение должностей по уровню удовлетворенности / (Столбчатая диаграмма)
role_stf = df.groupby('JobRole')[['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']].sum().sum(axis=1) # Удовлетворенность каждой должности

#categories = ['Sal Exec', 'Res Sci', 'Lab Tech', 'Manuf Dir', 'HC Rep', 'Manager', 'Sales Rep', 'Res Dir', 'HR']
#value = role_stf
#plt.bar(categories, value, color='#C4A4A4')
#plt.title('Сравнение должностей по уровню удовлетворенности')
#plt.xticks(rotation=35)
#plt.show()


# Всевозможные уровни удовлетворенности (процент) / (Столбчатая диаграмма)
categories = ['perfect', 'normal', 'low']
value = [procent_perfect_sf, procent_normal_sf, procent_low_sf]
plt.bar(categories, value)
plt.title('Уровни удовлетворенности (в процентах)')
plt.show()

