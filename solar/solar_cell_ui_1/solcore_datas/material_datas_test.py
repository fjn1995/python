import pandas as pd

material_data = pd.read_csv("solcore_datas/SOPRA_DB_Updated.csv")
material_data = material_data.iloc[1:,1:2]
# print(material_data)
list =material_data.values.tolist()
material_datas = []
for i in range(len(list)):
    if list[i][0] not in  material_datas:   #列表数据去重
        material_datas.append(list[i][0])

print(material_datas)
print(len(material_datas))

dataframe = pd.DataFrame({'material_datas':material_datas})
dataframe.to_csv(r"solcore_datas/material_datas",index=False)


# 保存为TXT
# f = open("solcore_datas/sopra_db.txt",'r')
# for i in material_datas:
#     f.write(str(i)+'\n')
#     # f.write()
# f.close()
# data = f.readlines()
# datas=[]
# for i in data:
#     i=i.strip('\n')
#     datas.append(i)
#
# print(datas)