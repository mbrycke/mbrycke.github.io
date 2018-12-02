---
layout: post
title: Random Forest Part 2
---
## Random Forest applied to a big dataset.
We will continue using random forest, but this time  we will use it for regression analysis (as compared to classification in the Titanic data set). We will use the data from the kaggle competition [Corporación_Favorita_Grocery_Sales_Forecasting] (https://www.kaggle.com/c/favorita-grocery-sales-forecasting) This dataset is much larger so we will have to use different techniques handling this, unless we an powerfull computer and alot of memory.



```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import model_selection
import re
import warnings; warnings.simplefilter('ignore')
from IPython.display import display, Markdown
import numpy as np
```


```python
#%%time
#df_train=pd.read_csv('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/train.csv')
#df_test=pd.read_csv('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/test.csv')
```

Now, if we read train.csv like above it will not only take a long time but also use a lot of memory. If you're on a local workstation you might actually run out of memory. If you use the setting 'low_memory=False' you will most certanly run out of memory. We can reduce the size of the dataframe by specifying what datatypes different columns should have. You can study what data-types are appropriate by listing a few lines of the file in bash with the `head ` or `less` command.


```python
types={'id':'int64', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32','onpromotion':'object'}
```


```python
%%time
df_train = pd.read_csv('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/train.csv', parse_dates=['date'], dtype=types, infer_datetime_format=True)
```

    CPU times: user 1min 52s, sys: 5.69 s, total: 1min 58s
    Wall time: 1min 58s



```python
df_train.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 125497040 entries, 0 to 125497039
    Data columns (total 6 columns):
    id             int64
    date           datetime64[ns]
    store_nbr      int8
    item_nbr       int32
    unit_sales     float32
    onpromotion    object
    dtypes: datetime64[ns](1), float32(1), int32(1), int64(1), int8(1), object(1)
    memory usage: 3.9+ GB



```python
%time df_train.describe(include='all') #include='all' makes it also process 'date'
```

    CPU times: user 32 s, sys: 5.75 s, total: 37.8 s
    Wall time: 37.8 s





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
      <th>id</th>
      <th>date</th>
      <th>store_nbr</th>
      <th>item_nbr</th>
      <th>unit_sales</th>
      <th>onpromotion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1.254970e+08</td>
      <td>125497040</td>
      <td>1.254970e+08</td>
      <td>1.254970e+08</td>
      <td>1.254970e+08</td>
      <td>125497040</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>NaN</td>
      <td>1684</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>top</th>
      <td>NaN</td>
      <td>2017-07-01 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>False</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>NaN</td>
      <td>118194</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>96028767</td>
    </tr>
    <tr>
      <th>first</th>
      <td>NaN</td>
      <td>2013-01-01 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>last</th>
      <td>NaN</td>
      <td>2017-08-15 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>6.274852e+07</td>
      <td>NaN</td>
      <td>2.746458e+01</td>
      <td>9.727692e+05</td>
      <td>8.554856e+00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>std</th>
      <td>3.622788e+07</td>
      <td>NaN</td>
      <td>1.633051e+01</td>
      <td>5.205336e+05</td>
      <td>2.360515e+01</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000e+00</td>
      <td>NaN</td>
      <td>1.000000e+00</td>
      <td>9.699500e+04</td>
      <td>-1.537200e+04</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.137426e+07</td>
      <td>NaN</td>
      <td>1.200000e+01</td>
      <td>5.223830e+05</td>
      <td>2.000000e+00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>6.274852e+07</td>
      <td>NaN</td>
      <td>2.800000e+01</td>
      <td>9.595000e+05</td>
      <td>4.000000e+00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>9.412278e+07</td>
      <td>NaN</td>
      <td>4.300000e+01</td>
      <td>1.354380e+06</td>
      <td>9.000000e+00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1.254970e+08</td>
      <td>NaN</td>
      <td>5.400000e+01</td>
      <td>2.127114e+06</td>
      <td>8.944000e+04</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



The dataframe now uses 3.9 gb of memory. The reason for using 'object' as datatype on the 'onpromotion' columns is because this column is a boolean but has missing values. So we need to deal with the missing values before we can turn it into a boolean. Exploratory analysis shows that missing values probably means 'False' i.e. not in promotion.
So, let's set missing values to False. Also, 'True' and 'False' in the column are now represented as strings. Lets change them to booleans.


```python
#how many missing values:
len(df_train['onpromotion'][df_train['onpromotion'].isnull()])
```




    21657651



Replace missing values in column 'onpromotion'


```python
df_train['onpromotion'].fillna(value=False, inplace=True) # inplace=True means that this operation is applied directly to dataframe
```

Changing strings 'True' and 'False' into booleans `True` and `False`.


```python
df_train['onpromotion']=df_train['onpromotion'].map({'False':False, 'True':True}) #'True' and 'Fasle' are stored as strings. Change to booleans.
df_train['onpromotion']=df_train['onpromotion'].astype(bool) #Cast column to boolean
```

We can se that 'onpromotion' is now a boolean. Also, the dataframe takes up almost 1 GB less memory


```python
df_train.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 125497040 entries, 0 to 125497039
    Data columns (total 6 columns):
    id             int64
    date           datetime64[ns]
    store_nbr      int8
    item_nbr       int32
    unit_sales     float32
    onpromotion    bool
    dtypes: bool(1), datetime64[ns](1), float32(1), int32(1), int64(1), int8(1)
    memory usage: 3.0 GB


## Test set
Let's read in the test set in the same way as the train set


```python
%%time
df_test=pd.read_csv('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/test.csv',parse_dates=['date'], dtype=types, infer_datetime_format = True)
df_test['onpromotion'].fillna(value=False, inplace=True)
df_test['onpromotion']=df_test['onpromotion'].map({'False':False, 'True':True})
df_test['onpromotion']=df_test['onpromotion'].astype(bool)
```

    CPU times: user 3.24 s, sys: 39.6 ms, total: 3.28 s
    Wall time: 3.28 s



```python
df_test.describe(include='all')
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
      <th>id</th>
      <th>date</th>
      <th>store_nbr</th>
      <th>item_nbr</th>
      <th>onpromotion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3.370464e+06</td>
      <td>3370464</td>
      <td>3.370464e+06</td>
      <td>3.370464e+06</td>
      <td>3370464</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>NaN</td>
      <td>16</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2</td>
    </tr>
    <tr>
      <th>top</th>
      <td>NaN</td>
      <td>2017-08-27 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>False</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>NaN</td>
      <td>210654</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3171867</td>
    </tr>
    <tr>
      <th>first</th>
      <td>NaN</td>
      <td>2017-08-16 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>last</th>
      <td>NaN</td>
      <td>2017-08-31 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1.271823e+08</td>
      <td>NaN</td>
      <td>2.750000e+01</td>
      <td>1.244798e+06</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>std</th>
      <td>9.729693e+05</td>
      <td>NaN</td>
      <td>1.558579e+01</td>
      <td>5.898362e+05</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.254970e+08</td>
      <td>NaN</td>
      <td>1.000000e+00</td>
      <td>9.699500e+04</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.263397e+08</td>
      <td>NaN</td>
      <td>1.400000e+01</td>
      <td>8.053210e+05</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.271823e+08</td>
      <td>NaN</td>
      <td>2.750000e+01</td>
      <td>1.294665e+06</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1.280249e+08</td>
      <td>NaN</td>
      <td>4.100000e+01</td>
      <td>1.730015e+06</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1.288675e+08</td>
      <td>NaN</td>
      <td>5.400000e+01</td>
      <td>2.134244e+06</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



## Handling the negativ unit_sales
Negativ unit sales are returns. In fact, in this kaggle competition it states that negativs could be considered 0.


```python
df_train['unit_sales'][df_train['unit_sales']<0]=0 #setting negative values to 0
```


```python
#### Or shorter ####
#max_unit_sales=df_train['unit_sales'].max() #Returns the maximum value in the column
# df_train['unit_sales']=np.log1p(np.clip(df_train['unit_sales'], 0,max_unit_sales, out=None))
```

## Log of unit_sales
We want to predict unit sales why we need to compare prediction vs actual value. However, we are interested in the relative error and not absolute error. In other words, if the prediction is off by 10 if the sought value is 10000 that is pretty good. However, to be off by 10 if the sought value is 8 is terrible. Therefore we use the quotient (percentage) of error instead. I nice way to handle this is to take the log values of the unit sales. Then we will automatically get the 'percentage' of error due to this relationship:


```latex
%%latex
$\log(\frac{a}{b})=\log(a)-\log(b)$
```


$\log(\frac{a}{b})=\log(a)-\log(b)$



Actually we do not take the log value but the numpy function log1p which is 'log one plus' i.e. log(x+1) instead of log(x). This is due to unit sales includes 0. Log(0) is of course impossible


```python
df_train['unit_sales']=np.log1p(df_train['unit_sales'])
```

#### Feather-format
The feather-format is a rather new method of saving data to disk. It saves the data in a very similar form as how it is stored in RAM. In that way this format has very short saving and reading time. Let's save the dataframe df_train.


```python
df_train.to_feather('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/df_train')
```

#### Split into train set and validation set
In the Titanic dataset we used model_selection.train_test_split (from sklearn). However, this splits the set randomly. Here we would like more control since we have a series of data. The test set begins where the train set ends why we should construct our validation set in the same fashion. Why do we need a validation set. It is true that random forest isn't prone to overfitting but even so we usually always want a validation set to evaluate the model. In fact, choosing a validation set isn't trivial. If possible, we should compare how the models score on the validation set and test set for a few different models. Then we are able to see if the validation score and test score are somewhat lineary depent. After concluding that validation set and test set are somewhat in agreement as to the accuracy of the model, we have a good validation set to test out our model on.


```python
def train_validation_split(dataframe, n):
    return dataframe[:n].copy(),dataframe[n:].copy()
    
```


```python
df_train_set, df_validation_set=train_validation_split(df_train,len(df_train)-len(df_test))
```

#### Handling date column?
The date column is of course important when predicting sales. The date contains info about week day, season, etc. We will se how we can handle this in a later blog post. For now we will just ignore this column


```python
%%time
x_train=df_train_set[['store_nbr', 'item_nbr', 'onpromotion']] 
y_train=df_train_set[['unit_sales']] 
df_validation_set.reset_index(inplace=True) #we need to reset index in order to be able to save the variable in the feather format.
x_val=df_validation_set[['store_nbr', 'item_nbr', 'onpromotion']] 
y_val=df_validation_set[['unit_sales']] 

```

    CPU times: user 905 ms, sys: 205 ms, total: 1.11 s
    Wall time: 1.12 s


### Saving train and validation sets.


```python
x_train.to_feather('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/x_train')
y_train.to_feather('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/y_train')
x_val.to_feather('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/x_val')
y_val.to_feather('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/y_val')
```

### Importing train and validation sets.


```python
import feather
x_train=feather.read_dataframe('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/x_train')
y_train=feather.read_dataframe('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/y_train')
x_val=feather.read_dataframe('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/x_val')
y_val=feather.read_dataframe('/home/mattias/Documents/ml_data/kaggleGroceryFavorita/data/y_val')
```

## Handling a big dataset
If we just train a random forest on our dataset with more than 120 miljon rows it would take a lot of time and use a lot of memory. What we will do is to train with a sub-sample. We also train each tree with a different random sub-sample. In that way each tree will contain an error but the errors will be indepent of each other. The mean error of several independent errors will become smaller and smaller.

#### Tip if you have limited RAM
If you have stored several large dataframes in memory and are about to start to train your model it might be a good idea to clear all unnessesary dataframes. In fact, you can restart the kernel and read the dataframes (in this case stored in the feather format) which are necessare.


```python
from sklearn.ensemble import forest

def set_rf_samples(n):
    """ Changes Scikit learn's random forests to give each tree a random sample of
    n random rows.
    """
    forest._generate_sample_indices = (lambda rs, n_samples:
        forest.check_random_state(rs).randint(0, n_samples, n))

def reset_rf_samples():
    """ Undoes the changes produced by set_rf_samples.
    """
    forest._generate_sample_indices = (lambda rs, n_samples:
        forest.check_random_state(rs).randint(0, n_samples, n_samples))
```

#### Give each random forest a random sample of 100000 rows:


```python
set_rf_samples(100000)
```

#### Creating the model:


```python
m=RandomForestRegressor(n_estimators=20, min_samples_leaf=100, n_jobs=-1)
```

#### Train the model:


```python
%time m.fit(x_train, y_train)
```

    CPU times: user 41.6 s, sys: 13.2 s, total: 54.8 s
    Wall time: 31.4 s





    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
               max_features='auto', max_leaf_nodes=None,
               min_impurity_decrease=0.0, min_impurity_split=None,
               min_samples_leaf=100, min_samples_split=2,
               min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1,
               oob_score=False, random_state=None, verbose=0, warm_start=False)




```python
def rmse(x,y): return np.sqrt(((x-y)**2).mean(axis=1))

def printscore(m,x_val, y_val):
    res = rmse(m.predict(x_val), np.array(y_val))
    print('RMSE:',res)
```

### Estimating the accuracy of the model
We will use the root mean square error 


```python
printscore(m,x_val,y_val.T)
```

    RMSE: [0.79900886]

