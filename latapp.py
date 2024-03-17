# from flask import Flask
# from pymongo import MongoClient
# from flask import jsonify, Flask, render_template, request

import pandas as pd
import numpy as np
import os
import glob
import json
 
import pprint
from json2html import *
from pymongo import MongoClient
from pathlib import Path
from flask import jsonify, Flask, render_template, request, send_file
from flask import Flask
import pdb
import ast
import os,subprocess
from bson.objectid import ObjectId
from itertools import chain
FILE_SYSTEM_ROOT =os.getcwd()

app = Flask(__name__)

arraylevels=[]
stdate=''
stdegr=''
studentid=''
levelst=''
stkeylevel=''
starraylevel={}
stlevelone=''
keydl=''
bflag=True
connection_string=os.environ.get('CONNECTION_STRING')
#client = MongoClient('localhost', 27017)
#client = MongoClient(connection_string)
client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.ps5mh8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Get and Post Route
bflag=True
db = client.hopedatabase
allstudents = db.datastudents
@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/data',methods=['GET'])
def data(): 
    # if request.method == 'POST':
    # CREATE
    # book: str = request.json['book']
    # pages: str = request.json['pages']

    # # insert new book into books collection in MongoDB
    # collection.insert_one({"book": book, "pages": pages})

    # return f"CREATE: Your book {book} ({pages} pages) has been added to your bookshelf.\n "

    # request.method == 'GET':
        # READ
    bookshelf = list(allstudents.find())
    novels = []

    for titles in bookshelf:
        firstname = titles['Firstname']
        lastname = titles['Lastname']
        shelf = {'book': firstname, 'pages': lastname}
        novels.insert(0, shelf)
    
    print(novels)
    return novels
    #pdb.set_trace()
    # if request.method == "POST":
    #     db = client.hopedatabase
    #     allstudents = db.datastudents 
    #     data=request.form.to_dict()
    #     print(data)
    #     allstudents.insert_one(data)
    #     return render_template('allstudent.html', students=allstudents.find({}))
    # else:   
    #     db = client.hopedatabase
    #     allstudents = db.datastudents 

    #     return render_template('allstudent.html', students=allstudents.find({}))

# @app.route('/printfill',methods=['POST','GET'])
# def printfill(): 
# #    pdb.set_trace()
#     db = client.hopedatabase
#     allstudents = db.datastudents
#     slkey=request.form.getlist('selkeys')
#     stkey=request.form['stkey']
#     stuid=request.form['stuid']
#     stlevel=request.form['stlevel']
#     stdegr=request.form['stdegr']
#     fromd=request.form['fromd']
#     tod=request.form['tod']
#     per=allstudents.find( { '_id':ObjectId(stuid)})
#            # pdb.set_trace()
#     result = []
#     for i in per :
#         result.append(i)
#     flatten_list=[]
#     category=[]
#     ee=[]
#     for skey in slkey:
#         li=list(chain.from_iterable(result[0][stlevel][stdegr][stkey][skey]))
        
#         for eachd in li:
#             if((eachd['Date'] >= request.form['fromd']) and (eachd['Date'] <= request.form['tod'])):
#                 eachd['subcat']=stkey 
#                 eachd['cat']=skey
#                 eachd['Firstname']=result[0]['Firstname']
#                 eachd['Lastname']=result[0]['Lastname']
#                 ee.append(eachd)
  
                 
#     #pdb.set_trace()
#     output_file = open("dest_file", 'w', encoding='utf-8')
#     for dic in flatten_list:
#         json.dump(dic, output_file) 
#         output_file.write("\n")
#     if(ee):
#         return render_template('vocastudent.html', firstname=result[0]['Firstname'],lastname=result[0]['Lastname'], stlevel=stlevel,stegr=stdegr,fromdate=request.form['fromd'],todate=request.form['tod'],resultsheader=['Date','Performance','Category', 'Sub Category','Firstname', 'Lastname'],rresult=ee, resultd=json.dumps(ee),file="dest_file") 
#     else:
#         return jsonify ( message="No data found for this time period",category="error", status=404)

# @app.route('/printstuff',methods=['POST','GET'])
# def printstuff(): 
#     #pdb.set_trace()
#     db = client.hopedatabase
#     allstudents = db.datastudents
    
#     if request.method == "POST":
#         if("bflag" not in request.form):
#             data_lines=[]
           
           
#             studentid=request.form['vehicle1']
#             degree=request.form['degree']
#             level=request.form['level']
#             print(studentid)
#             per=allstudents.find( { '_id':ObjectId(studentid)})
         
#             result = []
#             for i in per :
#                 result.append(i)
    
#             resdegree=result[0][level][degree]
#             listkeys=[]
#             stkeylevel=''
#             #pdb.set_trace()
#             keylist=[]
#             for key,value in resdegree.items():
#                 keylist.append(key)
#                 listkeys.append({key:list(value.keys())})
#             #pdb.set_trace()
#             return render_template('levelstudents.html', lisk=listkeys,stuid=studentid,stdegr=degree,stlevel=level,fromd=request.form['fromday'],tod=request.form['today'])         
#         else:
#             #pdb.set_trace()
#             stkey=request.form['stkey']
#             stuid=request.form['stuid']
#             stlevel=request.form['stlevel']
#             stdegr=request.form['stdegr']
#             fromd=request.form['fromd']
#             tod=request.form['tod']
#             flatten_list=[]
#             per=allstudents.find( { '_id':ObjectId(stuid)})
#             result = []
#             for i in per :
#                 result.append(i)
#             flatten_list=[]
#             category=[]
#             #pdb.set_trace()
#             finallist=[]
#             for key,value in result[0][stlevel][stdegr][stkey].items():
#                 finallist.append(key)
#             return render_template('finallevelstudents.html', stkey=stkey,catfinallist=finallist,stuid=stuid,stdegr=stdegr,stlevel=stlevel,fromd=request.form['fromd'],tod=request.form['tod'])         
        
        
#     else:
#         db = client.hopedatabase
#         allstudents = db.datastudents
#         data=list(allstudents.find({}))
      
#         if(data):
#             return render_template('studentprint.html', students=data)
#         else:
#             return jsonify ( message="No student found for this time period",category="error", status=404)
# def init(level,department):
#     db = client.hopedatabase
#     levels = db.datalevels.find({'_id':ObjectId('65e579bdfc618e2bf00c686b')})
#     result=[]
#     for i in levels:
#         result.append(i)
#     return result[0][level][department]
 
# def getname(studentid):
#     per=allstudents.find( { '_id':ObjectId(studentid)})
#     result = []
#     for i in per:
#         result.append(i)
#     return result[0]['Firstname']+" " +result[0]['Lastname']    
# def checklevel(keylevel,lislevel,studentid,degree,level,date):
#     jsond={}
#     jsonlevel=[]

#     for k in lislevel[keylevel][0]:
#         item=k
#         if k==0:        
#             jsonlevel.append({'key':item,'value':'enabled'})
#         else:
#             datafind=level+'.'+degree+'.'+keylevel+'.'+item+'.'+"Performance"
#             if(checklevelper(level,degree,keylevel,item,studentid,datafind)):
#                 jsonlevel.append({'key':item,'value':'enabled'})
#             else:
#                 jsonlevel.append({'key':item,'value':'disabled'})

#     return keylevel,jsonlevel
    
# def checklevelper(level,degree,keydl,item,studentid,keytodata):
#     per=allstudents.find( { '_id':ObjectId(studentid)},)
#     result = []
#     for i in per :
#          result.append(i)
#     #pdb.set_trace()
#     if (level not in result[0]) or (degree not in result[0][level]) or( keydl not in result[0][level][degree]) or (item not in result[0][level][degree][keydl]):
#         return True

#     value=allstudents.find( { '_id':ObjectId(studentid)},{keytodata:'Performed'})
#     if(len(value[0][level][degree][keydl][item])>=3):
#         return False
#     return True

# @app.route( '/filldata',methods=['POST'])
# def filldata():
#     #pdb.set_trace()
#     sdate=request.form['stdate']
#     suid=request.form['stuid']
#     sdegr=request.form['stdegr']
#     slevel=request.form['stlevel']
#     skeylevel=request.form['stkeylevel']
#     data=request.form.to_dict()
#     sname=getname(suid)
#     if request.method == "POST":
#         if("bflag" not in request.form):
#             rs="Performed,didnot Performed,and/or performed"
#             perm=rs.split(',')
#             slevelone=request.form[skeylevel]
#             return render_template('vocfilldata.html', performance=perm,sclicklevel=slevelone,stdate=sdate,stname=sname,stuid=suid,stdegr=sdegr,
#                                stlevel=slevel, stkeylevel=skeylevel)
                             
#         else:
#             perf=request.form['clicklevel']
#             per=allstudents.find( { '_id':ObjectId(suid)})
#             result = []
#             for i in per :
#                 result.append(i)
#             datedata={'Date':sdate,'Performance':perf}
#             leveldata={}

   
          
#             allstudents.update_one( { '_id': ObjectId(suid) },{ "$push" : {slevel+'.'+sdegr+'.'+request.form['stkeylevel']+'.'+request.form['sclicklevel']:[datedata] }})
          
#             return render_template('done.html',data="I am done")
        


# @app.route( '/insert',methods=['POST','GET'])
# def insert(): 
#     #pdb.set_trace()
#     if request.method == "POST":
#         date=request.form['date']
#         studentid=request.form['vehicle1']
#         degree=request.form['degree']
#         level=request.form['level']
#         data=request.form.to_dict()
#         namest=getname(studentid)
#         stru={}
#         if 'bflag' not in request.form:
#             lislevel={}
#             lislevel1st2nd={}
#             lislevel=init(level,degree)
#             for levele in lislevel:
#                 jsond,arraylev=checklevel(levele,lislevel,studentid,degree,level,date)
#                 lislevel1st2nd[levele]=arraylev
#             #pdb.set_trace()
#             return render_template('vocdetails.html',stdate=date,stname=namest,stuid=studentid,stlevel=level,stdegr=degree,comblevels=lislevel1st2nd)
    
#     #pdb.set_trace()
#     return render_template('student.html', students=allstudents.find({}))
   

# # main driver function
# if __name__ == '__main__':
 
#     # run() method of Flask class runs the application 
#     # on the local development server.
#     app.run(host='0.0.0.0', port=5000, debug=True)