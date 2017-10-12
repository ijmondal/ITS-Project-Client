# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import requests
#from .models import *
import json,urllib2
#from django.utils import simplejson
from datetime import datetime
import tempfile

def wellData():
	response3 = urllib2.urlopen("http://10.0.3.23:8025/agrophotos/get")
        jsonData3 = json.load(response3) 


        well_resp =urllib2.urlopen("http://10.0.3.23:8025/agrowells/get")
        jsonData_well = json.load(well_resp)

        yield_resp = urllib2.urlopen("http://10.0.3.23:8025/agroyields/get")
        jsonData_yield = json.load(yield_resp)

        locationRecordList1 =[]
        depthList = []
        photoList = []
        wellYield = {}
        avgYield = []
	
        for record in jsonData_yield:
                if record['Well_Id'] in wellYield.keys():
                        wellYield[ record['Well_Id'] ].append( float(record['Yield_Measure']) )
                else:
                        wellYield[ record['Well_Id'] ] = [float(record['Yield_Measure'])]

        i = 1
        for record in jsonData_well:
                locIndex = record['Location_Id'].index('(')
                locationStr = record['Location_Id'][locIndex+1:-1]
                location = locationStr.split(' ')
                locationRecordList1.append(float(location[0]))
                locationRecordList1.append(float(location[1]))

                for rec in jsonData3:
                        if rec['ID'] == record['Photo_Id']:
                                photoList.append('http://10.0.3.23:8025'+rec['Photo'])

                depthList.append(record['Depth'])
                temp = reduce(lambda x,y: x+y, wellYield[i])
                avgYield.append( float(temp)/len(wellYield[i]) )
                i+=1

	return {'depthList':depthList, 'locationRecordList1':locationRecordList1, 'photoList':photoList, 'wellYield':wellYield, 'avgYield':avgYield}

def viewHouseholds(request):

	response = urllib2.urlopen("http://10.0.3.23:8025/agrohouseholds/get")
        jsonData = json.load(response)
        locationRecordList =[]
        householdIdList = []
        monthlyIncomeList = []
        for record in jsonData:
                locIndex = record['Location_Id'].index('(')
                locationStr = record['Location_Id'][locIndex+1:-1]
                location = locationStr.split(' ')
                locationRecordList.append(float(location[0]))
                locationRecordList.append(float(location[1]))
                householdIdList.append(int(record['ID']))
                monthlyIncomeList.append(record["Monthly_Income"])

        response1 = urllib2.urlopen("http://10.0.3.23:8025/agrofarms/get")
        jsonData1 = json.load(response1)
        areaList = []
        farmIdList = []
        PointsList = []
        end = ['\n']
        for record in jsonData1:
                areaList.append(float(record['Area']))
                farmIdList.append(record['ID'])
                start_b = record['Points'].index('(')+2
                end_b = record['Points'].index(')')
                tempList = map(lambda x: x.split(' '),record['Points'][start_b:end_b].split(','))
                for t in tempList:
                        if '' in t:
                                t.remove('')
                for t in tempList:
                        t[0] = float(t[0])
                        t[1] = float(t[1])
                PointsList.append(tempList)

        response2 = urllib2.urlopen("http://10.0.3.23:8025/agromembers/get")
        jsonData2 = json.load(response2)

        response3 = urllib2.urlopen("http://10.0.3.23:8025/agrophotos/get")
        jsonData3 = json.load(response3) 
        
	# Get data related to wells such as depth, and average yield

	wells = wellData()

        FamilyList=[]
	FamilysizeList=[]
        for i  in range(0,len(householdIdList)):
                MemberList=[]
                MemberList.append(householdIdList[i])
                for record in jsonData2:
                    for record1 in jsonData3:
                        if record['HouseHold_Id']==householdIdList[i] and record1['ID']==record['Photo_Id']:
                            MemberList.append(record['Name'].decode("utf8") )
                            date1=record['DOB'].split('T')
                            MemberList.append(date1[0].decode())
                            MemberList.append('http://10.0.3.23:8025'+record1['Photo'])
                if MemberList!=[]:
		    FamilysizeList.append((len(MemberList))/3)
                    FamilyList.append(MemberList)

        response6 = urllib2.urlopen("http://10.0.3.23:8025/agrovideos/get")
	jsonData6 = json.load(response6)
        SeasonList=[]
        CropList=[]
        FarmIdList=[]
        videos=[]
	for video in jsonData6:
		temp=[]
		temp.append(video['Household_Id'])
		temp.append(video['Video_Clip'])
		videos.append(temp)
        '''for record in jsonData5:
            l=[]
            l.append(record['ID'])
            l.append(record['SeasonName'])
            l.append('http://10.0.3.23:8025'+record['SeasonPhoto'])
            SeasonList.append(l)
        for record in jsonData4:
            FarmIdList.append(record['Farm_Id'])'''

        '''for i in range(0,len(list(set(FarmIdList)))):
            farm=[]
            farm.append(record['Farm_Id'])
            for record in jsonData4:
                if record['Farm_Id']==FarmIdList[i]:
                    farm.append(record['Season_Id'])
                    farm.append(record['CropName'])
            if len(farm)!=1:
                CropList.append(farm)'''
	
	'''
	response_crop = urllib2.urlopen("http://10.0.3.23:8025/agrofarms/get")
	jsonData_crop = json.load(response_crop)
	croplist1=[]
	for loccrop1 in jsonData_crop:
		croplist1.append(loccrop1['Points'][0])


        '''
#added
	response = urllib2.urlopen("http://10.0.3.23:8025/agrofarms/get")
        jsonData_crop = json.load(response)
        croplist1=[]
        farmSeqPoints=[]
        for cropOfFarm in jsonData_crop:
                data=cropOfFarm['Points']
                data = cropOfFarm['Points'].strip('SRID=4326;POLYGON ((')
                data = data.strip('))')
                data1=data
                seqPnts = data.split(',')
                temp=[]
                farm_points=[]
                for item in seqPnts:
                        temp.append(item.split(' '))
                for it in temp:

                        for i in it:
                                if i=='':
                                        it.remove(i)
                        print it[0],it[1],it
                        farm_points.append([float(it[0]),float(it[1])])
                farmSeqPoints.append(farm_points)

                data1 = data1.split(',')[0]
                data1 = data1.split(' ')
                farm_location=[]
                for item in data1:
                        farm_location.append(float(item))
                croplist1.append(farm_location)
	



        template=loader.get_template('itstask22/map.html')                         
        context={'locationRecordList':wells['locationRecordList1'],'yieldList':json.dumps(wells['avgYield']),'depthList':json.dumps(wells['depthList']), 'photoList':json.dumps(wells['photoList']), 'householdLocation':locationRecordList,'householdId':householdIdList,'monthly_income':monthlyIncomeList,'FarmPoints':PointsList,'PersonalData':json.dumps(FamilyList),'seasonlist':json.dumps(SeasonList),'croplist':json.dumps(CropList),'videolist':json.dumps(videos),'Familysizelist':json.dumps(FamilysizeList),'location':croplist1,'farmSeqPoints':farmSeqPoints}
#	return HttpResponse(avgYield[1])
        return HttpResponse(template.render(context,request))	
       
def CropsDistribution(request):
	response = urllib2.urlopen("http://10.0.3.23:8025/agrofarms/get")
	jsonData_crop = json.load(response)
	croplist1=[]
	farmSeqPoints=[]
        for cropOfFarm in jsonData_crop:
		data=cropOfFarm['Points']
		data = cropOfFarm['Points'].strip('SRID=4326;POLYGON ((')
		data = data.strip('))')
		data1=data
		seqPnts = data.split(',')
		temp=[]
		farm_points=[]
		for item in seqPnts:
			temp.append(item.split(' '))
		for it in temp:
			
			for i in it:
				if i=='':
					it.remove(i)
			print it[0],it[1],it
			farm_points.append([float(it[0]),float(it[1])])
		farmSeqPoints.append(farm_points)	
		
        	data1 = data1.split(',')[0]
		data1 = data1.split(' ')
		farm_location=[]
		for item in data1:
			farm_location.append(float(item))
		croplist1.append(farm_location)
	context={'location':croplist1,'farmSeqPoints':farmSeqPoints}
	template=loader.get_template('itstask22/map_crops.html')
 
	return HttpResponse(template.render(context,request))
