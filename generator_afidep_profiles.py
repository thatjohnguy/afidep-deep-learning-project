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
    elif x==4: 
        return "Once"
    else:
        return x
    

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
    # print(q)
    # print("-----------------------------------------------------------------------")
    for i in [1,2,3,4,5,7,8,9,12,13,14,15,16,17,18,19,20]:
        # print(strats[i])
        for j in [1,2,3,4,5,7,8,9,12,13,14,15,16,17,18,19,20]:
            a=str(i)
            b=str(j)
            if (len(a)==2) & (len(b)==2):
                continue
            else:
                # if(len(a)==2) & (len(b)==1):
                question=q
                c=f'q{question}h_{i}{j}' #q220h_123
                if(len(c)>8):
                    if(c[-4:][0]=='_') & (int(c[-2:]) in two_digit_strats):
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
                            _=_[_[f"q215q216c_cal{i}"]==1]
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
                    elif(c[-4:][0]=='_') & (int(c[-3:][:2]) in two_digit_strats):
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
                            _=_[_[f"q215q216c_cal{i}"]==1]
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
                        _=_[_[f"q215q216c_cal{i}"]==1]
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
        
concurrent_user=pd.concat(res_list)


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
    _=r[
             ((r[f'q220d_{i}']==0)|(r[f'q220d_{i}'].isna())&
        (r[f'q221d_{i}']==0)|(r[f'q221d_{i}'].isna())&
        (r[f'q222d_{i}']==0)|(r[f'q222d_{i}'].isna())&
        (r[f'q223d_{i}']==0)|(r[f'q223d_{i}'].isna())&
        (r[f'q220d_{i}'].notna())&(r[f'q221d_{i}'].notna())&(r[f'q223d_{i}'].notna())&(r[f'q223d_{i}'].notna()))&
        
        
        
        (r[f'q216_cal{i}']==1)&
        ((r[f'q220f_{i}']==0)|(r[f'q220f_{i}'].isna())&
        (r[f'q221f_{i}']==0)|(r[f'q221f_{i}'].isna())&
        (r[f'q222f_{i}']==0)|(r[f'q222f_{i}'].isna())&
        (r[f'q223f_{i}']==0)|(r[f'q223f_{i}'].isna())&
        (r[f'q220f_{i}'].notna())&(r[f'q221f_{i}'].notna())&(r[f'q223f_{i}'].notna())&(r[f'q223f_{i}'].notna()))]
    [['resp_select',
      'q211q216', 
       'q220',
       'q221',
       'q222',
       'q223',
       f'q220g_{i}',
       f'q221g_{i}',
       f'q222g_{i}',
       f'q223g_{i}',
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
       f'q221a_{i}',
       f'q222a_{i}',
       f'q223a_{i}',
       f'q220d_{i}',
       f'q221d_{i}',
       f'q222d_{i}',
       f'q223d_{i}',
       f'q220f_{i}',
       f'q221f_{i}',
       f'q222f_{i}',
       f'q223f_{i}'
     ]]
    _[f"q211q215_cal{i}"]=0
    _[f"q211q216_cal{i}"]=0
    _[f"q215q216c_cal{i}"]=0
    _[f"q216a_calq216c_cal{i}"]=0
    _["index_strategy"]=strats[i]
    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
    e=_.copy()
    j=_[[
        'index_strategy',
        'resp_select',
        f'q220g_{i}',
        f'q221g_{i}',
        f'q222g_{i}',
        f'q223g_{i}',
        'q211q216',
        f'q215q216c_cal{i}',
        f"q216a_calq216c_cal{i}",
        'q211a_c_count',
        'q216_ac_count',
        'q209a',
        'q209b',
        'q210',
        f'q220a_{i}',
        f'q221a_{i}',
        f'q222a_{i}',
        f'q223a_{i}',
        f'q220d_{i}',
       f'q221d_{i}',
       f'q222d_{i}',
       f'q223d_{i}',
        f'q220f_{i}',
       f'q221f_{i}',
       f'q222f_{i}',
       f'q223f_{i}',
        f'q211_cal{i}',
        f'q216_cal{i}'
        
    ]]
    j.columns=range(j.shape[1])
  
    res_list.append(j)

stopper=pd.concat(res_list)
stopper.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy(q220)',
    'Used Index Strategy with other strategy(q221)',
    'Used Index Strategy with other strategy(q222)',
    'Used Index Strategy with other strategy(q223)',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220)a_x',
    'How often have you used this strategy in the past 6 months (q221)a_x',
    'How often have you used this strategy in the past 6 months (q222)a_x',
    'How often have you used this strategy in the past 6 months (q223)a_x',
    
    'Still using index strategy?(q220)d_x',
    'Still using index strategy?(q221)d_x',
    'Still using index strategy?(q222)d_x',
    'Still using index strategy?(q223)d_x',
    
    'when you stopped using index strategy, did you start ussing another strategy?(q220)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q221)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q222)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q223)f_x',
    
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]

stopper["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in stopper["Used more than 1 strategy"]]
stopper["Used Index Strategy with other strategy(q220)"]=["Yes" if x==1 else "No" for x in stopper["Used Index Strategy with other strategy(q220)"]]
stopper["Used Index Strategy with other strategy(q221)"]=["Yes" if x==1 else "No" for x in stopper["Used Index Strategy with other strategy(q221)"]]
stopper["Used Index Strategy with other strategy(q222)"]=["Yes" if x==1 else "No" for x in stopper["Used Index Strategy with other strategy(q222)"]]
stopper["Used Index Strategy with other strategy(q223)"]=["Yes" if x==1 else "No" for x in stopper["Used Index Strategy with other strategy(q223)"]]

stopper["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in stopper["Used index strategy throughout 6 month period(q211 and q215)"]]
stopper["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in stopper["Used index strategy throughout 6 month period(q211 and q216)"]]
stopper["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in stopper["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
stopper["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in stopper["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
stopper["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in stopper["Used any strategy in the last one month (q209a)"]]
stopper["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in stopper["Used any strategy in the last 2-6 month (q209b)"]]
stopper["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in stopper["Used any strategy in the last 2-6 months (q210)"]]

stopper["How often have you used this strategy in the past 6 months (q220)a_x"]=[conv(x) for x in stopper["How often have you used this strategy in the past 6 months (q220)a_x"]]
stopper["How often have you used this strategy in the past 6 months (q221)a_x"]=[conv(x) for x in stopper["How often have you used this strategy in the past 6 months (q221)a_x"]]
stopper["How often have you used this strategy in the past 6 months (q222)a_x"]=[conv(x) for x in stopper["How often have you used this strategy in the past 6 months (q222)a_x"]]
stopper["How often have you used this strategy in the past 6 months (q223)a_x"]=[conv(x) for x in stopper["How often have you used this strategy in the past 6 months (q223)a_x"]]

stopper['Still using index strategy?(q220)d_x']=["No" if x==0 else "" for x in stopper['Still using index strategy?(q220)d_x']]
stopper['Still using index strategy?(q221)d_x']=["No" if x==0 else "" for x in stopper['Still using index strategy?(q221)d_x']]
stopper['Still using index strategy?(q222)d_x']=["No" if x==0 else "" for x in stopper['Still using index strategy?(q222)d_x']]
stopper['Still using index strategy?(q223)d_x']=["No" if x==0 else "" for x in stopper['Still using index strategy?(q223)d_x']]

stopper['when you stopped using index strategy, did you start ussing another strategy?(q220)f_x']=["No" if x==0 else "" for x in stopper['when you stopped using index strategy, did you start ussing another strategy?(q220)f_x']]
stopper['when you stopped using index strategy, did you start ussing another strategy?(q221)f_x']=["No" if x==0 else "" for x in stopper['when you stopped using index strategy, did you start ussing another strategy?(q221)f_x']]
stopper['when you stopped using index strategy, did you start ussing another strategy?(q222)f_x']=["No" if x==0 else "" for x in stopper['when you stopped using index strategy, did you start ussing another strategy?(q222)f_x']]
stopper['when you stopped using index strategy, did you start ussing another strategy?(q223)f_x']=["No" if x==0 else "" for x in stopper['when you stopped using index strategy, did you start ussing another strategy?(q223)f_x']]

stopper["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in stopper["Used index stragegy in last 1 month (q211_calx=1)"]]
stopper["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in stopper["Used index stragegy in last 2-6 months (q216_calx=1)"]]

stopper.to_excel(excel_dir()+"stopper_profile.xlsx",index=False)  

#switcher

    
res_list=[]
for i in [1,2,3,4,5,7,8]:
    # print(i,strats[i])
    _=r[
        ((r[f'q220d_{i}']==0)|(r[f'q220d_{i}'].isna())&
        (r[f'q221d_{i}']==0)|(r[f'q221d_{i}'].isna())&
        (r[f'q222d_{i}']==0)|(r[f'q222d_{i}'].isna())&
        (r[f'q223d_{i}']==0)|(r[f'q223d_{i}'].isna())&
        (r[f'q220d_{i}'].notna())&(r[f'q221d_{i}'].notna())&(r[f'q223d_{i}'].notna())&(r[f'q223d_{i}'].notna()))&
        
        
        
        (r[f'q216_cal{i}']==1)&
        ((r[f'q220f_{i}']==1)|(r[f'q220f_{i}'].isna())&
        (r[f'q221f_{i}']==1)|(r[f'q221f_{i}'].isna())&
        (r[f'q222f_{i}']==1)|(r[f'q222f_{i}'].isna())&
        (r[f'q223f_{i}']==1)|(r[f'q223f_{i}'].isna())&
        (r[f'q220f_{i}'].notna())&(r[f'q221f_{i}'].notna())&(r[f'q223f_{i}'].notna())&(r[f'q223f_{i}'].notna()))
       
       ] [['resp_select',
      'q211q216', 
       'q220',
       'q221',
       'q222',
       'q223',
       f'q220g_{i}',
       f'q221g_{i}',
       f'q222g_{i}',
       f'q223g_{i}',
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
       f'q221a_{i}',
       f'q222a_{i}',
       f'q223a_{i}',
       f'q220d_{i}',
       f'q221d_{i}',
       f'q222d_{i}',
       f'q223d_{i}',
       f'q220f_{i}',
       f'q221f_{i}',
       f'q222f_{i}',
       f'q223f_{i}'
          ]]
    _[f"q211q215_cal{i}"]=0
    _[f"q211q216_cal{i}"]=0
    _[f"q215q216c_cal{i}"]=0
    _[f"q216a_calq216c_cal{i}"]=0
    _["index_strategy"]=strats[i]
    _.loc[(_[f'q210']!=1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q215q216c_cal{i}"]=1
    _.loc[(_[f'q210']==1)&(_[f'q211_cal{i}']==1)&(_[f'q216_cal{i}']==1),f"q216a_calq216c_cal{i}"]=1

    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q215_{i}']==1)|(_[f'q216c_{i}']==1)),f"q211q215_cal{i}"]=1
    _.loc[(_[f'q211_cal{i}']==1)&((_[f'q216_cal{i}']==1)),f"q211q216_cal{i}"]=1 
    w=_.copy()
    j=_[[
         'index_strategy',
        'resp_select',
        f'q220g_{i}',
        f'q221g_{i}',
        f'q222g_{i}',
        f'q223g_{i}',
        'q211q216',
        f'q215q216c_cal{i}',
        f"q216a_calq216c_cal{i}",
        'q211a_c_count',
        'q216_ac_count',
        'q209a',
        'q209b',
        'q210',
        f'q220a_{i}',
        f'q221a_{i}',
        f'q222a_{i}',
        f'q223a_{i}',
        f'q220d_{i}',
       f'q221d_{i}',
       f'q222d_{i}',
       f'q223d_{i}',
        f'q220f_{i}',
       f'q221f_{i}',
       f'q222f_{i}',
       f'q223f_{i}',
        f'q211_cal{i}',
        f'q216_cal{i}'
        
    ]]
    j.columns=range(j.shape[1])
  
    res_list.append(j)

switcher=pd.concat(res_list)
switcher.columns=[
    'Index Strategy Used',
    'Respondent ID',
    'Used Index Strategy with other strategy(q220)',
    'Used Index Strategy with other strategy(q221)',
    'Used Index Strategy with other strategy(q222)',
    'Used Index Strategy with other strategy(q223)',
    'Used more than 1 strategy',
    'Used index strategy throughout 6 month period(q211 and q215)',
    'Used index strategy throughout 6 month period(q211 and q216)',
    'Used more than 1 strategy in last 1 month (q211a_c_count > 1)',
    'Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)',
    'Used any strategy in the last one month (q209a)',
    'Used any strategy in the last 2-6 month (q209b)',
    'Used any strategy in the last 2-6 months (q210)',
    'How often have you used this strategy in the past 6 months (q220)a_x',
    'How often have you used this strategy in the past 6 months (q221)a_x',
    'How often have you used this strategy in the past 6 months (q222)a_x',
    'How often have you used this strategy in the past 6 months (q223)a_x',
    
    'Still using index strategy?(q220)d_x',
    'Still using index strategy?(q221)d_x',
    'Still using index strategy?(q222)d_x',
    'Still using index strategy?(q223)d_x',
    
    'when you stopped using index strategy, did you start ussing another strategy?(q220)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q221)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q222)f_x',
    'when you stopped using index strategy, did you start ussing another strategy?(q223)f_x',
    
    'Used index stragegy in last 1 month (q211_calx=1)',
    'Used index stragegy in last 2-6 months (q216_calx=1)'
]

switcher["Used more than 1 strategy"]=["Yes" if x>1 else "No" for x in switcher["Used more than 1 strategy"]]
switcher["Used Index Strategy with other strategy(q220)"]=["Yes" if x==1 else "No" for x in switcher["Used Index Strategy with other strategy(q220)"]]
switcher["Used Index Strategy with other strategy(q221)"]=["Yes" if x==1 else "No" for x in switcher["Used Index Strategy with other strategy(q221)"]]
switcher["Used Index Strategy with other strategy(q222)"]=["Yes" if x==1 else "No" for x in switcher["Used Index Strategy with other strategy(q222)"]]
switcher["Used Index Strategy with other strategy(q223)"]=["Yes" if x==1 else "No" for x in switcher["Used Index Strategy with other strategy(q223)"]]

switcher["Used index strategy throughout 6 month period(q211 and q215)"]=["Yes" if x==1 else "" for x in switcher["Used index strategy throughout 6 month period(q211 and q215)"]]
switcher["Used index strategy throughout 6 month period(q211 and q216)"]=["Yes" if x==1 else "" for x in switcher["Used index strategy throughout 6 month period(q211 and q216)"]]
switcher["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]=["No" if x==1 else "Yes" for x in switcher["Used more than 1 strategy in last 1 month (q211a_c_count > 1)"]]
switcher["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]=["No" if x==1 else "Yes" for x in switcher["Used more than 1 strategy in last 2- 6 months (q216_ac_count > 1)"]]
switcher["Used any strategy in the last one month (q209a)"]=["Yes" if x==1 else "No" for x in switcher["Used any strategy in the last one month (q209a)"]]
switcher["Used any strategy in the last 2-6 month (q209b)"]=["Yes" if x==1 else "No" for x in switcher["Used any strategy in the last 2-6 month (q209b)"]]
switcher["Used any strategy in the last 2-6 months (q210)"]=["Yes" if x==1 else "" for x in switcher["Used any strategy in the last 2-6 months (q210)"]]

switcher["How often have you used this strategy in the past 6 months (q220)a_x"]=[conv(x) for x in switcher["How often have you used this strategy in the past 6 months (q220)a_x"]]
switcher["How often have you used this strategy in the past 6 months (q221)a_x"]=[conv(x) for x in switcher["How often have you used this strategy in the past 6 months (q221)a_x"]]
switcher["How often have you used this strategy in the past 6 months (q222)a_x"]=[conv(x) for x in switcher["How often have you used this strategy in the past 6 months (q222)a_x"]]
switcher["How often have you used this strategy in the past 6 months (q223)a_x"]=[conv(x) for x in switcher["How often have you used this strategy in the past 6 months (q223)a_x"]]

switcher['Still using index strategy?(q220)d_x']=["No" if x==0 else "" for x in switcher['Still using index strategy?(q220)d_x']]
switcher['Still using index strategy?(q221)d_x']=["No" if x==0 else "" for x in switcher['Still using index strategy?(q221)d_x']]
switcher['Still using index strategy?(q222)d_x']=["No" if x==0 else "" for x in switcher['Still using index strategy?(q222)d_x']]
switcher['Still using index strategy?(q223)d_x']=["No" if x==0 else "" for x in switcher['Still using index strategy?(q223)d_x']]

switcher['when you stopped using index strategy, did you start ussing another strategy?(q220)f_x']=["Yes" if x==1 else "" for x in switcher['when you stopped using index strategy, did you start ussing another strategy?(q220)f_x']]
switcher['when you stopped using index strategy, did you start ussing another strategy?(q221)f_x']=["Yes" if x==1 else "" for x in switcher['when you stopped using index strategy, did you start ussing another strategy?(q221)f_x']]
switcher['when you stopped using index strategy, did you start ussing another strategy?(q222)f_x']=["Yes" if x==1 else "" for x in switcher['when you stopped using index strategy, did you start ussing another strategy?(q222)f_x']]
switcher['when you stopped using index strategy, did you start ussing another strategy?(q223)f_x']=["Yes" if x==1 else "" for x in switcher['when you stopped using index strategy, did you start ussing another strategy?(q223)f_x']]

switcher["Used index stragegy in last 1 month (q211_calx=1)"]=["Yes" if x==1 else "No" for x in switcher["Used index stragegy in last 1 month (q211_calx=1)"]]
switcher["Used index stragegy in last 2-6 months (q216_calx=1)"]=["Yes" if x==1 else "No" for x in switcher["Used index stragegy in last 2-6 months (q216_calx=1)"]]

switcher.to_excel(excel_dir()+"switcher_profile.xlsx",index=False)  
print("Done!")


#summary and qual selection
respondent_names=pd.read_excel(excel_dir()+"teamup_women_name.xlsx")

interviewer_names=pd.read_excel(excel_dir()+"teamup_interviewers.xlsx")

choices=pd.read_excel(excel_dir()+"lgas.xlsx")


consistent_user['profile']="Consistent User"
concurrent_user['profile']="Concurrent User"
stopper['profile']="Stopper"
switcher['profile']="Switcher"



data=r.copy()
data['respondent_names']=respondent_names['res_name']
data['state']="Adamawa"
selected_id=[]
selected_id.append(pd.Series(consistent_user["Respondent ID"]))
selected_id.append(pd.Series(concurrent_user["Respondent ID"]))
selected_id.append(pd.Series(stopper["Respondent ID"]))
selected_id.append(pd.Series(switcher["Respondent ID"]))
selected_id=pd.concat(selected_id)
selected_id=list(selected_id)
# selected_id

selected_strategy=[]
selected_strategy.append(pd.Series(consistent_user["Index Strategy Used"]))
selected_strategy.append(pd.Series(concurrent_user["Index Strategy Used"]))
selected_strategy.append(pd.Series(stopper["Index Strategy Used"]))
selected_strategy.append(pd.Series(switcher["Index Strategy Used"]))
selected_strategy=pd.concat(selected_strategy)
selected_strategy=list(selected_strategy)

selected_profiles=[]
selected_profiles.append(pd.Series(consistent_user["profile"]))
selected_profiles.append(pd.Series(concurrent_user["profile"]))
selected_profiles.append(pd.Series(stopper["profile"]))
selected_profiles.append(pd.Series(switcher["profile"]))
selected_profiles=pd.concat(selected_profiles)
selected_profiles=list(selected_profiles)
# selected_strategy
resp_name=[]
lga=[]
ward=[]
phone1=[]
phone2=[]
reinterview=[]
good_time=[]
head=[]
gpslat=[]
gpslong=[]
gpsalt=[]
gpsacc=[]
date_of_interview=[]
observation=[]
husband_concent=[]
interviewer=[]

for i in selected_id:
    x=data[data['resp_select']==i]['respondent_names']
    resp_name.append(x.iloc[0])
    
for i in selected_id:
    x=data[data['resp_select']==i]['level3']
    x=x.iloc[0]
    x=int(x)
    x=choices[choices["code"]==x]["decode"]
    x=x.iloc[0]
    lga.append(x)
for i in selected_id:
    x=data[data['resp_select']==i]['ward']
    x=x.iloc[0]
    x=str(x)
    ward.append(x)
for i in selected_id:
    x=data[data['resp_select']==i]['phn_1st']
    phone1.append(x.iloc[0])

for i in selected_id:
    x=data[data['resp_select']==i]['phn_2nd']
    x=x.iloc[0]
    x=str(x)
    
    phone2.append(x)
for i in selected_id:
    x=data[data['resp_select']==i]['provide_phn']
    reinterview.append(x.iloc[0])
for i in selected_id:
    x=data[data['resp_select']==i]['husband_schedule']
    x=x.iloc[0]
    good_time.append(x[-11:])
for i in selected_id:
    x=data[data['resp_select']==i]['husband_name']
    x=x.iloc[0]
    x=str(x)   
    head.append(x)
for i in selected_id:
    x=data[data['resp_select']==i]['husband_participate']
    husband_concent.append(x.iloc[0])  
for i in selected_id:
    x=data[data['resp_select']==i]['gpslongitude']
    gpslong.append(x.iloc[0]) 
for i in selected_id:
    x=data[data['resp_select']==i]['gpsaltitude']
    gpsalt.append(x.iloc[0]) 
for i in selected_id:
    x=data[data['resp_select']==i]['gpsaccuracy']
    gpsacc.append(x.iloc[0]) 
for i in selected_id:
    x=data[data['resp_select']==i]['gpslatitude']
    gpslat.append(x.iloc[0])
for i in selected_id:
    x=data[data['resp_select']==i]['today']
    date_of_interview.append(x.iloc[0]) 
for i in selected_id:
    x=data[data['resp_select']==i]['observation']
    observation.append(x.iloc[0])
for i in selected_id:
    x=data[data['resp_select']==i]['your_name']
    interviewer.append(x.iloc[0])   

selection=pd.DataFrame({"Respondent ID":selected_id,
              "Respondent Name":resp_name,
              "Profile":selected_profiles,
              "Strategy":selected_strategy,
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
selection.replace("nan",np.nan,inplace=True)
selection.replace(np.nan,'',inplace=True)

selection.to_excel(excel_dir()+"AFIDEP_qualitative_selection_adamawa_2Dec2022.xlsx",index=False)
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
summary=pd.DataFrame(a,columns=["","N","Total","%"])
summary.to_excel(excel_dir()+"summary_2Dec2022.xlsx",sheet_name="profile",index=False)