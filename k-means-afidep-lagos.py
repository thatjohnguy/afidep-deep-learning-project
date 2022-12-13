#!/usr/bin/env python
# coding: utf-8

# In[34]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # for data visualization
import seaborn as sns # for statistical data visualization
get_ipython().run_line_magic('matplotlib', 'inline')


# In[158]:


from sklearn.preprocessing import LabelEncoder


# In[76]:


from dataset_dir import excel_dir


# In[35]:


import warnings
warnings.filterwarnings('ignore')


# In[67]:


pd.io.formats.excel.ExcelFormatter.header_style = None
pd.options.display.max_rows = None
pd.options.display.max_columns = None
r=pd.read_stata(stata_dir()+"Teamup_women_Dataset_Lagos.dta",convert_categoricals=False)
r=r[r['level2']==7]


# In[68]:


data=r.copy()
cut_starting=list(data.columns[:26])
cut_ending=list(data.columns[-23:])
for i,j in enumerate(cut_ending):
    if(j=="instanceid"):
        del cut_ending[i]
    

for c in cut_starting:
    del data[c]
for c in cut_ending:
    del data[c]


# In[69]:


df=data.copy()


# Exploratory data analysis

# In[70]:


df.shape


# In[38]:


df.info()


# Drop redundant features

# In[71]:


red=[]
for i in df.columns:
    if(df[i].isnull().sum()==df.shape[0]):
        red.append(i)
for i in red:
    del df[i]


# In[72]:


df.shape


# fill missing values with special number

# In[ ]:


for i in 


# In[73]:


for i in df.columns:
    df[i]=df[i].fillna(-91)


# In[74]:


df.shape


# In[124]:


y=pd.read_excel(excel_dir()+"y.xlsx")


# In[125]:


y_ids=y['Respondent ID']


# In[126]:


x=df[df['resp_select'].isin(y_ids)]


# In[127]:


x.shape


# In[128]:


target=y[['Respondent ID','profile']]
target['resp_select']=y['Respondent ID']
del target['Respondent ID']


# In[164]:


m=pd.merge(x,target,how='right',on='resp_select')


# In[165]:


m.shape


# declare vector and target variables

# In[166]:


X=m
y=m['profile']


# In[167]:


del X['res_name']
del X['ward']
del X['hh_name']
del X['q102']
del X['q106_cal']
del X['q211_strategy1']
del X['instanceid']
del X['resp_select']
del X['strat_lab1']

for i in X.columns:
    if(i[0]=="v"):
        del X[i]
for i in X.columns:
    if('strategy' in i):
        del X[i]
for i in X.columns:
    if('cal' in i):
        del X[i]
for i in X.columns:
    if('lab' in i):
        del X[i]
X=X.replace('',-91)
for i in X.columns:
    if(X[i].dtype=='object'):
        del X[i]

for i in X.columns:
    X[i]=X[i].astype(int)        


# In[168]:


X.shape


# In[169]:


le = LabelEncoder()

X['profile'] = le.fit_transform(X['profile'])

y = le.transform(y)


# In[182]:


X.info(verbose=True, show_counts=True)


# feature scaling

# In[184]:


cols=X.columns


# In[185]:


from sklearn.preprocessing import MinMaxScaler

ms = MinMaxScaler()

X = ms.fit_transform(X)


# In[186]:


X = pd.DataFrame(X, columns=[cols])


# In[188]:


X.head(3)


# Kmeans model with 4 clusters

# In[231]:


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=0) 

kmeans.fit(X)


# In[232]:


kmeans.cluster_centers_


# In[233]:


kmeans.inertia_


# In[234]:


labels = kmeans.labels_

# check how many of the samples were correctly labeled
correct_labels = sum(y == labels)

print("Result: %d out of %d samples were correctly labeled." % (correct_labels, y.size))


# In[230]:


print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y.size)))


# In[223]:


from sklearn.cluster import KMeans
cs = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    kmeans.fit(X)
    cs.append(kmeans.inertia_)
plt.plot(range(1, 11), cs)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('CS')
plt.show()


# In[ ]:




