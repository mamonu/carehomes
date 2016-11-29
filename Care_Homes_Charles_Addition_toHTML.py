__author__ = 'bigdata'
import re
import nltk
import pandas
import numpy
import matplotlib.pyplot
from bs4 import BeautifulSoup as bs4




#To be able to read csv formated files, we will first have to import the
#csv module.import csv
#print "the methods of package re which is used for regular expressions"
#print (dir(re))

#print "the methods of package nltk which is a natural language toolkit"
#print (dir(nltk))

#read csv with csv module

#with open('/home/bigdata/PycharmProjects/carehomes/carehome.csv', 'rb') as f:
  # reader = csv.reader(f)
  # for row in reader:
      # print row

#read csv with pandas module

chomes = pandas.read_csv('/home/bigdata/PycharmProjects/carehomes/carehome.csv')

#chomes = pandas.read_csv('H:/My Documents/Python Working Dir/carehome.csv', sep=",")
#chomes = pandas.read_csv('/home/bigdata/data/carehome.csv', sep=",")
chomes = chomes.head(200)
print (chomes)

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
# print (text)
text = 'Group: South Tyneside Metropolitan Borough Council Person in charge: Dawn Hill (Manager) Local Authority / Social Services: South Tyneside Metropolitan Borough Council (click for contact details) Type of Service: Care Home only (Residential Care) \xe2\x80\x93 Local Authority Owned  30 residents Registered Care Categories*: Mental Health Condition \xe2\x80\xa2 Old Age \xe2\x80\xa2 Physical Disability \xe2\x80\xa2 Sensory Impairment Specialist Care Categories: Hearing Impairment & Deafness \xe2\x80\xa2 Speech Impairment Single Rooms: monkey Rooms with ensuite WC: 1 Latest CQC* Report on Perth Green House: click here * Care Quality Commission (CQC) is responsible for the registration and inspection of social care services in England.'
# print (text)
address = 'Charmouth Road Lyme Regis DT7 3HH '

# We take care of 4 attributes which are non-standard 
# Postcode
chomes['Postcode']= chomes['Address'].apply(lambda x:x[-8:])

#     #City
#     city = re.search(r'\s[A-Z][^-]+[A-Z][A-Z][0-9]+\s[0-9][A-Z][A-Z]\s', address, flags=0)
#     city = str(city.group())
#     print city
#     chomes['City'] = city

# Single Rooms    
def getRooms(chomes):
     srooms = re.search(r'Rooms:\s[0-9][0-9]', chomes, flags=0)
     if srooms is None:
         sroomsno = ' '
     # If no rooms exist/ it doesn't find any reooms, then sroomsno is empty/0   
     else:
         # Group the search results contained within the match object to create a 
         # single string
         sroom = str(srooms.group())
         # Split this string so you can get a two digit number  
         sroomsno = re.sub(r'Rooms:\s', '', sroom)
         # for the first occurence of 'Room ' in sroom, replace with ''
         # print "sroomsno- {}".format(sroomsno)     
     # If it does find srooms, then how many does it find.
     # Put the Output into Dictionary form
     # Convert the dictionary to a Pandas series. 
     # Correct format 
     return pandas.Series(dict(rooms = sroomsno))
     
chomes['Single Rooms'] = (chomes['Information'].apply(lambda x:getRooms(x)))

# Ensuite Rooms
def getEnsuiteRooms(chomes):
     erooms = re.search(r'ensuite\sWC:\s[0-9]+', chomes, flags=0)
     if erooms is None:
         eroomsno = ' '
     else:
         eroom = str(erooms.group())
         eroomsno = re.sub(r'ensuite\sWC:\s', '', eroom)
     return pandas.Series(dict(erooms = eroomsno))

chomes['Ensuite Rooms'] = (chomes['Information'].apply(lambda x:getEnsuiteRooms(x)))

# Ages Accepted
def getAges(chomes):
     ages = re.search(r'Ages\s[0-9][0-9]\+', chomes, flags=0)
     if ages is None:
         ages = 'All Ages'
     else:
         ages = str(ages.group())
     return pandas.Series(dict(ages = ages))

chomes['Ages Accepted'] = (chomes['Information'].apply(lambda x:getAges(x)))

# Here we define our function for finding all other attributes that follow
# a standard format
def getAttribute(sv,data):  
    present = re.search(sv,data,flags=0)
    if present is None:
        Attribute = '0'
    else:
        Attribute = '1'
    return pandas.Series(dict(Attribute = Attribute))  
    
# We list all the Attribute title and associated Regular Expressions to find
# List of Attribute Titles
an = ['Alcohol Dependence','Alzheimers','Anorexia/Bulimia/Self Harming','Bipolar/Manic Depression','Cancer Care','Cerebral Palsy','Challenging Behaviour','Colitis','Dementia','Down Syndrome','Drug Dependence','Eating Disorder','Epilepsy','Head Injury','Hearing Impairment','Huntington\'s Disease','Learning Disability','Mental Health Condition','Motor Neuron Disease','Multiple Sclerosis','Muscular Dystrophy','Old Age','Orthopaedic','Parkinson\'s Disease','Physical Disability','Schizophrenia','Sensory Impairment','Speech Impairment','Stroke','Substance Misuse']
# List of Regular Expressions associated with Attribute Title. 
av = [r'Alcohol\sDependence',r'Alzheimer\'s',r'Anorexia/Bulimia/Self\sHarming',r'Bipolar/Manic\sDepression',r'Cancer\sCare',r'Cerebral\sPalsy',r'Challenging\sBehaviour',r'Colitis',r'Dementia',r'Down\sSyndrome',r'Drug\sDependence',r'Eating\sDisorder',r'Epilepsy',r'Head\sInjury',r'Hearing\sImpairment',r'Huntington\'s\sDisease',r'Learning\sDisability',r'Mental\sHealth\sCondition',r'Motor\sNeuron\sDisease',r'Multiple\sSclerosis',r'Muscular\sDystrophy',r'Old\sAge',r'Eating\sDisorder',r'Parkinson\'s\sDisease',r'Physical\sDisability',r'Schizophrenia',r'Sensory\sImpairment',r'Speech\sImpairment',r'Stroke',r'Substance\sMisuse']

# Search for the Attributes witin the carehomes data (Contained within the Information column)
# Iterate over both the list of attributes, and list of regular expressions
for i,v in zip(an,av):
    # Search the Information column of the care homes Dataframe
    # Begin with Alchol Depndence and iterate along the lists above
    # create a new column in the array called e.g. chomes['Alcohol Dependence']
    # The apply term applies a function to all elements of a series/column 
    # within a Pandas array
    chomes[i] = chomes['Information'].apply(lambda x:getAttribute(v,x))

# What is written is a simpler way of doing this
# for i in range(0,len(av)):
#    chomes[an[i]] = chomes['Information'].apply(lambda x:getAttribute(av[i],x))


print chomes



#chomes.to_html("/home/bigdata/PycharmProjects/carehomes/res.html")


final = pandas.read_csv('/home/bigdata/PycharmProjects/carehomes/final.csv')
final = final.head(100)


#avoid utf problems by converting with bs4 prettify

#another way is to delete the first and second column which are not used anyway
final = final.drop(final.columns[[0, 1, 2]], axis=1)


print final

html1 = bs4(final.to_html(), 'html.parser')
f = open('results.html','w')
f.write(html1.prettify(encoding='utf-8'))
f.close()

# Notes:
# lambda is necessary if your function has more than one argument
# This might work if you can get the string down and figure out which way
# the arguments in the function need to be.


# Change Path for your needs
#chomes.to_csv("H:/My Documents/Python Working Dir/Care Homes Summary.csv")
