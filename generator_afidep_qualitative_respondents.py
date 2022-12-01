#Author: John Omoluabi (Data Analyst Intern)
#Organisation: Akena Associates

# import dependencies
import pandas as pd
import numpy as np
from dataset_dir import stata_dir
from dataset_dir import excel_dir
import os
import seaborn as sns
import datetime

# pandas configuration
pd.io.formats.excel.ExcelFormatter.header_style = None
pd.options.display.max_rows = None
pd.options.display.max_columns = None

#today's date
date_today= datetime.date.today()

# import survey responses
data=pd.read_stata(stata_dir()+"Teamup_Women_Dataset_cleanv4.dta",convert_categoricals=False)

#import respondent names dictionary
respondent_names=pd.read_excel(excel_dir()+"teamup_women_name.xlsx")

# import fieldworker names dictionary
interviewer_names=pd.read_excel(excel_dir()+"teamup_interviewers.xlsx")

# append respondent names to data
data['respondent_names']=respondent_names['res_name']
data['state']="Adamawa"




#import profile reports
consistent_user=pd.read_excel(excel_dir()+"AFIDEP_user_profiles_adamawa_JO_29Nov2022_v1.xlsx",sheet_name="Consistent User(more frequent)")
concurrent_user=pd.read_excel(excel_dir()+"AFIDEP_user_profiles_adamawa_JO_29Nov2022_v1.xlsx",sheet_name="Concurrent User(1mth & 2-6mths)")
stopper=pd.read_excel(excel_dir()+"AFIDEP_user_profiles_adamawa_JO_29Nov2022_v1.xlsx",sheet_name="Stoppers")
switcher=pd.read_excel(excel_dir()+"AFIDEP_user_profiles_adamawa_JO_29Nov2022_v1.xlsx",sheet_name="Switchers")

#import level3 names dictionary
choices=pd.read_excel(excel_dir()+"lgas.xlsx")


# new dataframes for respondent ids across profiles 
s1=consistent_user["Respondent ID"]
s2=concurrent_user["Respondent ID"]
s3=stopper["Respondent ID"]
s4=switcher["Respondent ID"]

# define output table columns as lists
ids=[]
resp_name=[]
prof=[]
husband=[]
phone1=[]
phone2=[]
lga=[]
ward=[]
head=[]
gpslat=[]
gpslong=[]
gpsalt=[]
gpsacc=[]
interviewer=[]
date_of_interview=[]
good_time=[]
reinterview=[]
husband_concent=[]
observation=[]

for i in s1:
    if(str(type(i))!="<class 'float'>"):
        ids.append(i)
for i in s2:
    if(str(type(i))!="<class 'float'>"):
        ids.append(i)
for i in s3:
    if(str(type(i))!="<class 'float'>"):
        ids.append(i)
for i in s4:
    if(str(type(i))!="<class 'float'>"):
        ids.append(i)
        
        
for i in ids:
    if(i in s1.values):
        prof.append("Consistent User")
    elif(i in s2.values):
        prof.append("Concurrent User")
    elif(i in s3.values):
        prof.append("Stopper")
    else:
        prof.append("Switcher")
        
# display(y)
for i in ids:
    x=data[data['resp_select']==i]['husband_participate']
    husband.append(x.iloc[0])
# display(z)
for i in ids:
    x=data[data['resp_select']==i]['respondent_names']
    resp_name.append(x.iloc[0])
    
for i in ids:
    x=data[data['resp_select']==i]['phn_1st']
    phone1.append(x.iloc[0])

for i in ids:
    x=data[data['resp_select']==i]['phn_2nd']
    x=x.iloc[0]
    x=str(x)
    
    phone2.append(x)
for i in ids:
    x=data[data['resp_select']==i]['level3']
    x=x.iloc[0]
    x=int(x)
    x=choices[choices["code"]==x]["decode"]
    x=x.iloc[0]
    lga.append(x)

for i in ids:
    x=data[data['resp_select']==i]['ward']
    x=x.iloc[0]
    x=str(x)
    
    ward.append(x)
for i in ids:
    x=data[data['resp_select']==i]['husband_name']
    x=x.iloc[0]
    x=str(x)
    
    head.append(x)
for i in ids:
    x=data[data['resp_select']==i]['gpslatitude']
    gpslat.append(x.iloc[0])
for i in ids:
    x=data[data['resp_select']==i]['gpslongitude']
    gpslong.append(x.iloc[0]) 
for i in ids:
    x=data[data['resp_select']==i]['gpsaltitude']
    gpsalt.append(x.iloc[0]) 
for i in ids:
    x=data[data['resp_select']==i]['gpsaccuracy']
    gpsacc.append(x.iloc[0]) 
for i in ids:
    x=data[data['resp_select']==i]['your_name']
    interviewer.append(x.iloc[0])   
for i in ids:
    x=data[data['resp_select']==i]['provide_phn']
    reinterview.append(x.iloc[0])
for i in ids:
    x=data[data['resp_select']==i]['today']
    date_of_interview.append(x.iloc[0])  
for i in ids:
    x=data[data['resp_select']==i]['husband_schedule']
    x=x.iloc[0]
    good_time.append(x[-11:])
for i in ids:
    x=data[data['resp_select']==i]['husband_participate']
    husband_concent.append(x.iloc[0])      
for i in ids:
    x=data[data['resp_select']==i]['observation']
    observation.append(x.iloc[0])


selection=pd.DataFrame({"Respondent ID":ids,
              "Respondent Name":resp_name,
              "Profile":prof,
              "State":"Adamawa",
              "LGA":lga,
              "Ward":ward,
              "Phone no1":phone1,
              "Phone no2":phone2,
              "Consent for re-interview":reinterview,
              "Concent for husband's Interview":husband_concent,
              "Respondent's husband":head,
              "Good time for Husband Interview":good_time,
              "GPS Latitude":gpslat,
              "GPS Longitude":gpslong,
              "GPS Altitude":gpsalt,
              "GPS Accuracy":gpsacc,
              "Interviewer Name":interviewer,
              "Date of Interview":date_of_interview,
              "Observations":observation,
                       
                       })

selection = selection.replace(1,'Yes')
selection = selection.replace(0,'No')
temp=[]
for i in selection['Interviewer Name']:
    if i in interviewer_names['id']:
        x=interviewer_names[interviewer_names['id']==i]['name']
        temp.append(x.iloc[0])
selection['Interviewer Name']=temp
selection

#table summary
#summary feature

# replace missing values with whitespace
selection.replace("nan",np.nan,inplace=True)
selection.replace(np.nan,'',inplace=True)

s1="Consistent User"
s2="Concurrent User"
s3="Stopper"
s4="Switcher"

total_resp=data.shape[0]
total_selected=selection.shape[0]
total_consistent=selection[selection['Profile']==s1].shape[0]
total_concurrent=selection[selection['Profile']==s2].shape[0]
total_stopper=selection[selection['Profile']==s3].shape[0]
total_switcher=selection[selection['Profile']==s4].shape[0]

a=[]

def summary_engine(tag,top,bottom):
    _=round((top/bottom)*100,2)
    b=[tag,top,bottom,_]
    a.append(b)
    # print(f'{tag}==>{top}/{bottom}, {_}%')
    
summary_engine("Selected",total_selected,total_resp)
summary_engine(s1,total_consistent,total_selected)
summary_engine(s2,total_concurrent,total_selected)
summary_engine(s3,total_stopper,total_selected)
summary_engine(s4,total_switcher,total_selected)
pd.DataFrame(a,columns=["","N","Total","%"])
