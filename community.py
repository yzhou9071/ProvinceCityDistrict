#!/usr/bin/python
#!/usr/bin/env python
from xml.etree import ElementTree

provinceList = {}
root = ElementTree.fromstring(open("Provinces.xml").read())
lst_node = root.getiterator("Province")
for node in lst_node:
	if int(node.attrib['ID']) < 10 :
		provinceList['0' + node.attrib['ID']] = node.attrib['ProvinceName']
	else:
		provinceList[node.attrib['ID']] = node.attrib['ProvinceName']

cityList = {}
root = ElementTree.fromstring(open("Cities.xml").read())
lst_node = root.getiterator("City")
for node in lst_node:
	if int(node.attrib['PID']) < 10:
		pid = '0' + node.attrib['PID']
	else:
		pid = node.attrib['PID']
	if int(node.attrib['ID']) < 10 :
		cityList['00' + node.attrib['ID']] = [pid, node.attrib['CityName']]
	elif int(node.attrib['ID']) < 100 :
		cityList['0' + node.attrib['ID']] = [pid, node.attrib['CityName']]
	else:
		cityList[node.attrib['ID']] = [pid, node.attrib['CityName']]

districtList = {}
root = ElementTree.fromstring(open("Districts.xml").read())
lst_node = root.getiterator("District")
for node in lst_node:
	if int(node.attrib['CID']) < 10 :
		cid = '00' + node.attrib['CID']
	elif int(node.attrib['CID']) < 100 :
		cid = '0' + node.attrib['CID']
	else:
		cid = node.attrib['CID']
	if int(node.attrib['ID']) < 10 :
		districtList['000' + node.attrib['ID']] = [cid, node.attrib['DistrictName']]
	elif int(node.attrib['ID']) < 100 :
		districtList['00' + node.attrib['ID']] = [cid, node.attrib['DistrictName']]
	elif int(node.attrib['ID']) < 1000 :
		districtList['0' + node.attrib['ID']] = [cid, node.attrib['DistrictName']]
	else :
		districtList[node.attrib['ID']] = [cid, node.attrib['DistrictName']]

sqlWrite = open('community.sh','w+')
dataLine = '#!/bin/sh\n'
sqlWrite.write(dataLine)
dataLine = 'DBNAME=\"ejieCommunity\"\n'
sqlWrite.write(dataLine)
dataLine = 'USER=\"root\"\n'
sqlWrite.write(dataLine)
dataLine = 'PASSWD=\"yzhou9071\"\n'
sqlWrite.write(dataLine)


dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"create table if not exists provinceList(provinceID varchar(2) not null, provinceName varchar(256) not null,primary key(provinceID))\"\n'
sqlWrite.write(dataLine)
for provinceID in provinceList:
	dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"insert into provinceList(provinceID,provinceName) values(\\\"'+provinceID+'\\\",\\\"'+provinceList[provinceID].encode('utf-8')+'\\\")\"\n'
	sqlWrite.write(dataLine)

dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"create table if not exists cityList(cityID varchar(3) not null, cityName varchar(256) not null, provinceID varchar(2) not null, primary key(cityID))\"\n'
sqlWrite.write(dataLine)
for cityID in cityList:
	dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"insert into cityList(cityID,cityName,provinceID) values(\\\"'+cityID+'\\\",\\\"'+cityList[cityID][1].encode('utf-8')+'\\\",\\\"'+cityList[cityID][0]+'\\\")\"\n'
	sqlWrite.write(dataLine)

dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"create table if not exists districtList(districtID varchar(4) not null, districtName varchar(256) not null, cityID varchar(3) not null,primary key(districtID))\"\n'
sqlWrite.write(dataLine)
for districtID in districtList:
	dataLine = 'mysql -u${USER} -p${PASSWD} ${DBNAME} -e\"insert into districtList(districtID,districtName,cityID) values(\\\"'+districtID+'\\\",\\\"'+districtList[districtID][1].encode('utf-8')+'\\\",\\\"'+districtList[districtID][0]+'\\\")\"\n'
	sqlWrite.write(dataLine)

sqlWrite.close()
