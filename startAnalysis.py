#import parquet
#import json
#import rows
#import pyarrow.parquet as pq
import pandas as pd
import csv
import pickle 
import operator

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

def getCandidateInfoDiputado():
	df=pd.read_csv("candidatosDiputados.csv")
	df.info()

	candidatosSenado=df["propietario"]
	#candidatosSenadoSuplente=df["suplente"]
	yearCandidato=df["yr"]
	partidoCandidato=df["part"]

	i=0
	candidatosDiputadoPartido={}

	for c in candidatosSenado:
		#print c
		c=c.lower()
		partido=partidoCandidato[i]
		#suplente=candidatosSenadoSuplente[i].lower()

		year=yearCandidato[i]
		print year
		i+=1
		if year==2018:
			candidatosDiputadoPartido[c]=partido
			#candidatosDiputadoPartido[suplente]=partido

	for c in candidatosDiputadoPartido:
		print c+", "+candidatosDiputadoPartido[c]
	pickle.dump(candidatosDiputadoPartido, open("candidatosDiputadoPartido.p", "wb" ))
	

	

def getCandidateInfoSenado():
	df=pd.read_csv("candidatosSenado.csv")
	df.info()
	candidatosSenado=df["propietario"]
	candidatosSenadoSuplente=df["suplente"]
	partidoCandidato=df["part"]
	
	i=0
	candidatosSenadoPartido={}
	for c in candidatosSenado:
		#print c
		c=c.lower()
		partido=partidoCandidato[i]
		suplente=candidatosSenadoSuplente[i].lower()
		i+=1
		candidatosSenadoPartido[c]=partido
		candidatosSenadoPartido[suplente]=partido

	for c in candidatosSenadoPartido:
		print c+", "+candidatosSenadoPartido[c]
	pickle.dump(candidatosSenadoPartido, open("candidatosSenadoPartido.p", "wb" ))
	


def getNamesYear(year):
	#df=pd.read_csv("Declaraciones_2018.csv")
	df=pd.read_csv("Declaraciones_"+str(year)+".csv")
	
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
	pickle.dump(didNotAccept, open("didNotAccept"+str(year)+".p", "wb" ))
	pickle.dump(allFuncionarios, open("allFuncionarios"+str(year)+".p", "wb" ))
	
	return didNotAccept,allFuncionarios

def addFuncionarios(allFuncionarios,funcionarioYear,year):
	for funcionario in funcionarioYear:
		funcionarioL=funcionario.lower()
		allFuncionarios.setdefault(funcionarioL,{})
		allFuncionarios[funcionarioL][year]=funcionarioYear[funcionario]
	return allFuncionarios

def getAllCorruptFuncionariosAcrossYears():
	funcionarios2014=pickle.load( open("didNotAccept2014.p", "rb" ) )
	funcionarios2015=pickle.load( open("didNotAccept2015.p", "rb" ) )
	funcionarios2016=pickle.load( open("didNotAccept2016.p", "rb" ) )
	funcionarios2017=pickle.load( open("didNotAccept2017.p", "rb" ) )
	funcionarios2018=pickle.load( open("didNotAccept2018.p", "rb" ) )

	allFuncionarios={}

	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2014,2014)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2015,2015)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2016,2016)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2017,2017)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2018,2018)

	print len(allFuncionarios)
	pickle.dump(allFuncionarios, open("allFuncionariosCorruptos.p", "wb" ))
	

def getAllFuncionariosAcrossYears():
	funcionarios2014=pickle.load( open("allFuncionarios2014.p", "rb" ) )
	funcionarios2015=pickle.load( open("allFuncionarios2015.p", "rb" ) )
	funcionarios2016=pickle.load( open("allFuncionarios2016.p", "rb" ) )
	funcionarios2017=pickle.load( open("allFuncionarios2017.p", "rb" ) )
	funcionarios2018=pickle.load( open("allFuncionarios2018.p", "rb" ) )

	allFuncionarios={}

	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2014,2014)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2015,2015)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2016,2016)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2017,2017)
	allFuncionarios=addFuncionarios(allFuncionarios,funcionarios2018,2018)

	print len(allFuncionarios)
	pickle.dump(allFuncionarios, open("allFuncionarios.p", "wb" ))
	

def unirPartidos(partidos):
	partidosUnidos={}
	for p in partidos:
		if "prd" in p:
			partidoFinal="PAN"
		elif "pes" in p:
			partidoFinal="MORENA"
		elif "panal" in p:
			partidoFinal="PRI"
		elif "pvem" in p:
			partidoFinal="PRI"
		elif "pan" in p:
			partidoFinal="PAN"
		elif "pri" in p:
			partidoFinal="PRI"
		elif "morena" in p:
			partidoFinal="MORENA"
		elif "indep" in p:
			partidoFinal="INDEPENDIENTE"
		partidosUnidos.setdefault(partidoFinal,0)
		partidosUnidos[partidoFinal]+=partidos[p]
		#partidosUnidos[partidoFinal]=partidos[p]
	return partidosUnidos




	#prd,1
	#pes,1
	#morena,2
	#panal,4
	#pvem,4
	#pan,4
	#morena-pt-pes,8
	#pan-prd-mc,8
	#pri-pvem-panal,10
	#pri,26

def calcularDiputadosCorruptosPartido():
	candidatosDiputadoPartido=pickle.load( open("candidatosDiputadoPartido.p", "rb" ) )
	allFuncionarios=pickle.load( open("allFuncionarios.p", "rb" ) )
	allFuncionariosCorruptos=pickle.load( open("allFuncionariosCorruptos.p", "rb" ) )

	numCandidatosPartidoFound={}
	numCandidatosPartidoCorrupto={}
	for c in candidatosDiputadoPartido:
		if c in allFuncionarios:
			partido=candidatosDiputadoPartido[c]
			
			numCandidatosPartidoFound.setdefault(partido,0)
			numCandidatosPartidoFound[partido]+=1

			if c in allFuncionariosCorruptos:
				
				numCandidatosPartidoCorrupto.setdefault(partido,0)
				numCandidatosPartidoCorrupto[partido]+=1

	numCandidatosPartidoFound=unirPartidos(numCandidatosPartidoFound)
	numCandidatosPartidoCorrupto=unirPartidos(numCandidatosPartidoCorrupto)

	for partido in numCandidatosPartidoFound:
		if partido in numCandidatosPartidoCorrupto:
			corrupto=numCandidatosPartidoCorrupto[partido]
		else:
			corrupto=0
		porcentaje=corrupto*100
		porcentaje=float(float(porcentaje)/float(numCandidatosPartidoFound[partido]))
		pNuevo=100-porcentaje
		print partido+","+str(corrupto)+","+str(pNuevo)
	#numCandidatosPartidoFound={}
	#numCandidatosPartidoCorrupto={}


		
		

	

def findFuncionario():
	
	allFuncionarios=pickle.load( open("allFuncionarios.p", "rb" ) )
	allFuncionariosCorruptos=pickle.load( open("allFuncionariosCorruptos.p", "rb" ) )

	#pickle.dump(allFuncionarios, open("allFuncionariosCorruptos.p", "wb" ))
	
	candidatosSenadoPartido=pickle.load( open("candidatosSenadoPartido.p", "rb" ) )
	candidatosDiputadoPartido=pickle.load( open("candidatosDiputadoPartido.p", "rb" ) )
	#didNotAccept

	
	foundCandidatesSenado={}
	for f in candidatosSenadoPartido:
		if f in allFuncionarios:
			foundCandidatesSenado[f]=candidatosSenadoPartido[f]
	print len(foundCandidatesSenado)
	candidatoSenadoCorruptos={}
	for f in foundCandidatesSenado:
		if f in allFuncionariosCorruptos:
			candidatoSenadoCorruptos[f]=foundCandidatesSenado[f]
	print len(candidatoSenadoCorruptos)

	porcentajeCorruptos=len(candidatoSenadoCorruptos)*100
	porcentajeCorruptos=float(float(porcentajeCorruptos)/float(len(foundCandidatesSenado)))
	print porcentajeCorruptos

	partidosCorruptos={}

	for f in candidatoSenadoCorruptos:
		partido=candidatoSenadoCorruptos[f]
		partidosCorruptos.setdefault(partido,0)
		partidosCorruptos[partido]+=1
	partidosCorruptos=unirPartidos(partidosCorruptos)
	#partidosSorted = sorted(partidosCorruptos.items(), key=operator.itemgetter(1),reverse=False)

	#for p,v in partidosSorted:
	#	print p+","+str(v)

	partidosBuenos={}
	for f in foundCandidatesSenado:
		#if not f in candidatoSenadoCorruptos:
		partido=foundCandidatesSenado[f]
		partidosBuenos.setdefault(partido,0)
		partidosBuenos[partido]+=1
	partidosBuenos=unirPartidos(partidosBuenos)
	for p in partidosBuenos:
		#print "FINAL:"+p+","+str(partidosBuenos[p])
		if p in partidosCorruptos:
			numCorruptos=partidosCorruptos[p]
			porcentaje=numCorruptos*100
			porcentaje=float(float(porcentaje)/float(partidosBuenos[p]))
			#print porcentaje
		else:
			porcentaje=0
			numCorruptos=0
		print "FINAL:"+p+","+str(porcentaje)+","+str(numCorruptos)






	#foundCandidatesSenado[f]



	#MORENA,11
	#PAN,13
	#PRI,44
	
	#for p in partidosCorruptos:
	#	print 




	#porcentaje de candidatos de senado que no declara son 84% de los que aparecen en la lista





	#for f in allFuncionariosCorruptos:
	#	if f in candidatosSenadoPartido:
	#		print "FOUND IT"+f
		#if "menchaca salazar" in f:
		#if "lorena martinez rodriguez" in f:
		#	print f
			#if "martinez" in f:
			#	print f

	#for funcionarioA in funcionarioPartidosPAN:
	#	for funcionarioB in allFuncionarios:
	#		if funcionarioA in funcionarioB:
	#			print "FOUND IT!"+funcionarioA
	#			break

calcularDiputadosCorruptosPartido()
#getAllCorruptFuncionariosAcrossYears()
#findFuncionario()
#getCandidateInfoDiputado()
#getCandidateInfoSenado()	
#startDateUsersClean={}
#getAllFuncionariosAcrossYears()
#Numero total de funcionarios: 311,040 (2014-2018)
#didNotAccept,allFuncionarios=getNamesYear(2018)
#didNotAccept,allFuncionarios=getNamesYear(2017)
#didNotAccept,allFuncionarios=getNamesYear(2016)
#didNotAccept,allFuncionarios=getNamesYear(2015)
#didNotAccept,allFuncionarios=getNamesYear(2014)
#getNamesPartido("PAN")

#Total de funcionarios sin declarar: 226,229
#Num. funcionarios sin declarar:5,904
#7286
#81.0321163876
#Num. funcionarios sin declarar:151,118
#207,291
#72.9013801853
#Num. funcionarios sin declarar:133,030
#201,150
#66.1347253294






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
