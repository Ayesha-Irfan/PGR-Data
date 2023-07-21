import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pywaffle import Waffle
import plotly.express as px

df = pd.read_excel('PGR_Finance_Data.xlsx')

st.set_page_config(page_title="Explore The Data", page_icon=":chart_with_upwards_trend:", layout="wide")

st.sidebar.header('Filter below to see how gender, course and mode of study affect the financial circumstance of the average PhD student:')
Gender = st.sidebar.multiselect("Select the gender:",
                                options=[n for n in df['Gender'].unique() if str(n) != 'nan'],
                                default=[n for n in df['Gender'].unique() if str(n) != 'nan'])

Mode = st.sidebar.multiselect("Select the mode of study:",
                                options=[n for n in df['Mode'].unique() if str(n) != 'nan'],
                                default=[n for n in df['Mode'].unique() if str(n) != 'nan'])

Home_International = st.sidebar.multiselect("Select the type of student:",
                                options=[n for n in df['Home_International'].unique() if str(n) != 'nan'],
                                default=[n for n in df['Home_International'].unique() if str(n) != 'nan'])

Dependents = st.sidebar.multiselect("Select the number of dependents:",
                                options=[n for n in df['Dependents'].unique() if str(n) != 'nan'],
                                default=[n for n in df['Dependents'].unique() if str(n) != 'nan'])

CDT = st.sidebar.multiselect("Select whether you would like to include CDT students:",
                                options=[n for n in df['CDT'].unique() if str(n) != 'nan'],
                                default=[n for n in df['CDT'].unique() if str(n) != 'nan'],)



df_selection = df.query("Gender == @Gender & Mode == @Mode & Home_International == @Home_International & Dependents == @Dependents & CDT == @CDT")

average_salary = 0

if 'Yes' in df_selection['CDT'].values:
    average_salary = 1760.0
    if 'No' in df_selection['CDT'].values or 'Not sure' in df_selection['CDT'].values:
        average_salary =  (1760 + 1472)/2
else:
    average_salary = 1472.0

average_foodcost = 194

st.title(':clipboard: Explore The Data')
st.markdown('##')

considered_withdrawing = [n for n in df_selection['Have you seriously considered withdrawing from the University at any stage during the current 2022/23 academic year?'] if str(n) != 'nan']
withdrawing_df = df_selection.loc[(df_selection['Have you seriously considered withdrawing from the University at any stage during the current 2022/23 academic year?']) == 1.0]
finance_withdrawing = df_selection.loc[((df_selection['Have you seriously considered withdrawing from the University at any stage during the current 2022/23 academic year?']) == 1.0) & (df_selection['Was this primarily or partly for financial reasons?'].isin(['Partly financial', 'Primarily financial']))]


total_students = len(df_selection.index)
hours_worked = round(df_selection['Approximately how many hours per week do/did you work on average?'].mean(), 2)
rent = round(df_selection['How much do you spend on your rent or mortgage per calendar month (PCM)?'].mean(), 2)
bills = round(df_selection['How much do you spend on bills (energy and water) per calendar month?'].mean(), 2)


left_column, middle_column, right_column = st.columns(3)
with left_column: 
    st.subheader('Average income per month: ')
    st.subheader(f"£ {average_salary:,}")
with middle_column: 
    st.subheader('Average bills per month: ')
    st.subheader(f"£ {bills}")
with right_column: 
    st.subheader('Average rent per month:')
    st.subheader(f"£ {rent}")

st.markdown("---")


st.subheader('Spending Breakdown')

spending_labelled = ['Remaining', 'Money spent on rent', 'Money spent on bills', 'Money spent on food']
spending_df = pd.DataFrame({'Groups': spending_labelled, 'Count': [(average_salary-(bills + rent + average_foodcost)), rent, bills, average_foodcost]})   
second_job = [n for n in df_selection['In the current academic year (2022/23), have you undertaken any employment to supplement your income?'] if str(n) != 'nan']     
reds = ['rgb(214,96,77)','rgb(253,219,199)', 'rgb(244,165,130)',  'rgb(229,131,104)', 'rgb(255,195,143)' ]
#lighter_reds = reds.remove('rgb(178,24,43)')
fig4 = px.pie(spending_df, values='Count', names='Groups', color_discrete_sequence=reds)
st.plotly_chart(fig4)

average_pay = np.round(average_salary-(bills + rent + average_foodcost), 2)
if average_pay < 0:
    st.subheader('Therefore, the average PhD student is £' + str(np.absolute(average_pay)) + ' short per month, they need supplementary income just to pay for their bills, rent and food.')
else: 
    st.subheader('Therefore, the average PhD student has just £' + str(average_pay) + ' left over per month after paying for their bills, rent and for food.')

st.markdown("---")
#WAFFLE DIAGRAM
lith_dict = {'LITH': ['Considered', 'Did not consider'],
             'Well1': [len(withdrawing_df)/total_students, (total_students-len(withdrawing_df))/total_students]}

lith_data_df = pd.DataFrame.from_dict(lith_dict)

colours = ['#E53935', '#827D7D' 
           ]

plot_labels = [f'{i} ({str(j)} %)' for i,j in zip(lith_data_df.LITH, 
                                                    lith_data_df.Well1)]
fig0 = plt.figure(FigureClass=Waffle, rows=2, columns = 12, 
                 values=list(lith_data_df['Well1']),
                 colors=colours,
                 labels=plot_labels, 
                icons='person',
                font_size='20',
                 starting_location='NW',
      
    block_aspect_ratio=1.2
                 )

fig0.axes[0].get_legend().remove()

st.pyplot(fig0, use_container_width=True)
st.subheader('On average, ' + '**' + str(int(round(considered_withdrawing.count(1.0)/len(considered_withdrawing), 2)*100)) + '%** ' + 'of PhD students have seriously considered :red[withdrawing] from their studies.')
st.subheader( 'Out of these students, **' + str(int(round(len(finance_withdrawing)/len(withdrawing_df), 2)*100)) + '%' +  '** of these students stated that they were considering withdrawing due to their :red[financial situation].')

st.markdown('---')
importance_of_job = df_selection.groupby(by=['IMPORTANCE_OF_JOB']).count()[['REDACTED']]
average_rating = round(df_selection['IMPORTANCE_OF_JOB'].mean(), 2)
neater_df = pd.DataFrame({'Rating': importance_of_job['REDACTED'].index.values, 'Count': importance_of_job['REDACTED'].values})
fig = px.bar(neater_df, x="Rating", y="Count", color="Rating", barmode="relative")
fig.update_traces(marker_color='#E53935', marker_line_color='rgb(38,35,35)', marker_line_width=0.05, opacity=0.7)
#fig1 = px.bar(neater_df, x="Rating", y="Count"),
st.subheader(str(int((second_job.count(1.0)/total_students)*100)) + '% students supplement their income with a second job. The average student works ' + str(hours_worked) + ' additional hours per week during term-time on top of their PhD.')

st.plotly_chart(fig)

st.subheader('Here, students have rated the importance of their second job during term-time. A rating of 10 means that it was essential for the student to have a second job, the average rating was ' + str(average_rating) + '.')

st.subheader('When asked what the motivation of taking on a second job was, the following were the responses:')

phd_related = [n for n in df_selection['To help pay the costs of books, study materials, field trips etc.'] if str(n) == 'To help pay the costs of books, study materials, field trips etc.']
living_related = [n for n in df_selection['To pay for essential living costs (food, rent, fuel bills etc.)'] if str(n) == 'To pay for essential living costs (food, rent, fuel bills etc.)']
comfort_related = [n for n in df_selection['To have a more comfortable life while studying'] if str(n) == 'To have a more comfortable life while studying']
saving_related = [n for n in df_selection['To save for a specific purpose (e.g. a holiday or a car)'] if str(n) == 'To save for a specific purpose (e.g. a holiday or a car)']
family_related = [n for n in df_selection['To support family (e.g. your children)'] if str(n) == 'To support family (e.g. your children)']
experience_related = [n for n in df_selection['To gain employment experience'] if str(n) == 'To gain employment experience']
studentdebt_related = [n for n in df_selection['To avoid or minimise student debt (if you have any debt)'] if str(n) == 'To avoid or minimise student debt (if you have any debt)']
hobbies_related = [n for n in df_selection['To enable you to do other things outside of university life (e.g. travel, have hobbies, etc.)'] if str(n) == 'To enable you to do other things outside of university life (e.g. travel, have hobbies, etc.)']
health_related = [n for n in df_selection['Health-related costs'] if str(n) == 'Health-related costs']
other_related = [n for n in df_selection['Other'] if  (type(n)) == str]

reasons_labels = ['PhD materials and field trips', 'For Essential Living Costs', 'To Live Comfortably', 'For Savings', 'For Helping Family', 'For Job Experience', 'Repaying Debt', 'For Hobbies', 'Health-related Costs', 'Other reasons']
reasons_count = [len(phd_related), len(living_related), len(comfort_related), len(saving_related), len(family_related), len(experience_related), len(studentdebt_related), len(hobbies_related), len(health_related), len(other_related)]

reasons_dict = {}

for i in range(len(reasons_labels)):
    reasons_dict.update({reasons_labels[i]: reasons_count[i]})
#descending_dict = sorted(reasons_dict, reverse=True)
sorted_dict = dict(sorted(reasons_dict.items(), key=lambda x:x[1], reverse=True))

reasons_df = pd.DataFrame({'Motivation': sorted_dict.keys(), 'Count': sorted_dict.values()})

colors = px.colors.sequential.YlOrRd_r
colors.append('#fffed9')
figh = px.bar(reasons_df, x="Count", y="Motivation", orientation='h', color='Motivation', color_discrete_sequence=colors )
figh.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
st.plotly_chart(figh)

st.markdown('##')
st.markdown("---")

total_students = len(df_selection.index)
hours_worked = round(df_selection['Approximately how many hours per week do/did you work on average?'].mean(), 2)
rent = round(df_selection['How much do you spend on your rent or mortgage per calendar month (PCM)?'].mean(), 2)
bills = round(df_selection['How much do you spend on bills (energy and water) per calendar month?'].mean(), 2)

st.subheader('Distribution of additional hours worked')
under_5 = 0
from_5_to_15 = 0
from_15_to_25 = 0
from_25_to_35 = 0
over_35 = 0

hours_df = df_selection.groupby(by=['Approximately how many hours per week do/did you work on average?']).count()[['REDACTED']]
neater_df2 = pd.DataFrame({'Hours': hours_df['REDACTED'].index.values, 'Count': hours_df['REDACTED'].values})

for hours in neater_df2['Hours']:
    if hours < 5.0:
        under_5 += 1
    elif hours < 15 and hours >= 5:
        from_5_to_15 += 1
    elif hours < 25 and hours >= 15:
        from_15_to_25 += 1
    elif hours < 35 and hours >= 25:
        from_25_to_35 += 1
    elif hours >= 35:
        over_35 += 1


hours_labelled = ['Under 5 hours', '5-15 hours', '15-25 hours', '25-35 hours', 'over 35 hours']
new_df = pd.DataFrame({'Groups': hours_labelled, 'Count': [under_5, from_5_to_15, from_15_to_25, from_25_to_35, over_35]})             
#fig3 = plt.figure(figsize =(10, 7))
#plt.pie([under_5, from_5_to_15, from_15_to_25, from_25_to_35, over_35], labels = cars)

fig3 = px.pie(new_df, values='Count', names='Groups', color_discrete_sequence=reds)
st.plotly_chart(fig3)
#st.bar_chart(importance_of_job['REDACTED'].values)
fig2 = px.line(neater_df2, x="Hours", y="Count", render_mode="svg", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig2)
st.subheader('Over 50' + '%' + ' of PhD students work 15 or more hours on top of their PhD hours. Nearly 25' + '%' + ' work a full-time job alongside their PhD.')

st.markdown('---')

l_column, r_column = st.columns(2)
with l_column: 
    st.subheader('Students included in this demographic: ')
    st.subheader(f"{total_students:,}")
with r_column: 
    st.subheader('Total students included in study:')
    st.subheader("503")

st.markdown('---')