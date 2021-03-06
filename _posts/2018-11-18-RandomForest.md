---
layout: post
title: Random Forest Part 1
---

## -Simple yet powerful
Random Forest is really powerfull machine learning algorithm. In general there is no algorithm that works well for any kind of dataset. However, random forest comes pretty close.

* It can make predictions for both a continous variable or categorical.
* It usually does not overfit to badly and you generally don't need a validation set.
* It requires very little feature engineering.
    
We will use, probably the most popular package for machine learing in Python, i.e. scikit-learn. It's not the best at anything (that I am aware of) but it's not bad at anything either. We will also use Pandas which probably is the most popular data analysis tool for python. It's so popular that it has a standard for importing ("as pd").


```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
import re
import warnings; warnings.simplefilter('ignore')
from IPython.display import display, Markdown
df_train=pd.read_csv('data/train.csv')
df_test=pd.read_csv('data/test.csv')
```


```python
def pandas_df_to_markdown_table(df):
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.to_csv(sep="|", index=False)))
```


```python
pandas_df_to_markdown_table(df_train.head())
```


PassengerId|Survived|Pclass|Name|Sex|Age|SibSp|Parch|Ticket|Fare|Cabin|Embarked
---|---|---|---|---|---|---|---|---|---|---|---
1|0|3|Braund, Mr. Owen Harris|male|22.0|1|0|A/5 21171|7.25||S
2|1|1|Cumings, Mrs. John Bradley (Florence Briggs Thayer)|female|38.0|1|0|PC 17599|71.2833|C85|C
3|1|3|Heikkinen, Miss. Laina|female|26.0|0|0|STON/O2. 3101282|7.925||S
4|1|1|Futrelle, Mrs. Jacques Heath (Lily May Peel)|female|35.0|1|0|113803|53.1|C123|S
5|0|3|Allen, Mr. William Henry|male|35.0|0|0|373450|8.05||S




```python
print(df_train.info())
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 891 entries, 0 to 890
    Data columns (total 12 columns):
    PassengerId    891 non-null int64
    Survived       891 non-null int64
    Pclass         891 non-null int64
    Name           891 non-null object
    Sex            891 non-null object
    Age            714 non-null float64
    SibSp          891 non-null int64
    Parch          891 non-null int64
    Ticket         891 non-null object
    Fare           891 non-null float64
    Cabin          204 non-null object
    Embarked       889 non-null object
    dtypes: float64(2), int64(5), object(5)
    memory usage: 83.6+ KB
    None
    


```python
print(df_train.describe())
```

           PassengerId    Survived      Pclass         Age       SibSp  \
    count   891.000000  891.000000  891.000000  714.000000  891.000000   
    mean    446.000000    0.383838    2.308642   29.699118    0.523008   
    std     257.353842    0.486592    0.836071   14.526497    1.102743   
    min       1.000000    0.000000    1.000000    0.420000    0.000000   
    25%     223.500000    0.000000    2.000000   20.125000    0.000000   
    50%     446.000000    0.000000    3.000000   28.000000    0.000000   
    75%     668.500000    1.000000    3.000000   38.000000    1.000000   
    max     891.000000    1.000000    3.000000   80.000000    8.000000   
    
                Parch        Fare  
    count  891.000000  891.000000  
    mean     0.381594   32.204208  
    std      0.806057   49.693429  
    min      0.000000    0.000000  
    25%      0.000000    7.910400  
    50%      0.000000   14.454200  
    75%      0.000000   31.000000  
    max      6.000000  512.329200  
    

From the above we can see that
* Some columns contains string data
* Some columns are missing data
* max, min etc seems to be reasonable i.e. it doesn't seem to be any obvious errors in the data
Random forest (and most algorithms) need numbers, not strings, and moreover can't handle missing data. So we need to do some feature enginering. But first, lets see how good a result we can det by just choosing columns with given number data and do a quick replacement of the missing data.


```python
def getTestScoreFromRMFC(x_train, x_test, y_train, y_test):
    rmfc=RandomForestClassifier(n_estimators=20, criterion='entropy',n_jobs=-1)
    rmfc.fit(x_train, y_train)
    test_score=rmfc.score(x_test, y_test)
    return test_score
```


```python
#fill in missing values and run a quick test
df_train['Age'].fillna(df_train['Age'].median(),inplace=True) #Sometimes you see people use mean value. Often that is fine but using median should usually be better
X=df_train[['Pclass', 'Age', 'SibSp','Parch']]
y=df_train['Survived']
x_train, x_test, y_train, y_test = model_selection.train_test_split( X, y, test_size=0.20, random_state=42)
print('Test score:',getTestScoreFromRMFC(x_train, x_test, y_train, y_test))
```

    Test score: 0.6927374301675978
    

As you might have suspected, the result is not very good. But it's way better than chance alone. Now, let's try using more data.
## Feature engineering
### Gender
Starting with the column 'Sex'. We have two categories, 'male', 'female'.


```python
#RandomForest can only work with numercal values. We must convert 'male', 'female' info numbers. Sklearn has a method for this.
from sklearn.preprocessing import LabelEncoder
le_gender=LabelEncoder()
#Encode categories into numbers:
le_gender.fit(df_train['Sex'])
#You can check which categories where found:
le_gender.classes_
#Transform the categorical data into numbers
le_gender.transform(df_train['Sex'])
df_train['Sex']=le_gender.transform(df_train['Sex'])
```


```python
#Second run 
#If we run RandomForestClassifier with this extra data we find a huge improvement (which is due to that gender is the most important factor in the titanic data set. How we can determine that we will look at later)
X=df_train[['Pclass', 'Age','Sex', 'SibSp','Parch']]
y=df_train['Survived']
x_train, x_test, y_train, y_test = model_selection.train_test_split( X, y, test_size=0.20, random_state=42)
print('Test score:',getTestScoreFromRMFC(x_train, x_test, y_train, y_test))
```

    Test score: 0.7877094972067039
    

We significantely improve the test score with very litte effor. 

### Embarked 
Lets do the same thing with Embarked. However, Embarked has two null-values, so first let's replace them with 'M' for missing value.


```python
df_train['Embarked'].fillna('M', inplace=True) #replacing missing values with 'M'
le_embarked=LabelEncoder()
le_embarked.fit(df_train['Embarked'])
le_embarked.classes_
df_train['Embarked']=le_embarked.transform(df_train['Embarked'])
#You can now run your data again as in 'Second run'. Don't forget to add the 'Embarked' column. You will not see much of a difference. 
```


```python
df_train[df_train['Cabin'].isnull()==True].index
```




    Int64Index([  0,   2,   4,   5,   7,   8,   9,  12,  13,  14,
                ...
                878, 880, 881, 882, 883, 884, 885, 886, 888, 890],
               dtype='int64', length=687)



### Cabin
Most of the Cabin info is missing. But let's first se if Cabin has any relevance before discarding it. Again replacing NaN with 'M0' (since we will split into letter and number).


```python
def cabin_split(cabin):
    cabin_croped = cabin.split(' ')[0]
    if len(cabin_croped)<2: #this if statement is an ugly hack to handle different cabin name formats
        cabin_croped=cabin.replace(' ','')
        if len(cabin_croped)<2:
            return cabin_croped, 0
    match = re.match(r"([a-z]+)([0-9]+)", cabin_croped, re.I)
    letter, number =match.groups()
    return letter, int(number)
```


```python
df_train['Cabin'].fillna('M0', inplace=True) #Replace NaN with 'M0'
df_train['CabinChar']=df_train['Cabin'].apply(lambda x: cabin_split(x)[0])
df_train['CabinNum']=df_train['Cabin'].apply(lambda x: cabin_split(x)[1])
```


```python
le_cabinchar=LabelEncoder()
le_cabinchar.fit(df_train['CabinChar'])
le_cabinchar.classes_
df_train['CabinChar']=le_cabinchar.transform(df_train['CabinChar'])
```

### Ticket
Lets handle ticket similar to what we did with cabin


```python
def ticket_split(ticket):
    split_result=ticket.split(' ')
    if len(split_result)==1:
        try:
            return ' ', int(split_result[0])
        except:
            return split_result[0], 0 
    else:
        num=split_result[1]
        try:
            num=int(num)
        except:
            num=0
        return split_result[0], num 
```


```python
df_train['TicketChar']=df_train['Ticket'].apply(lambda x: ticket_split(x)[0])
df_train['TicketNum']=df_train['Ticket'].apply(lambda x: ticket_split(x)[1])
```

Transform TicketChar into number categories


```python
le_tickchar=LabelEncoder()
le_tickchar.fit(df_train['TicketChar'])
le_tickchar.classes_
df_train['TicketChar']=le_tickchar.transform(df_train['TicketChar'])
```

### Name
From the name column we can extract title. There might be something we can do with the name itself. Does the number of names has an impact (upper class people tended to have more names). Does the length of the name matter? We could even perhaps use external data if we hade access to some useful statistics of names from the period. We will settle with title

#### Title


```python
df_train['Title']=df_train['Name'].str.split(',', expand=True)[1].str.split('.', expand=True)[0]
```


```python
le_title=LabelEncoder()
le_title.fit(df_train['Title'])
le_title.classes_
df_train['Title']=le_title.transform(df_train['Title'])
```

#### Length of name


```python
def getNameLength(name):
    #exlude title
    part1=name.split(',')[0]
    part2=name.split('.')[1]
    tot_length=len(part1)+len(part2)
    return tot_length
```


```python
#length of name
df_train['NameLength']=df_train['Name'].apply(lambda x: getNameLength(x))
```

### FamilySize and IsAlone
I have seen people add this in their kernel but I don't see any improvement. This information should be available to the Random Forest algorithm anyway.


```python
df_train['FamilySize']=df_train['SibSp']+df_train['Parch']
```


```python
df_train['IsAlone']=df_train['FamilySize'].apply(lambda x: 1 if x==1 else 0)
```

### Saving feature engineered dataframe
We use the feather function to save the dataframe. In this case its a small dataframe so how we store it does not matter much, however, with large dataframes feather is an excellent way of quickly storing and load from disk. The feather format stores the data similar to how its stored in RAM, therefore need litle processing. It's an increasingly popular way of storing data for quick access.

df_train.to_feather('train_cleaned')
# read back by
# df_train=pd.read_feather('train_cleaned')

## Run prediction
Let's use our 'new' data


```python
df_train.columns
```




    Index(['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
           'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked', 'CabinChar', 'CabinNum',
           'TicketChar', 'TicketNum', 'Title', 'NameLength', 'FamilySize',
           'IsAlone'],
          dtype='object')




```python
X=df_train[['Pclass','Sex','Age', 'SibSp','Parch', 'Fare', 'CabinChar', 'CabinNum', 'TicketChar', 'TicketNum', 'Title']]
y=df_train['Survived']
x_train, x_test, y_train, y_test = model_selection.train_test_split( X, y, test_size=0.20)
getTestScoreFromRMFC(x_train, x_test, y_train, y_test)
```




    0.8324022346368715



Let's run the test for 100 times to see what the average test score is.


```python
mean=0
for i in range(100):
    print('#',end='')
    X=df_train[['Pclass','Sex','Age', 'SibSp','Parch', 'Fare', 'CabinChar', 'CabinNum', 'TicketNum', 'Title','NameLength']]
    y=df_train['Survived']
    x_train, x_test, y_train, y_test = model_selection.train_test_split( X, y, test_size=0.20)
    mean+=getTestScoreFromRMFC(x_train, x_test, y_train, y_test)
print(' Ready!')
print('Average', mean/100)
```

    #################################################################################################### Ready!
    Average 0.8303910614525136
    

### About the result
We didn't improve our result significantly despite adding lots of data. We will take a look at why this is so i another blog post where we visualize the data and correlations between categories.

### Testing other algorithms
Let's see how good random forest is compared to some other sci-kit tools.


```python
from sklearn import svm, tree, linear_model, neighbors, naive_bayes, ensemble, discriminant_analysis, gaussian_process

#Machine Learning Algorithm (MLA) Selection and Initialization
MLA = [
    #Ensemble Methods
    ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(),
    ensemble.ExtraTreesClassifier(),
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),

    #Gaussian Processes
    gaussian_process.GaussianProcessClassifier(),
    
    #GLM
    linear_model.LogisticRegressionCV(),
    linear_model.PassiveAggressiveClassifier(),
    linear_model.RidgeClassifierCV(),
    linear_model.SGDClassifier(),
    linear_model.Perceptron(),
    
    #Navies Bayes
    naive_bayes.BernoulliNB(),
    naive_bayes.GaussianNB(),
    
    #Nearest Neighbor
    neighbors.KNeighborsClassifier(),
    
    #SVM
    svm.SVC(probability=True),
    svm.NuSVC(probability=True),
    svm.LinearSVC(),
    
    #Trees    
    tree.DecisionTreeClassifier(),
    tree.ExtraTreeClassifier(),
    
    #Discriminant Analysis
    discriminant_analysis.LinearDiscriminantAnalysis(),
    discriminant_analysis.QuadraticDiscriminantAnalysis(),
 
   
    ]

```


```python
cv_split = model_selection.ShuffleSplit(n_splits = 100, test_size = .2, train_size = .8, random_state = 0 ) # run model 100 times with 20/80 test/train split. 
```


```python
X=df_train[['Pclass','Sex','Age', 'SibSp','Parch', 'Fare', 'CabinChar', 'CabinNum', 'TicketNum', 'Title','NameLength']]
y=df_train['Survived']
```


```python
df_testscore=pd.DataFrame(columns=['Algorithm', 'Test score', 'Time '])

for i,i_mla in enumerate(MLA):
    cv_results=model_selection.cross_validate(i_mla, X, y, cv=cv_split) #Returns dictionary with scores
    mean_test_score=cv_results['test_score'].mean()
    mean_test_time=cv_results['fit_time'].mean()
    print('#',end='')
    #print(i_mla.__class__.__name__,'Averate test score:', mean_test_score)
    df_testscore.loc[i]=[i_mla.__class__.__name__, mean_test_score, mean_test_time]
print('Ready!')
```

    #####################Ready!
    


```python
df_testscore
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Algorithm</th>
      <th>Test score</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AdaBoostClassifier</td>
      <td>0.815363</td>
      <td>0.065842</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BaggingClassifier</td>
      <td>0.814078</td>
      <td>0.022147</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ExtraTreesClassifier</td>
      <td>0.817263</td>
      <td>0.012723</td>
    </tr>
    <tr>
      <th>3</th>
      <td>GradientBoostingClassifier</td>
      <td>0.832682</td>
      <td>0.089744</td>
    </tr>
    <tr>
      <th>4</th>
      <td>RandomForestClassifier</td>
      <td>0.821229</td>
      <td>0.014231</td>
    </tr>
    <tr>
      <th>5</th>
      <td>GaussianProcessClassifier</td>
      <td>0.689441</td>
      <td>0.247731</td>
    </tr>
    <tr>
      <th>6</th>
      <td>LogisticRegressionCV</td>
      <td>0.716425</td>
      <td>0.097742</td>
    </tr>
    <tr>
      <th>7</th>
      <td>PassiveAggressiveClassifier</td>
      <td>0.538436</td>
      <td>0.002254</td>
    </tr>
    <tr>
      <th>8</th>
      <td>RidgeClassifierCV</td>
      <td>0.793575</td>
      <td>0.003988</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SGDClassifier</td>
      <td>0.551453</td>
      <td>0.002159</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Perceptron</td>
      <td>0.532626</td>
      <td>0.002179</td>
    </tr>
    <tr>
      <th>11</th>
      <td>BernoulliNB</td>
      <td>0.788045</td>
      <td>0.002298</td>
    </tr>
    <tr>
      <th>12</th>
      <td>GaussianNB</td>
      <td>0.682737</td>
      <td>0.002129</td>
    </tr>
    <tr>
      <th>13</th>
      <td>KNeighborsClassifier</td>
      <td>0.688492</td>
      <td>0.002188</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SVC</td>
      <td>0.632905</td>
      <td>0.198373</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NuSVC</td>
      <td>0.634190</td>
      <td>0.209005</td>
    </tr>
    <tr>
      <th>16</th>
      <td>LinearSVC</td>
      <td>0.530056</td>
      <td>0.037551</td>
    </tr>
    <tr>
      <th>17</th>
      <td>DecisionTreeClassifier</td>
      <td>0.764749</td>
      <td>0.003838</td>
    </tr>
    <tr>
      <th>18</th>
      <td>ExtraTreeClassifier</td>
      <td>0.757486</td>
      <td>0.002228</td>
    </tr>
    <tr>
      <th>19</th>
      <td>LinearDiscriminantAnalysis</td>
      <td>0.794246</td>
      <td>0.003578</td>
    </tr>
    <tr>
      <th>20</th>
      <td>QuadraticDiscriminantAnalysis</td>
      <td>0.786983</td>
      <td>0.002294</td>
    </tr>
  </tbody>
</table>
</div>



It is interesting to se that the Boosting classifier performs the best. Boosting is a machine learning ensemble(it uses multiple learning algorithms) that often perform better then random forest. But it is also more time consuming.
