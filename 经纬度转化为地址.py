import requests
import json
import pandas as pd
from pandas import Series, DataFrame

def locationToAddress(location):
    """
    将经纬度转换为地址
    所以选用的是逆地理编码的接口
    :param location: 经纬度，格式为 经度+','+维度，例如:location='116.323294,39.893874'
    :return:返回地址所在区，以及详细地址
    """
    parameters = {
                    'location': location,
                    'key': '689e4cd9c9ef6b3f2bac08904e31a3be'
                 }
    base = 'http://restapi.amap.com/v3/geocode/regeo?'
    response = requests.get(base, parameters)
    answer = response.json()  #.encode('gbk','replace')

    return answer['regeocode']['addressComponent']['district'],answer['regeocode']['formatted_address']


if __name__ == '__main__':

    print('转化进行中请稍等...')
    df = pd.read_excel('List.xlsx', sheet_name = 0)
    lst = list(df['longitude,latitude']) 

    #转换存入空列表newlst
    newlst = []    
    for i in lst:
        location = i
        newlst.append(locationToAddress(i))

    #存入的列表转换为Series
    #Series再转换为DataFrame数据的最后一列
    Ser = Series(newlst, name='Address')
    df = pd.concat([df, Ser], axis=1)

    #df.drop('Unnamed: 2', axis=1, inplace=True)
    df.columns = ['Name', '经纬度坐标', '经度', '纬度', '地址']
    df.to_csv('Outfile.csv', encoding='gbk', index=False)
    print('转化完成！')