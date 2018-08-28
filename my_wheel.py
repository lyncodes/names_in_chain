import pandas as pd


def freq(data=None, variable=None, dropna=False):
    """
    Description:
    this function: freq, stands for frequency, which will calculate each unique value of a variable in a Pandas DataFrame.
    
    Parameters：
    data: A Pandas DataFrame  (required)
    
    variable: Default None
                A Python List,if not given, will output the frequency of each vaiables
                if supplied, will output the frequency of variable specified.
    
    dropna: Boolean, default False
            if False, will count as the NaN values
    return:
            DataFrame     
    描述:
    这个函数将会输出一个Pandas DataFrame的所有变量中，变量值出现的频数    
    
    参数：
    data: 一个Pandas DataFrame  (必须填写)
    
    variable: 默认为空， 一个python list，如果不提供，将会计算所有的变量的频数，如果提供，则会计算所提供的变量的频数。

    dropna: 布尔, 默认为False，如果为Fasle，则将NaN包含在计算中，否则不包含。

    返回：
        DataFrame   
    """
    frequency = pd.DataFrame()
    if data is None:
        raise TypeError('Please supply a DataFrame')
    elif variable is None:
        for i in list(data.columns):
            tmp = data[i].value_counts(dropna=False).to_frame().reset_index()
            tmp.columns = [i,'count of '+i]
            frequency = pd.concat([frequency,tmp], axis=1, sort=True)

    else:
        for i in variable:
            tmp = data[i].value_counts(dropna=False).to_frame().reset_index()
            tmp.columns = [i,'count of '+i]
            frequency = pd.concat([frequency,tmp], axis=1, sort=True)
    return frequency
