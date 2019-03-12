import mysql.connector as mysql
import re
import math


def strCheck(index, shapeStr):
    # 对shapeStr的格式判断
    shapeList = shapeStr.split(';')
    for point in shapeList:
        pointList = point.strip().replace(' ', '').split(',')
        if len(pointList) == 2:  # 正确经纬度格式-数值判断
            reValue = re.compile(r'^[-+]?[0-9]+\.?[0-9]+$')
            lonBool = reValue.match(pointList[0])
            latBool = reValue.match(pointList[1])
            if (lonBool and latBool):  # 经纬度中类型正确
                if float(pointList[0]) < -180 or float(pointList[0]) > 180 or float(pointList[1]) < -90 or float(
                        pointList[1]) > 90:
                    print(point + '数值错误' + str(index))
                    shapeList.remove(point)
            else:  # 经纬度数据类型错误
                print(point + '类型错误' + str(index))
                shapeList.remove(point)
        else:  # 经纬度格式错误-抛弃
            print(point + '格式错误' + str(index))
            shapeList.remove(point)
    # 判断首尾是否相同
    before = shapeList[0]
    end = shapeList[-1]
    if end != before:
        shapeList[-1] = before
        print("首尾不相同" + str(index))
    shapeTmp = ';'.join(shapeList)
    # 判断shapeTmp是否能形成一个圈
    return shapeTmp



conn = mysql.connect(host="      ", port="3306", user="      ", passwd="      ", db="       ")
cursor = conn.cursor()
sql1 = "select id,name,shape from china_city_new "
cursor.execute(sql1)
results = cursor.fetchall()
flagFile = 'D:/work/shape/flagFile111.txt'
fileWriter = open(flagFile, "a")
num = 0
for data in results:
    if ";" in data[2]:
        if len(data[2].split(";")) < 2:
            print(str(data[0]) + "点")
        elif len(data[2].split(";")) < 3:
            print(str(data[0]) + "线段")
            # square = line2squre(data[2])
        else:
            shapeNew = strCheck(data[0], data[2].strip())
            #sql2 = "update re_gould_geographic_info_copy set shape= %s where id= %s"
            #sql2 = "update gould_geographic_info_20190211_copy set shape= %s where id= %s"
            sql2 = "update china_city_new set shape= %s where id= %s"
            params = (shapeNew, data[0])
            if shapeNew != data[2]:
                print(data[0])
                cursor.execute(sql2, params)
    else:
        fileWriter.write(str(data[0]) + '\n')
    #print("验证完成")
fileWriter.close()
conn.commit()
cursor.close()
conn.close()
