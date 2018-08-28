import pandas as pd
import numpy as np
import itertools
import math


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
        DataFrame contains:
        1. the unique values
        2. the count of the unique values
        3. the percentage of the unique values
    """
    frequency = pd.DataFrame()
    if data is None:
        raise TypeError('Please supply a DataFrame')
    elif variable is None:
        # If variable is None, output all variables' frequency.
        for i in list(data.columns):
            count = data[i].value_counts(dropna=False).to_frame()
            percent = data[i].value_counts(normalize=True, dropna=False).to_frame()*100
            tmp = pd.concat([count,percent], axis=1).reset_index()
            tmp.columns = [i,'cnt of '+i, 'pct of '+i]
            frequency = pd.concat([frequency,tmp], axis=1, sort=True)

    else:
        for i in variable:
            # calculate the given variables' frequency
            count = data[i].value_counts(dropna=False).to_frame()
            percent = data[i].value_counts(normalize=True, dropna=False).to_frame()*100
            tmp = pd.concat([count,percent], axis=1).reset_index()
            tmp.columns = [i,'cnt of '+i, 'pct of '+i]
            frequency = pd.concat([frequency,tmp], axis=1, sort=True)
    return frequency




def num_marker(data=None,variables=None,cutpoints=None,labels=None,inplace=False):
    """
    Description:
    this function: num_marker, stands for numerical data marker, which will map the different periods of number into several literal markers.
    =========================================================
    Parameters：
    data: A Pandas DataFrame  (required)
    
    variable: A Python list (required)
    
                contains the numerical variables need to be marked.
    
    cutpoints: 2-dimensional python list
                each element is the cutpoints for corresponding variables, the cutpoints and variables are One-to-one correspondence
    
    labels: 2-dimensional python list
                 each element is the labels will be atatched to the numerical data

    inplace: Boolean,defaul False
            if True ,the calculation process will change the initial dataframe,else will retuen a demo dataframe
    
    =========================================================
    Return:
            DataFrame if inplace is False

            Amendment DataFrame if inplace is True
    =========================================================
    描述:
    将Pandas DataFrame中的指定的数值型字段，根据给定切割点（cutpoints），映射到不同的标签（labels）上。
    =========================================================
    参数：
    data: 一个Pandas DataFrame  (必须填写)
    
    variable:一个python list，包含需要进行离散化的数值型变量

    cutpoints: 一个2维python list。
                example:[[1,2,3],[4,5,6]],其中的每一个子列表，代表相对应的变量的离散化切割点
    labels：一个2维python list。
                example:[['good','bad'],['A class','B class','C class']],其中的每一个子列表，代表相对应的变量的离散化之后的类别属性标记
    inplace：Boolean, default False
            如果为True，则直接在原DataFrame上进行操作
            如果为False，则返回variable中第一个变量的离散化后的结果（并不对原数据集进行改变）
    =========================================================
    返回：
        DataFrame
    """
    if data is None:
        raise TypeError('Please supply a DataFrame')
    elif variables is None:
        raise TypeError('Please supply a variables')
        for i in variables:
            if not np.issubdtype(data[i].dtype, np.number):
                # check the data in current Pandas Series is numeriacal or not
                raise TypeError('given variables contains non numerical data type(s)')

    elif cutpoints is None:
        raise TypeError('Please supply a cutpoints')
    elif labels is None:
        raise TypeError('Please supply a labels')

    else:
        pass
    combination = list(zip(variables,cutpoints,labels))
    # combine all elements together for futher indexing
    for i in combination:
        
        if not inplace:
            return pd.cut(data[i[0]],bins=i[1],labels=i[2]).to_frame()
        else:
            data[i[0]] = pd.cut(data[i[0]],bins=i[1],labels=i[2])


            

import itertools
def cart_prod(*args,deli='_'):
    """
    Description:
    generate cartesian product   
    =========================================================
    Parameters:

    *args: all elements should be string, not number

    delimeter: string,default '_',you can specify by yourself,such as '-','~',.....

    *args: iteratable,list,tuple,any iteratable sequence,such as ['1','2','3'],['A', 'B'], ['a', 'b']......
    =========================================================
    Return: The cartesian product
    =========================================================
    Example:

        IN[1]:
            cart_prod(['A', 'B'], ['a', 'b'],['1', '2'],['f','g'],deli='_') 
        OUT[1]:
            ['A_a_1_f','A_a_1_g','A_a_2_f','A_a_2_g','A_b_1_f','A_b_1_g','A_b_2_f',
            'A_b_2_g','B_a_1_f','B_a_1_g','B_a_2_f','B_a_2_g','B_b_1_f','B_b_1_g','B_b_2_f','B_b_2_g']     

        IN[2]:
            a = ['A', 'B']
            b = ['a', 'b']
            c = ['1', '2']
            d = ['f','g']

            cart_prod(a,b,c,d)

        OUT[2]:
            ['A_a_1_f','A_a_1_g','A_a_2_f','A_a_2_g','A_b_1_f','A_b_1_g','A_b_2_f',
            'A_b_2_g','B_a_1_f','B_a_1_g','B_a_2_f','B_a_2_g','B_b_1_f','B_b_1_g','B_b_2_f','B_b_2_g']  

    """ 
    cartesian_product = []
    for i in itertools.product(*args):
        # *args for many many variables will be supplied.
        cartesian_product.append(deli.join(i))  
    return cartesian_product




def chimerge(data=None, variable=None, target=None, threshold=3.8):
    """
    Description:
    This function can apply the chi_merge algorithm to auto optimal binning you table
    
    Reference Paper:http://sci2s.ugr.es/keel/pdf/algorithm/congreso/1992-Kerber-ChimErge-AAAI92.pdf
    =========================================================
    Parameters:
    data: A pandas tableframe
    
    varibale: string ,the variable choose to be discreted
    
    target: A pandas column name ,the taget variable which only support binary type(0 and 1)
            before apply the function, make sure the target variable contains 0 and 1 only.
    
    threshold: float, the threshold for chi-square test, this function is only for degree of freedom is one, 
                defalut as 2.7 for the 90% probability.
    
    =========================================================
    Return: Python List, the cutpoints of the optimal binning.

	example:

	chimerge(data=df,varible='age',target='overdue')

	return:
	[21,29,35,………………]



    """
    sort = data[variable].drop_duplicates().sort_values()
    sort.index = list(range(sort.shape[0]))
    sort = list(sort)

    if len(sort) <= 10:

        interval = []
        sub_interval = len(sort)//1
        sub_interval = int(sub_interval)
        j = 0
        while j < len(sort):
            tmp = []
            tmp.append(int(sort[j]))
            j += sub_interval
            if j < len(sort):
                tmp.append(int(sort[j]))
            else:
                tmp.append(int(sort[-1]))
            interval.append(tmp)
    elif len(sort) <= 20:
        interval = []
        sub_interval = len(sort)//2
        sub_interval = int(sub_interval)
        j = 0
        while j < len(sort):
            tmp = []
            tmp.append(int(sort[j]))
            j += sub_interval
            if j < len(sort):
                tmp.append(int(sort[j]))
            else:
                tmp.append(int(sort[-1]))
            interval.append(tmp)
            
    else:
        interval = []
        sub_interval = len(sort)//10
        sub_interval = int(sub_interval)
        j = 0
        while j < len(sort):
            tmp = []
            tmp.append(int(sort[j]))
            j += sub_interval
            if j < len(sort):
                tmp.append(int(sort[j]))
            else:
                tmp.append(int(sort[-1]))
            interval.append(tmp)
        
                   
    cutpoints = []
    for l in interval:
        cutpoints.append(l[0])
        cutpoints.append(l[-1])



    cutpoints = list(set(cutpoints))

    cutpoints.sort()


    return cutpoints

    def chi_value(a_positive,a_negative,b_positive,b_negative):
        a_row_sum = a_positive + a_negative
        b_row_sum = b_positive + b_negative
        a_column_sum = a_positive + b_positive
        b_column_sum = a_negative + b_negative

        total_sum = a_positive + a_negative + b_positive + b_negative

        positive_prob = a_column_sum/total_sum
        negative_prob = b_column_sum/total_sum

        exp_a_positive = a_row_sum * positive_prob
        exp_a_negative = a_row_sum * negative_prob
        exp_b_positive = b_row_sum * positive_prob
        exp_b_negative = b_row_sum * negative_prob

        chi_square_value = ((a_positive-exp_a_positive) ** 2)/exp_a_positive\
                                                                            + ((a_negative-exp_a_negative) ** 2)/exp_a_negative\
                                                                            + ((b_positive-exp_b_positive) ** 2)/exp_b_positive\
                                                                            + ((b_negative-exp_b_negative) ** 2)/exp_b_negative
        return chi_square_value

    chi_values = [1] * (len(interval) - 1)
    iter = 0
    while min(chi_values) < threshold:
    #     iter += 1
    #     print(iter)
        chi_values = []
        for k in range(len(interval) - 1):

            a_l = interval[k][0]
            a_r = interval[k][-1]

            b_l = interval[k + 1][0]
            b_r = interval[k + 1][-1]


            a_positive = data[(data[variable].between(a_l, a_r)) & (data[target] == 0)].shape[0] + 1
            a_negative = data[(data[variable].between(a_l, a_r)) & (data[target] == 1)].shape[0] + 1

            b_positive = data[(data[variable].between(b_l, b_r)) & (data[target] == 0)].shape[0] + 1
            b_negative = data[(data[variable].between(b_l, b_r)) & (data[target] == 1)].shape[0] + 1

    #         print(k)
    #         print(a_positive,a_negative,b_positive,b_negative)
            tmp = chi_value(a_positive,a_negative,b_positive,b_negative)
            chi_values.append(tmp)
        print(chi_values)
        mini_chi = min(chi_values)

        mini_position = chi_values.index(mini_chi)

        interval[mini_position] = interval[mini_position] + interval[mini_position + 1]
        interval.remove(interval[mini_position + 1])
    # interval

    cutpoints = []
    for l in interval:
        cutpoints.append(l[0])
        cutpoints.append(l[-1])
        
    cutpoints = list(set(cutpoints))
    cutpoints = cutpoints.sort()

    return cutpoints


def calc_iv(data=None, variables=None, target=None):
    """calculate the IV(information values) for given variables

    Parameters
    ----------
    data : Pandas DataFrame
        the dataset contains variables and target
    variables : iterable sequence, required
        the variables need to be calculated
    target : str, required
        the target of the dataset, must be binary values(map to 0 and 1 before use)
        
    Returns
    -------
    list
        a list of numbers contains
    """
    
    response = data[data[target] == 0].shape[0] + 1
    no_response = data[data[target] == 1].shape[0] + 1

    iv = {}

    for i in variables:

        iv_var = []
        for j in list(data[i].value_counts().index):

            sub_response = data[(data[i] == j) & (data[target] == 0)].shape[0] + 1

            sub_no_response = data[(data[i] == j) & (data[target] == 1)].shape[0] + 1

            woe_class = np.log((sub_response / response) / (sub_no_response / no_response))

            iv_class = ((sub_response / response) - (sub_no_response / no_response)) * woe_class

            iv_var.append(iv_class)
            
            tmp = sum(iv_var)

        iv[i] = tmp
    iv = pd.DataFrame(data=iv,index=[0])
    iv = iv.T
    iv = iv.reset_index()
    iv.columns = ['variables','IV_value']
    return iv





