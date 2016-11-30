from nltk import *
import pandas as pd
import pprint


text = '''
Gracewell of Hove is a purpose-built luxury nursing home and is part of Gracewell Healthcare, winner of the Health Investors Award for residential care provider of the year 2014.

The home offers a comfortable and active retirement lifestyle for its residents and provides leading-edge care tailored to older age-related care needs.

The home works closely with family and loved ones and has strong community links that include an excellent relationship with related health services and professionals.

Group: Gracewell Healthcare Ltd

Person in charge: Ann Lee (Registered Manager)

Local Authority / Social Services: Brighton & Hove City Council (click for contact details)

Type of Service: Care Home with nursing – Privately Owned , 35 residents

Registered Care Categories*: Old Age • Physical Disability • Sensory Impairment

Admission Information: Ages 50+.

Languages Spoken by Staff (other than English): Filipino, Chinese - Cantonese, Polish, Portuguese, Romanian

Single Rooms: 35

Rooms with ensuite WC: 29

Facilities & Services: Palliative Care • Respite Care • Convalescent Care • Own GP if required • Own Furniture if required • Pets by arrangement • Smoking not permitted • Close to Local shops • Near Public Transport • Minibus or other transport • Lift • Wheelchair access • Gardens for residents • Phone Point in own room/Mobile • Television point in own room • Residents Internet Access
'''

#print (text)



sents = sent_tokenize(text)



firstsentence = (sents[0])
tagged=pos_tag(word_tokenize(firstsentence))
entities=ne_chunk(tagged)      #to identify Named entities.
print(entities)


grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = RegexpParser(grammar)
result = cp.parse(entities)
result.draw()



#
#
# def ie_preprocess(document):
#     sentences = sent_tokenize(document)
#     sentences = word_tokenize(sent) for sent in sentences
#     sentences = pos_tag(sent) for sent in sentences
