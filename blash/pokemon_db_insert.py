import csv
from pymongo import MongoClient

client=MongoClient('localhost',27017)
template=client['template']
pokemon=template['pokemon']


csv_file = '/Users/minjingli/Desktop/pragmatism-python/数据分析/level2/data_pd/pokemon.csv'

def read_csv():
    f=open(csv_file,'r')
    reader=csv.DictReader(f)
    return [info for info in reader]


for info in read_csv():
    types=[]
    name=info['Name']
    if info['Type_1']:
        types.append(info['Type_1'])
    if info['Type_2']:
        types.append(info['Type_2'])
    rate=info['Total']
    desc=info['Body_Style']
    data={
        'name':name,
        'types':types,
        'rate':rate,
        'desc':desc
    }
    print(data)
    pokemon.insert_one(data)