__author__ = 'bigdata'
import re
import nltk
import pandas
import numpy
import matplotlib.pyplot
#To be able to read csv formated files, we will first have to import the
#csv module.import csv
#print "the methods of package re which is used for regular expressions"
#print (dir(re))

#print "the methods of package nltk which is a natural language toolkit"
#print (dir(nltk))



#read csv with csv module


#with open('/home/bigdata/data/carehome.csv', 'rb') as f:
  # reader = csv.reader(f)
  # for row in reader:
      # print row

#read csv with pandas module

#chomes = pandas.read_csv('/home/bigdata/data/carehome.csv')

chomes = pandas.read_csv('/home/bigdata/data/carehome.csv', sep=",")
chomes = chomes.head(200)
#print (chomes)

#Delete uneccessary columns
del chomes['_source']
del chomes['_widgetName']
del chomes['_resultNumber']
del chomes['_pageUrl']
del chomes['name']

#Change columns to appropriate data types and rename
chomes['Number'] = chomes['_num'].astype('int64')
chomes['Address'] = chomes['address'].astype('str')
chomes['Information'] = chomes['info'].astype('str')

#Remove original columns
chomes = chomes.drop(['_num','address','info'], axis=1)


text = 'Group: South Tyneside Metropolitan Borough Council Person in charge: Dawn Hill (Manager) Local Authority / Social Services: South Tyneside Metropolitan Borough Council (click for contact details) Type of Service: Care Home only (Residential Care) \xe2\x80\x93 Local Authority Owned  30 residents Registered Care Categories*: Mental Health Condition \xe2\x80\xa2 Old Age \xe2\x80\xa2 Physical Disability \xe2\x80\xa2 Sensory Impairment Specialist Care Categories: Hearing Impairment & Deafness \xe2\x80\xa2 Speech Impairment Single Rooms: 30 Rooms with ensuite WC: 1 Latest CQC* Report on Perth Green House: click here * Care Quality Commission (CQC) is responsible for the registration and inspection of social care services in England.'
print (text)

text = 'Group: South Tyneside Metropolitan Borough Council Person in charge: Dawn Hill (Manager) Local Authority / Social Services: South Tyneside Metropolitan Borough Council (click for contact details) Type of Service: Care Home only (Residential Care) \xe2\x80\x93 Local Authority Owned  30 residents Registered Care Categories*: Mental Health Condition \xe2\x80\xa2 Old Age \xe2\x80\xa2 Physical Disability \xe2\x80\xa2 Sensory Impairment Specialist Care Categories: Hearing Impairment & Deafness \xe2\x80\xa2 Speech Impairment Single Rooms: monkey Rooms with ensuite WC: 1 Latest CQC* Report on Perth Green House: click here * Care Quality Commission (CQC) is responsible for the registration and inspection of social care services in England.'
print (text)


address = 'Charmouth Road Lyme Regis DT7 3HH '


#Postcode
chomes['Postcode']= chomes['Address'].apply(lambda x:x[-8:])


#     #City
#     city = re.search(r'\s[A-Z][^-]+[A-Z][A-Z][0-9]+\s[0-9][A-Z][A-Z]\s', address, flags=0)
#     city = str(city.group())
#     print city
#     chomes['City'] = city
#

#Single Rooms
def getRooms(chomes):
     srooms = re.search(r'Rooms:\s[0-9][0-9]', chomes, flags=0)
     if srooms is None:
        sroomsno = ' '
     else:
         sroom = str(srooms.group())
         sroomsno = re.sub(r'Rooms:\s', '', sroom)
     return pandas.Series(dict(rooms = sroomsno))

chomes['Single Rooms'] = (chomes['Information'].apply(lambda x:getRooms(x)))


#getEnsuiteRooms
def getEnsuiteRooms(chomes):
     erooms = re.search(r'ensuite\sWC:\s[0-9]+', chomes, flags=0)
     if erooms is None:
         eroomsno = ' '
     else:
         eroom = str(erooms.group())
         eroomsno = re.sub(r'ensuite\sWC:\s', '', eroom)
     return pandas.Series(dict(erooms = eroomsno))

chomes['Ensuite Rooms'] = (chomes['Information'].apply(lambda x:getEnsuiteRooms(x)))

#Ages Accepted
def getAges(chomes):
     ages = re.search(r'Ages\s[0-9][0-9]\+', chomes, flags=0)
     if ages is None:
         ages = 'All Ages'
     else:
         ages = str(ages.group())
     return pandas.Series(dict(ages = ages))

chomes['Ages Accepted'] = (chomes['Information'].apply(lambda x:getAges(x)))

#Support Types

def getAlcoholDependence(chomes):
     present = re.search(r'Alcohol\sDependence', chomes, flags=0)
     if present is None:
         alcohol = '0'
     else:
         alcohol = '1'
     return pandas.Series(dict(alcohol = alcohol))

chomes['Alcohol Dependence'] = (chomes['Information'].apply(lambda x:getAlcoholDependence(x)))

def getAlzheimers(chomes):
     present = re.search(r'Alzheimer\'s', chomes, flags=0)
     if present is None:
         alzheimers = '0'
     else:
         alzheimers = '1'
     return pandas.Series(dict(alzheimers = alzheimers))

chomes['Alzheimers'] = (chomes['Information'].apply(lambda x:getAlzheimers(x)))

def getAnorexia(chomes):
     present = re.search(r'Anorexia/Bulimia/Self\sHarming', chomes, flags=0)
     if present is None:
         anorexia = '0'
     else:
         anorexia = '1'
     return pandas.Series(dict(anorexia = anorexia))

chomes['Anorexia/Bulimia/Self Harming'] = (chomes['Information'].apply(lambda x:getAnorexia(x)))

def getBipolar(chomes):
     present = re.search(r'Bipolar/Manic\sDepression', chomes, flags=0)
     if present is None:
         bipolar = '0'
     else:
         bipolar = '1'
     return pandas.Series(dict(bipolar = bipolar))

chomes['Bipolar/Manic Depression'] = (chomes['Information'].apply(lambda x:getBipolar(x)))

def getCancerCare(chomes):
     present = re.search(r'Cancer\sCare', chomes, flags=0)
     if present is None:
         cancerCare = '0'
     else:
        cancerCare = '1'
     return pandas.Series(dict(alzheimers = cancerCare))

chomes['Cancer Care'] = (chomes['Information'].apply(lambda x:getCancerCare(x)))

def getcerebralPalsy(chomes):
     present = re.search(r'Cerebral\sPalsy', chomes, flags=0)
     if present is None:
         cerebralPalsy = '0'
     else:
         cerebralPalsy = '1'
     return pandas.Series(dict(cerebralPalsy = cerebralPalsy))

chomes['Cerebral Palsy'] = (chomes['Information'].apply(lambda x:getcerebralPalsy(x)))

def getChallengingBehaviour(chomes):
     present = re.search(r'Challenging\sBehaviour', chomes, flags=0)
     if present is None:
         challengingBehaviour = '0'
     else:
         challengingBehaviour = '1'
     return pandas.Series(dict(challengingBehaviour = challengingBehaviour))

chomes['Challenging Behaviour'] = (chomes['Information'].apply(lambda x:getChallengingBehaviour(x)))

def getColitis(chomes):
     present = re.search(r'Colitis', chomes, flags=0)
     if present is None:
         colitis = '0'
     else:
         colitis = '1'
     return pandas.Series(dict(colitis = colitis))

chomes['Colitis'] = (chomes['Information'].apply(lambda x:getColitis(x)))

def getDementia(chomes):
     present = re.search(r'Dementia', chomes, flags=0)
     if present is None:
         dementia = '0'
     else:
         dementia = '1'
     return pandas.Series(dict(dementia = dementia))

chomes['Dementia'] = (chomes['Information'].apply(lambda x:getDementia(x)))

def getDownSyndrome(chomes):
     present = re.search(r'Down\sSyndrome', chomes, flags=0)
     if present is None:
         downSyndrome = '0'
     else:
         downSyndrome = '1'
     return pandas.Series(dict(downSyndrome = downSyndrome))

chomes['Down Syndrome'] = (chomes['Information'].apply(lambda x:getDownSyndrome(x)))

def getDrugDependence(chomes):
     present = re.search(r'Drug\sDependence', chomes, flags=0)
     if present is None:
         drugDependence = '0'
     else:
         drugDependence = '1'
     return pandas.Series(dict(drugDependence = drugDependence))

chomes['Drug Dependence'] = (chomes['Information'].apply(lambda x:getDrugDependence(x)))

def getEatingDisorder(chomes):
     present = re.search(r'Eating\sDisorder', chomes, flags=0)
     if present is None:
         eatingDisorder = '0'
     else:
         eatingDisorder = '1'
     return pandas.Series(dict(eatingDisorder = eatingDisorder))

chomes['Eating Disorder'] = (chomes['Information'].apply(lambda x:getEatingDisorder(x)))

def getEpilepsy(chomes):
     present = re.search(r'Epilepsy', chomes, flags=0)
     if present is None:
         epilepsy = '0'
     else:
         epilepsy = '1'
     return pandas.Series(dict(epilepsy = epilepsy))

chomes['Epilepsy'] = (chomes['Information'].apply(lambda x:getEpilepsy(x)))

def getHeadInjury(chomes):
     present = re.search(r'Head\sInjury', chomes, flags=0)
     if present is None:
         headInjury= '0'
     else:
         headInjury = '1'
     return pandas.Series(dict(headInjury = headInjury))

chomes['Head Injury'] = (chomes['Information'].apply(lambda x:getHeadInjury(x)))

def getHearingImpairment(chomes):
     present = re.search(r'Hearing\sImpairment', chomes, flags=0)
     if present is None:
         hearingImpairment = '0'
     else:
         hearingImpairment = '1'
     return pandas.Series(dict(hearingImpairment = hearingImpairment))

chomes['Hearing Impairment'] = (chomes['Information'].apply(lambda x:getHearingImpairment(x)))

def getHuntingtons(chomes):
     present = re.search(r'Huntington\'s\sDisease', chomes, flags=0)
     if present is None:
         huntingtons = '0'
     else:
         huntingtons = '1'
     return pandas.Series(dict(huntingtons = huntingtons))

chomes['Huntington\'s Disease'] = (chomes['Information'].apply(lambda x:getHuntingtons(x)))

def getLearningDisability(chomes):
     present = re.search(r'Learning\sDisability', chomes, flags=0)
     if present is None:
         learningDisability = '0'
     else:
         learningDisability = '1'
     return pandas.Series(dict(learningDisability = learningDisability))

chomes['Learning Disability'] = (chomes['Information'].apply(lambda x:getLearningDisability(x)))

def getMentalHealthCondition(chomes):
     present = re.search(r'Mental\sHealth\sCondition', chomes, flags=0)
     if present is None:
         mentalHealthCondition = '0'
     else:
         mentalHealthCondition = '1'
     return pandas.Series(dict(mentalHealthCondition = mentalHealthCondition))

chomes['Mental Health Condition'] = (chomes['Information'].apply(lambda x:getMentalHealthCondition(x)))

def getMND(chomes):
     present = re.search(r'Motor\sNeuron\sDisease', chomes, flags=0)
     if present is None:
         MND = '0'
     else:
         MND = '1'
     return pandas.Series(dict(MND = MND))

chomes['Motor Neuron Disease'] = (chomes['Information'].apply(lambda x:getMND(x)))

def getMultipleSclerosis(chomes):
     present = re.search(r'Multiple\sSclerosis', chomes, flags=0)
     if present is None:
         multipleSclerosis = '0'
     else:
         multipleSclerosis = '1'
     return pandas.Series(dict(multipleSclerosis = multipleSclerosis))

chomes['Multiple Sclerosis'] = (chomes['Information'].apply(lambda x:getMultipleSclerosis(x)))

def getMuscularDystrophy(chomes):
     present = re.search(r'Muscular\sDystrophy', chomes, flags=0)
     if present is None:
         muscularDystrophy = '0'
     else:
         muscularDystrophy = '1'
     return pandas.Series(dict(muscularDystrophy = muscularDystrophy))

chomes['Muscular Dystrophy'] = (chomes['Information'].apply(lambda x:getMuscularDystrophy(x)))

def getOldAge(chomes):
     present = re.search(r'Old\sAge', chomes, flags=0)
     if present is None:
         oldAge = '0'
     else:
         oldAge = '1'
     return pandas.Series(dict(oldAge = oldAge))

chomes['Old Age'] = (chomes['Information'].apply(lambda x:getOldAge(x)))

def getOrthopaedic(chomes):
     present = re.search(r'Eating\sDisorder', chomes, flags=0)
     if present is None:
         orthopaedic = '0'
     else:
         orthopaedic = '1'
     return pandas.Series(dict(orthopaedic = orthopaedic))

chomes['Orthopaedic'] = (chomes['Information'].apply(lambda x:getOrthopaedic(x)))

def getParkinsons(chomes):
     present = re.search(r'Parkinson\'s\sDisease', chomes, flags=0)
     if present is None:
         parkinsons = '0'
     else:
         parkinsons = '1'
     return pandas.Series(dict(parkinsons = parkinsons))

chomes['Parkinson\'s Disease'] = (chomes['Information'].apply(lambda x:getParkinsons(x)))

def getPhysicalDisability(chomes):
     present = re.search(r'Physical\sDisability', chomes, flags=0)
     if present is None:
         physicalDisability = '0'
     else:
         physicalDisability = '1'
     return pandas.Series(dict(physicalDisability = physicalDisability))

chomes['Physical Disability'] = (chomes['Information'].apply(lambda x:getPhysicalDisability(x)))

def getSchizophrenia(chomes):
     present = re.search(r'Schizophrenia', chomes, flags=0)
     if present is None:
         schizophrenia = '0'
     else:
         schizophrenia = '1'
     return pandas.Series(dict(schizophrenia = schizophrenia))

chomes['Schizophrenia'] = (chomes['Information'].apply(lambda x:getSchizophrenia(x)))

def getSensoryImpairment(chomes):
     present = re.search(r'Sensory\sImpairment', chomes, flags=0)
     if present is None:
         sensoryImpairment = '0'
     else:
         sensoryImpairment = '1'
     return pandas.Series(dict(sensoryImpairment = sensoryImpairment))

chomes['Sensory Impairment'] = (chomes['Information'].apply(lambda x:getSensoryImpairment(x)))

def getSpeechImpairment(chomes):
     present = re.search(r'Speech\sImpairment', chomes, flags=0)
     if present is None:
         speechImpairment = '0'
     else:
         speechImpairment = '1'
     return pandas.Series(dict(speechImpairment = speechImpairment))

chomes['Speech Impairment'] = (chomes['Information'].apply(lambda x:getSpeechImpairment(x)))

def getStroke(chomes):
     present = re.search(r'Stroke', chomes, flags=0)
     if present is None:
         stroke = '0'
     else:
         stroke = '1'
     return pandas.Series(dict(stroke = stroke))

chomes['Stroke'] = (chomes['Information'].apply(lambda x:getStroke(x)))

def getSubstanceMisuse(chomes):
     present = re.search(r'Substance\sMisuse', chomes, flags=0)
     if present is None:
         substanceMisuse = '0'
     else:
         substanceMisuse = '1'
     return pandas.Series(dict(substanceMisuse = substanceMisuse))

chomes['Substance Misuse'] = (chomes['Information'].apply(lambda x:getSubstanceMisuse(x)))

chomes['Stroke Total']= chomes['Stroke'].sum(axis= 1)
print chomes
#print type(chomes['Stroke'])
#chomes.to_csv('result.csv')



