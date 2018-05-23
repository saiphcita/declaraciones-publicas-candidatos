#import parquet
#import json
#import rows
#import pyarrow.parquet as pq
import pandas as pd
import csv
import pickle 

funcionarioPartidos={}
def getNamesPartido(partido):
	global funcionarioPartidos
	FILE=open("namesPAN.txt",'r')
	lines=FILE.readlines()
	for l in lines:
		l=l.lower()
		l=l.replace("\n","")
		print (l)
		name=l
		funcionarioPartidos.setdefault(name,{})
		funcionarioPartidos[name][partido]=0
	pickle.dump(funcionarioPartidos, open("funcionarioPartidosPAN.p", "wb" ))
	
	return funcionarioPartidos


def getNamesYear(year):
	df=pd.read_csv("Declaraciones_2018.csv")
	#df.info()
	#print(df['NOMBRE'])
	declaracion=df['DECLARACION']

	nombres=df['NOMBRE']
	valor=df['VALOR']
	indexN=0
	didNotAccept={}
	allFuncionarios={}
	for v in valor:
		name=nombres[indexN]
		name=name.lower()
		allFuncionarios[name]=0
		if "EL SERVIDOR NO ACEPTO HACER PUBLICOS SUS DATOS PATRIMONIALES" in str(v):
		
			#print (name)
			#print (v)
			didNotAccept.setdefault(name,0)
			didNotAccept[name]+=1
		indexN+=1
	print ("Num. funcionarios sin declarar:"+str(len(didNotAccept)))
	print (len(allFuncionarios))
	p=len(didNotAccept)*100
	p=float(float(p)/float(len(allFuncionarios)))
	print (p)
	for n in didNotAccept:
		v=didNotAccept[n]
	pickle.dump(didNotAccept, open("didNotAccept2018.p", "wb" ))
	pickle.dump(allFuncionarios, open("allFuncionarios2018.p", "wb" ))
	
	return didNotAccept,allFuncionarios
		
def getLowwrCaseFuncionarios():
	funcionariosPartidos=pickle.load( open("funcionarioPartidosPAN.p", "rb" ) )
	funcionariosLower={}
	for f in allFuncionarios:
		fLower=f.lower()
		flower
		print (f)


def findMatch():
	didNotAccept=pickle.load( open("didNotAccept2018.p", "rb" ) )
	allFuncionarios=pickle.load( open("allFuncionarios2018.p", "rb" ) )
	funcionariosPartidos=pickle.load( open("funcionarioPartidosPAN.p", "rb" ) )
	
	#for funcionarioA in funcionariosPartidos:
	#	print (funcionarioA)
	for funcionarioB in allFuncionarios:
		if "robledo" in funcionarioB:
			print ("found it"+funcionarioB+">>")
			#break
		#if f in allFuncionarios:
		#	print ("found"+f)

	#for f in allFuncionarios:
	#	if "martinez" in f:
	#		print (f)
	#	print (f)

	
	
#didNotAccept,allFuncionarios=getNamesYear(2018)
#getNamesPartido("PAN")

findMatch()








	#if i<100:
	#	print (i)
	#	print (d)
	#	print ()
	#	i+=1
	#else:
	#	break

#print (data)


#print ("hello")

#table2 = pq.read_table("2018.parquet")
#table2.to_pandas()

#i=0

#for row in table2:
#	if i==2:
#		print ("counter:"+str(i))
#		print (row)
		#for e in row:
		#	print (e)
	#elif i==9:
	#	print ("counter:"+str(i))
	#	print (row)

#	i+=1
	#if i<:
	#	print (row)
	#	i+=1
	#else:
	#	break
#table2 = parquet.read_table("2018.parquet")
#parquet.write_table(table, 'example.parquet')
#rows.print(myfile.parquet)
#table = rows.import_from_parquet("2018.parquet")
#for row in table:
#    print (row)
#    break
#with open("2018.parquet") as fo:
	#print ("eber")
	#for row in parquet.DictReader(fo):
	#	print (row)
   # prints:
   # {"foo": 1, "bar": 2}
   # {"foo": 4, "bar": 5}
   #for row in parquet.DictReader(fo, columns=['foo', 'bar']):
       #print(json.dumps(row))
   # @   print (row)
