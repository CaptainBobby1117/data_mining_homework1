import pandas as pd
import csv
import numpy as np
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import sys
#导出控制台输出到日志文件中
log_print = open('完整实验结果(github数据集).log', 'w',encoding='utf8')
sys.stdout = log_print
sys.stderr = log_print


data = pd.read_csv('github_dataset.csv')#,index_col = 0)
print(data)
for column_name in ['repositories','stars_count','forks_count','issues_count','pull_requests','contributors','language']:
    #['IMDb-rating','appropriate_for','director','downloads','id','industry','language','posted_date','release_date','run_time','storyline','title','views','writer']:
    freq_counts = data[column_name].value_counts()
    print(column_name+' have freq_counts:'+str(freq_counts))
    # 计算五数概括等基本统计量
    basic_stats = data[column_name].describe()
    print(column_name+' have basic_stats:'+str(basic_stats))
    # 计算缺失值个数
    missing_count = data[column_name].isnull().sum()
    print(column_name+' have Missing count:', str(missing_count))

print(type(data[column_name]))
for i in range(4):
    if(i==3):
        data_tmp1 = data.drop(['repositories','language'], axis=1)#['appropriate_for','director','downloads','industry','language','posted_date','release_date','run_time','storyline','title','views','writer']
        data_tmp = data_tmp1#.drop('language', axis=1)
    # 读取数据文件
    data = pd.read_csv('github_dataset.csv')#,index_col = 0)
    print(type(data))
    print(data)
    #['stars_count','forks_count','issues_count','pull_requests','contributors']
    column_name_for_rating=['stars_count','forks_count','issues_count','pull_requests','contributors']#['IMDb-rating','id']
    #'repositories','stars_count','forks_count','issues_count','pull_requests','contributors','language'.for movies:IMDb-rating,appropriate_for,director,downloads,id,industry,language,posted_date,release_date,run_time,storyline,title,views,writer
    for column_name in ['repositories','stars_count','forks_count','issues_count','pull_requests','contributors','language']:



        # 1.将缺失部分删除
        if i==0:
            data = data.dropna()

        # 2.找到最高频率的值
        elif i==1:
            most_freq_value = data[column_name].value_counts().index[0]

        # 用最高频率值来填充缺失值
            data_fillna = data[column_name].fillna(most_freq_value)

        # 3.通过属性的相关关系来填补缺失值
        elif i == 2:
            correlation_matrix = data.corr()
            print("correlation_matrix:",correlation_matrix)
            for column in column_name_for_rating:
                for column_with_missing_values in column_name_for_rating:
                    if correlation_matrix[column][column_with_missing_values] > 0.5:
                        data[column_with_missing_values].fillna(data[column].mean(), inplace=True)

        # 通过数据对象之间的相似性来填补缺失值

        elif i==3:
            #KNNImputer这是整体的数据对象相似度处理，但字符串转换不到float，只能把两列暂时去掉进行处理
            print(data.columns)
            print(data)
            print(type(data))

            print(data_tmp)
            print(type(data_tmp))
            imputer = KNNImputer(n_neighbors=3)
            data = pd.DataFrame(imputer.fit_transform(data_tmp.values),columns=['stars_count','forks_count','issues_count','pull_requests','contributors'])
            print(data)


            if  column_name in column_name_for_rating:
                # 统计频数
                freq_counts = data[column_name].value_counts()
                print(column_name + ' have freq_counts:' + str(freq_counts)+' in the '+str(i)+' method')
                # 计算五数概括等基本统计量
                basic_stats = data[column_name].describe()
                print(column_name + ' have basic_stats:' + str(basic_stats)+' in the '+str(i)+' method')
                # 计算缺失值个数
                missing_count = data[column_name].isnull().sum()
                print(column_name + ' have Missing count:', str(missing_count)+' in the '+str(i)+' method')
                print(type(data[column_name]))
        if (i != 3):       #第3列的data是少列的，所以要单独讨论
            # 统计频数
            freq_counts = data[column_name].value_counts()
            print(column_name + ' have freq_counts:' + str(freq_counts)+' in the '+str(i)+' method')
            # 计算五数概括等基本统计量
            basic_stats = data[column_name].describe()
            print(column_name + ' have basic_stats:' + str(basic_stats)+' in the '+str(i)+' method')
            # 计算缺失值个数
            missing_count = data[column_name].isnull().sum()
            print(column_name + ' have Missing count:', str(missing_count)+' in the '+str(i)+' method')

            print(type(data[column_name]))
        # 绘制直方图
        if column_name!='language' and column_name!='repositories' and column_name in column_name_for_rating and not isinstance(data[column_name].iloc[1], str) :
            plt.hist(data[column_name], bins=10)
            plt.title('The ' + str(i + 1) + ' th method:' + column_name + ":hist graph")
            plt.show()
        # TypeError: '<='not supported between instances of 'float' and 'str
        # 绘制盒图
        if column_name!='language' and column_name!='repositories' and column_name in column_name_for_rating and not isinstance(data[column_name].iloc[1], str) :
            plt.boxplot((data[column_name]))
            plt.title('The ' + str(i + 1) + ' th method:' + column_name + ":boxplot graph")
            plt.show()
    # 对比新旧数据集的差异
    print('data'+str(i+1),data.shape)





