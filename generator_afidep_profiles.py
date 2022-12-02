import pandas as pd
import numpy as np
from dataset_dir import stata_dir
from dataset_dir import excel_dir
import os
import seaborn as sns
from pandas_profiling import ProfileReport
import datetime
date_today= datetime.date.today()


pd.io.formats.excel.ExcelFormatter.header_style = None

pd.options.display.max_rows = None
pd.options.display.max_columns = None

r=pd.read_stata(stata_dir()+"Teamup_Women_Dataset_cleanv4.dta",convert_categoricals=False)
strats={1:'Withdrawal',2:'Abstinence/Rhythm',3:'Counting Plus',
        4:'Concoctions',5:'Herbs',7:'LAM',8:'Non-LAM',
        9: 'Standard Days',12:'Emergency Contraceptive',
        13:'Female Condom',14:'Male Condom',15:'Pill',
        16:'Implants',17:'Injectables',18:'IUD',19:'Male Sterilization',20:'Female Sterilization'}

#consistent user
res_list=[]


def conv(x):
    if x==1:
        return "All the time"
    elif x==2:
        return "Most of the time"
    elif x==3: 
        return "Some of the time"
    
    

for i in [1,2,3,4,5,7,8]:
    # print(strats[i])
    _=r[
        (r[f'q211q216']==1)&
        (r[f'q211_cal{i}']==1)&
        (r[f'q216_cal{i}']==1)&
        (r[f'q220g_{i}']==0)&
        (r[f'q220d_{i}']==1)
        # (r[f'q220f_{i}']==0)
        
    
    ][['resp_select',
       'q211q216', 
       'q220',
       'q221',
       'q222',
       'q223',
       f'q220g_{i}',
       f'strat_combine{i}',
       'q216_ac_count',
       'q211a_c_count',
       f'q211_cal{i}',
       f'q216a_cal{i}',
       f'q216_cal{i}',
       'q210',
       f'q211a_{i}',
       f'q211c_{i}',
       f'q209a',
       f'q209b',
       f'q215_{i}',
       f'q216c_{i}',
       f'q216_{i}',
       f'q216c_cal{i}',
       f'q220a_{i}',
       f'q220d_{i}']]
    _[f"q211q215_cal{i}"]=0
    _[f"q211q216_cal{i}"]=0
    _[f"q215q216c_cal{i}"]=0
    _[f"q216a_calq216c_cal{i}"]=0
    _["index_strategy"]=strats[i]
    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
    j=_[[
        'index_strategy',
        'resp_select',
        f'q220g_{i}',
        'q211q216',
        f'q215q216c_cal{i}',
        f"q216a_calq216c_cal{i}",
        'q211a_c_count',
        'q216_ac_count',
        'q209a',
        'q209b',
        'q210',
        f'q220a_{i}',
        f'q211_cal{i}',
        f'q216_cal{i}'
        
    ]]
    j.columns=range(j.shape[1])
  
    res_list.append(j)

consistent_user=pd.concat([res_list[0],
res_list[1],
res_list[2],
res_list[3],
res_list[4],
res_list[5],
res_list[6]
])
consistent_user.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220-q223)a_x',
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]
consistent_user["Used Index Strategy with other strategy"].replace(0,"No")
consistent_user["Used Index Strategy with other strategy"].replace(1,"Yes")
consistent_user["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in consistent_user["Used more than 1 strategy"]]
consistent_user["Used Index Strategy with other strategy"]=["Yes" if x==1 else "No" for x in consistent_user["Used Index Strategy with other strategy"]]
consistent_user["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in consistent_user["Used index strategy throughout 6 month period(q211 and q215)"]]
consistent_user["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in consistent_user["Used index strategy throughout 6 month period(q211 and q216)"]]
consistent_user["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in consistent_user["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
consistent_user["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in consistent_user["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
consistent_user["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in consistent_user["Used any strategy in the last one month (q209a)"]]
consistent_user["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in consistent_user["Used any strategy in the last 2-6 month (q209b)"]]
consistent_user["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in consistent_user["Used any strategy in the last 2-6 months (q210)"]]

consistent_user["How often have you used this strategy in the past 6 months (q220-q223)a_x"]=[conv(x) if x is not None else x for x in consistent_user["How often have you used this strategy in the past 6 months (q220-q223)a_x"]]
consistent_user["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in consistent_user["Used index stragegy in last 1 month (q211_calx=1)"]]
consistent_user["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in consistent_user["Used index stragegy in last 2-6 months (q216_calx=1)"]]



# consistent_user
consistent_user.to_excel(excel_dir()+"consistent_user_profile.xlsx",index=False)

#concurrent user
res_list=[]
two_digit_strats={12:'Emergency Contraceptive',13:'Female Condom',14:'Male Condom',15:'Pill',16:'Implants',17:'Injectables',18:'IUD',19:'Male Sterilization',20:'Female Sterilization'}
for q in ['220','221','222','223']: 
    for i in [1,2,3,4,5,7,8]:
        # print(strats[i])
        for j in [1,2,3,4,5,7,8,9,12,13,14,15,16,17,18,19,20]:
            question=q
            c=f'q{question}h_{i}{j}'
            if len(c)>8:
                c=c[-4:]
                if((c[0])=="_")&(int(c[-2:]) in list(two_digit_strats.keys())):
                    try:
                        # print(r[f'q220h_{i}{j}'].value_counts(dropna=False))

                        _=r[
                            (r[f'q{question}h_{i}{j}']==1)&
                            (r[f'q{question}d_{i}']==1)
                        
                        
                        ][['resp_select',
                           'q211q216', 
                           'q220',
                           'q221',
                           'q222',
                           'q223',
                           f'q220g_{i}',
                           f'strat_combine{i}',
                           'q216_ac_count',
                           'q211a_c_count',
                           f'q211_cal{i}',
                           f'q216a_cal{i}',
                           f'q216_cal{i}',
                           'q210',
                           f'q211a_{i}',
                           f'q211c_{i}',
                           f'q209a',
                           f'q209b',
                           f'q215_{i}',
                           f'q216c_{i}',
                           f'q216_{i}',
                           f'q216c_cal{i}',
                           f'q220a_{i}',
                           f'q220d_{i}']]
                        _[f"q211q215_cal{i}"]=0
                        _[f"q211q216_cal{i}"]=0
                        _[f"q215q216c_cal{i}"]=0
                        _[f"q216a_calq216c_cal{i}"]=0
                        _["index_strategy"]=strats[i]
                        _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
                        _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

                        _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
                        _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
                        # _.loc[(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q211q216_cal{i}"]=1
                        if str(type(_))=="<class 'pandas.core.frame.DataFrame'>":
                            _['index_strategy']=strats[i] +" + "+ strats[j]
                        if _.size>0:
                            # print(f"strategy:{i} + Strategy:{j}")
                            # _['dsd']=f"{i}+{j}"
                            # print(f"strategy:{i} + Strategy:{j}")
                            j=_[[
                                'index_strategy',
                                'resp_select',
                                f'q220g_{i}',
                                'q211q216',
                                f'q215q216c_cal{i}',
                                f"q216a_calq216c_cal{i}",
                                'q211a_c_count',
                                'q216_ac_count',
                                'q209a',
                                'q209b',
                                'q210',
                                f'q220a_{i}',
                                f'q211_cal{i}',
                                f'q216_cal{i}'

                            ]]
                            j.columns=range(j.shape[1])

                            res_list.append(j)
                    except(KeyError):
                        continue
            else:
                try:
                        # print(r[f'q220h_{i}{j}'].value_counts(dropna=False))

                    _=r[
                        (r[f'q{question}h_{i}{j}']==1)&
                        (r[f'q{question}d_{i}']==1)


                    ][['resp_select',
                       'q211q216', 
                       'q220',
                       'q221',
                       'q222',
                       'q223',
                       f'q{question}g_{i}',
                       f'strat_combine{i}',
                       'q216_ac_count',
                       'q211a_c_count',
                       f'q211_cal{i}',
                       f'q216a_cal{i}',
                       f'q216_cal{i}',
                       'q210',
                       f'q211a_{i}',
                       f'q211c_{i}',
                       f'q209a',
                       f'q209b',
                       f'q215_{i}',
                       f'q216c_{i}',
                       f'q216_{i}',
                       f'q216c_cal{i}',
                       f'q{question}a_{i}',
                       f'q{question}d_{i}']]
                    _[f"q211q215_cal{i}"]=0
                    _[f"q211q216_cal{i}"]=0
                    _[f"q215q216c_cal{i}"]=0
                    _[f"q216a_calq216c_cal{i}"]=0
                    _["index_strategy"]=strats[i]
                    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
                    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

                    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
                    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
                    # _.loc[(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q211q216_cal{i}"]=1
                    if str(type(_))=="<class 'pandas.core.frame.DataFrame'>":
                        _['index_strategy']=strats[i] +" + "+ strats[j]
                    if _.size>0:
                        # print(f"strategy:{i} + Strategy:{j}")
                        # _['dsd']=f"{i}+{j}"
                        # print(f"strategy:{i} + Strategy:{j}")
                        j=_[[
                            'index_strategy',
                            'resp_select',
                            f'q{question}g_{i}',
                            'q211q216',
                            f'q215q216c_cal{i}',
                            f"q216a_calq216c_cal{i}",
                            'q211a_c_count',
                            'q216_ac_count',
                            'q209a',
                            'q209b',
                            'q210',
                            f'q{question}a_{i}',
                            f'q211_cal{i}',
                            f'q216_cal{i}'

                        ]]
                        j.columns=range(j.shape[1])

                        res_list.append(j)
                except(KeyError):
                    continue


concurrent_user=pd.concat([res_list[0],
res_list[1],
res_list[2],
res_list[3],
res_list[4],
res_list[5],
res_list[6],
res_list[7],
res_list[8],
res_list[9],
res_list[10],
res_list[11],
res_list[12],
res_list[13],
res_list[14],
res_list[15],
res_list[16],
res_list[17],
res_list[18],
res_list[19],
res_list[20],
res_list[21],
res_list[22],
res_list[23],
res_list[24],
res_list[25],
res_list[26],
                           
])

concurrent_user.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220-q223)a_x',
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]
concurrent_user["Used Index Strategy with other strategy"].replace(0,"No")
concurrent_user["Used Index Strategy with other strategy"].replace(1,"Yes")
concurrent_user["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in concurrent_user["Used more than 1 strategy"]]
concurrent_user["Used Index Strategy with other strategy"]=["Yes" if x==1 else "No" for x in concurrent_user["Used Index Strategy with other strategy"]]
concurrent_user["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in concurrent_user["Used index strategy throughout 6 month period(q211 and q215)"]]
concurrent_user["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in concurrent_user["Used index strategy throughout 6 month period(q211 and q216)"]]
concurrent_user["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in concurrent_user["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
concurrent_user["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in concurrent_user["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
concurrent_user["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in concurrent_user["Used any strategy in the last one month (q209a)"]]
concurrent_user["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in concurrent_user["Used any strategy in the last 2-6 month (q209b)"]]
concurrent_user["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in concurrent_user["Used any strategy in the last 2-6 months (q210)"]]

concurrent_user["How often have you used this strategy in the past 6 months (q220-q223)a_x"]=[conv(x) if x is not None else x for x in concurrent_user["How often have you used this strategy in the past 6 months (q220-q223)a_x"]]
concurrent_user["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in concurrent_user["Used index stragegy in last 1 month (q211_calx=1)"]]
concurrent_user["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in concurrent_user["Used index stragegy in last 2-6 months (q216_calx=1)"]]
concurrent_user.to_excel(excel_dir()+"concurrent_user_profile.xlsx",index=False)



#stopper
res_list=[]
for i in [1,2,3,4,5,7,8]:
    # print(i,strats[i])
    _=r[((r[f'q220d_{i}']==0)|(r[f'q221d_{i}']==0)|(r[f'q222d_{i}']==0)|(r[f'q223d_{i}']==0))&(r[f'q216_cal{i}']==1)&((r[f'q220f_{i}']==0)|(r[f'q221f_{i}']==0)|(r[f'q222f_{i}']==0)|(r[f'q223f_{i}']==0))]
    [['resp_select',
      'q211q216', 
       'q220',
       'q221',
       'q222',
       'q223',
       f'q220g_{i}',
       f'strat_combine{i}',
       'q216_ac_count',
       'q211a_c_count',
       f'q211_cal{i}',
       f'q216a_cal{i}',
       f'q216_cal{i}',
       'q210',
       f'q211a_{i}',
       f'q211c_{i}',
       f'q209a',
       f'q209b',
       f'q215_{i}',
       f'q216c_{i}',
       f'q216_{i}',
       f'q216c_cal{i}',
       f'q220a_{i}',
       f'q220d_{i}']]
    _[f"q211q215_cal{i}"]=0
    _[f"q211q216_cal{i}"]=0
    _[f"q215q216c_cal{i}"]=0
    _[f"q216a_calq216c_cal{i}"]=0
    _["index_strategy"]=strats[i]
    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
    j=_[[
        'index_strategy',
        'resp_select',
        f'q220g_{i}',
        'q211q216',
        f'q215q216c_cal{i}',
        f"q216a_calq216c_cal{i}",
        'q211a_c_count',
        'q216_ac_count',
        'q209a',
        'q209b',
        'q210',
        f'q220a_{i}',
        f'q211_cal{i}',
        f'q216_cal{i}'
        
    ]]
    j.columns=range(j.shape[1])
  
    res_list.append(j)

stopper=pd.concat([res_list[0],
res_list[1],
res_list[2],
res_list[3],
res_list[4],
res_list[5],
res_list[6]
])
stopper.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220-q223)a_x',
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]
stopper["Used Index Strategy with other strategy"].replace(0,"No")
stopper["Used Index Strategy with other strategy"].replace(1,"Yes")
stopper["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in stopper["Used more than 1 strategy"]]
stopper["Used Index Strategy with other strategy"]=["Yes" if x==1 else "No" for x in stopper["Used Index Strategy with other strategy"]]
stopper["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in stopper["Used index strategy throughout 6 month period(q211 and q215)"]]
stopper["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in stopper["Used index strategy throughout 6 month period(q211 and q216)"]]
stopper["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in stopper["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
stopper["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in stopper["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
stopper["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in stopper["Used any strategy in the last one month (q209a)"]]
stopper["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in stopper["Used any strategy in the last 2-6 month (q209b)"]]
stopper["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in stopper["Used any strategy in the last 2-6 months (q210)"]]

stopper["How often have you used this strategy in the past 6 months (q220-q223)a_x"]=[conv(x) if x is not None else x for x in stopper["How often have you used this strategy in the past 6 months (q220-q223)a_x"]]
stopper["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in stopper["Used index stragegy in last 1 month (q211_calx=1)"]]
stopper["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in stopper["Used index stragegy in last 2-6 months (q216_calx=1)"]]

stopper.to_excel(excel_dir()+"stopper.xlsx",index=False)  

#switcher

    
res_list=[]
for i in [1,2,3,4,5,7,8]:
    # print(i,strats[i])
    _=r[((r[f'q220d_{i}']==0)|(r[f'q221d_{i}']==0)|(r[f'q222d_{i}']==0)|(r[f'q223d_{i}']==0))&(r[f'q216_cal{i}']==1)&((r[f'q220f_{i}']==1)|(r[f'q221f_{i}']==1)|(r[f'q222f_{i}']==1)|(r[f'q223f_{i}']==1))][['resp_select',
      'q211q216', 
       'q220',
       'q221',
       'q222',
       'q223',
       f'q220g_{i}',
       f'strat_combine{i}',
       'q216_ac_count',
       'q211a_c_count',
       f'q211_cal{i}',
       f'q216a_cal{i}',
       f'q216_cal{i}',
       'q210',
       f'q211a_{i}',
       f'q211c_{i}',
       f'q209a',
       f'q209b',
       f'q215_{i}',
       f'q216c_{i}',
       f'q216_{i}',
       f'q216c_cal{i}',
       f'q220a_{i}',
       f'q220d_{i}']]
    _[f"q211q215_cal{i}"]=0
    _[f"q211q216_cal{i}"]=0
    _[f"q215q216c_cal{i}"]=0
    _[f"q216a_calq216c_cal{i}"]=0
    _["index_strategy"]=strats[i]
    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
    j=_[[
        'index_strategy',
        'resp_select',
        f'q220g_{i}',
        'q211q216',
        f'q215q216c_cal{i}',
        f"q216a_calq216c_cal{i}",
        'q211a_c_count',
        'q216_ac_count',
        'q209a',
        'q209b',
        'q210',
        f'q220a_{i}',
        f'q211_cal{i}',
        f'q216_cal{i}'
        
    ]]
    j.columns=range(j.shape[1])
  
    res_list.append(j)

switcher=pd.concat([res_list[0],
res_list[1],
res_list[2],
res_list[3],
res_list[4],
res_list[5],
res_list[6]
])
switcher.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220-q223)a_x',
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]
switcher["Used Index Strategy with other strategy"].replace(0,"No")
switcher["Used Index Strategy with other strategy"].replace(1,"Yes")
switcher["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in switcher["Used more than 1 strategy"]]
switcher["Used Index Strategy with other strategy"]=["Yes" if x==1 else "No" for x in switcher["Used Index Strategy with other strategy"]]
switcher["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in switcher["Used index strategy throughout 6 month period(q211 and q215)"]]
switcher["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in switcher["Used index strategy throughout 6 month period(q211 and q216)"]]
switcher["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in switcher["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
switcher["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in switcher["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
switcher["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in switcher["Used any strategy in the last one month (q209a)"]]
switcher["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in switcher["Used any strategy in the last 2-6 month (q209b)"]]
switcher["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in switcher["Used any strategy in the last 2-6 months (q210)"]]

switcher["How often have you used this strategy in the past 6 months (q220-q223)a_x"]=[conv(x) if x is not None else x for x in switcher["How often have you used this strategy in the past 6 months (q220-q223)a_x"]]
switcher["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in switcher["Used index stragegy in last 1 month (q211_calx=1)"]]
switcher["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in switcher["Used index stragegy in last 2-6 months (q216_calx=1)"]]

switcher.to_excel(excel_dir()+"switcher_profile.xlsx",index=False)  
print("Done!")
