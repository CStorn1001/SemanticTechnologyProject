import spacy
from spacy.matcher import Matcher
from spacy import displacy
from bs4 import BeautifulSoup
import pandas as pd

#opening the html server we created with the student data and parsing it into python
with open ('student.html') as f:
    student_html = BeautifulSoup(f, 'html.parser')
# removing html tags and grabbing the text within the html tags
student_text = student_html.get_text()

#cleaning the data
#firstly remove the title of 'Informal Triples for Assignment 3
student_text = student_text.replace('\n\n\nStudent\n\nInformal Triples for Assignment 3\n', '')
#remove all the spaces (\n) from string
student_text = student_text.replace('\n', ' ')

#Using spacy to extract the text into a list of sentences
nlp = spacy.load('en_core_web_sm')
student_list = [token.text for token in nlp(student_text).sents] 
#we do this as the last item is empty - probably occurs due to the extraction above
student_list = student_list[:-1]

#printing to make it the same result as shown within the notification
print()
print()
print('STUDENT LIST')
print()
for idx, tok in enumerate(student_list):
    if idx == 0:
        print(f"['{tok}',")
    elif idx == len(student_list)-1:
        print(f" '{tok}', ]")
    elif idx!=0 and idx !=len(student_list)-1:
        print(f" '{tok}',")
#printing spaces
print()
print()

# Splitting the sentence with COMP units into two sentences
res1 = ''
res2 = ''
student_sents = []
for i in student_list:
    #if the word 'and' occurs we will split and make into two sentences
    if 'and' in i:
        q = i.split(' and ')
        res1 = q[0]+'.'
        p2 = q[1]
        p1 = res1.split('in')[0]
        res2 = p1+q[1]
        student_sents.append(res1)
        student_sents.append(res2)
    elif 'and' not in i:
        student_sents.append(i)


#### Extraction of Subject, Predicate and Object

#### function similar to practical wk7 but with some minor changes
#used to get the Subject and Object
def get_entities(sent):  
  ent1 = ""           # Variable for storing the subject.
  ent2 = ""           # Variable for storing the object.
  prv_tok_dep = ""    # Variable for dependency tag of previous token in the sentence.
  prv_tok_text = ""   # Variable for previous token in the sentence.
  prefix = ""         # Variable for storing compounds.
  modifier = ""       # Variable for storing modifieres.
  # Loop through the tokens in the sentence.
  for idx, tok in enumerate(nlp(sent)):
    # Check if a token is a punctuation mark or not.
    if tok.dep_ != 'punct':
      # Check if a token is a compound one or not.
      if tok.dep_ == 'compound':
        # If yes, then store the token in the prefix variable.
        prefix = tok.text
        # Check if the previous token was also a compound one.
        if prv_tok_dep == 'compound':
          # If yes, then update the prefix variable.
          predix = prv_tok_dep + " "+ tok.text  
      # Check if a token is a modifier or not.
      if tok.dep_.endswith("mod") == True:
        # If yes, then store the token in the modifier varible.
        modifier = tok.text
        # Check if the previous token was a compound one.
        if prv_tok_dep == "compound":
          # If yes, then update the modifier variable.
          modifier = prv_tok_dep + " " + tok.text  
      # Check if a token is the subject.
      if tok.dep_.find("subj") == True:
        # If yes, then concatenate the modifier, prefix, and token
        # and assign the result to the subject variable (ent1).
        ent1 = modifier + " "+ prefix + " "+ tok.text
        # Reset the following variables: prefix, modifier, prv_tok_dep, and prv_tok_text.
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""
      # Check if a token is the object.
      if tok.dep_.find("obj") == True or idx ==len(nlp(sent))-2:
        ent2 = modifier + " "+ prefix + " "+ tok.text
        #check to see if token includes nummoid which is the student number
        if tok.dep_ == "nummod":
          ent2 = tok.text
        else:
          # If yes, then concatenate the modifier, prefix, and token 
          # and assign the result to the object variable (ent2).
          ent2 = modifier + " "+ prefix + " "+ tok.text   
      # Update the variable for the dependency tag for the previous token. 
      prv_tok_dep = tok.dep_
      # Update the variable for the previous token in the sentence.
      prv_tok_text = tok.text
  return [ent1.strip(), ent2.strip()]
#calling to get both subject and objects of the student sentences
entity_pairs = []
for i in student_sents:
    entity_pairs.append(get_entities(i))

#function to get predicate items within a sentence
def get_predicates(sent):
    doc = nlp(sent)
    #enumerate so I can grab both the index and the value - easy for me to move forward and backwards within a setence
    for idx, val in enumerate(doc):
        #only allowed if not first item and last item (at index +2)
        if idx != 0 or doc[idx+2].text != doc[-1].text:
            #if the token equals a verb
            if val.dep_ == 'ROOT':
                #if forward and backward do not includes any aux or auxpass and not the word 'was'
                if doc[idx-1].text != 'was' and (doc[idx-1].dep_ == 'aux' or doc[idx-1].dep_ == 'auxpass'):
                    if doc[idx+1].dep_ == 'prep':
                        #combine together item-1, item and item+1 as a predicate
                        return doc[idx-1].text + ' ' + val.text + ' ' + doc[idx+1].text
                    #if was then we will combine just the item and item+1 for a predicate
                    if doc[idx-1].text == 'was':
                        return val.text + ' ' + doc[idx+1].text
                elif doc[idx-1].dep_ != 'aux' or doc[idx-1].dep_ != 'auxpass':
                    if doc[idx+1].dep_ == 'det' or doc[idx+1].dep_ == 'prep':
                        # if tiem forward 2 does not include student and is equal to a dependency attribute or compound is true
                        if doc[idx+2].text != 'student'  and (doc[idx+2].dep_ == 'attr' or doc[idx+2].dep_ == 'compound'):
                            if doc[idx+3].dep == 'dobj' or doc[idx+3].dep == 'prep':
                                #combined item, item+2 and item+3 into a predicate
                                return val.text + ' ' + doc[idx+2].text + ' ' + doc[idx+3].text
                            else:
                                #else if not of above then combine the same items indexes into a predicate
                                return val.text + ' ' + doc[idx+2].text + ' ' + doc[idx+3].text
                        #if does include student at item+2 is true
                        elif doc[idx+2].text == 'student':
                            #combine item and item+1 as a predicate ('is a')
                            return val.text + ' ' + doc[idx+1].text
                        elif doc[idx+2].dep_ != 'attr' or doc[idx+2].dep_ != 'compound':
                            #combine item and item+1 into predicate
                            return val.text + ' ' + doc[idx+1].text

#callling and store the predicates into a list
predicate_entities = []
for i in student_sents:
    predicate_entities.append(get_predicates(i))

#Extracting words into final lists (some cleaning must be done)

subjects_list = [i[0] for i in entity_pairs]
subjects = [] 
#replacing the particular pronouns such as he, she and also first names with the given name
for i in subjects_list:
    if i == 'Kevin':
        i = i.replace('Kevin', 'Kevin Walker')
    if i == 'He':
        i = i.replace('He', 'Kevin Walker')
    if i == 'She':
        i = i.replace('She', 'Alice Miller')
    subjects.append(i)

# Extracts objects.
objects_list = [i[1] for i in entity_pairs]
objects = []

for i in objects_list:
    # coverting the date of '/' into '-'
    if '/' in i:
        i = i.replace('/', '-')
    objects.append(i)

#extracting the predicates
predicates_list = [i for i in predicate_entities]
predicates=[]
for i in predicates_list:
    if 'the' in i:
        i = i.replace('the', 'student number')
    predicates.append(i)

# store object, subject and predicate lists  within a pandas data frame
df = pd.DataFrame({'source': subjects, 'edge':predicates, 'target': objects})

#printing the dataframe
print('STUDENT EXTRACTION INFORMATION DATAFRAME')
print()
print(df)

#Create csv of dataframe
df.to_csv('student_extract.csv', index= False)

################################PRE-PROCESSING FOR RML MAP - Placing data into csv files########################################
#This helps with the next stage of RML mapping where we split each row of the csv file into a seperate csv
#The link below helped develop a function to split csv files into a certain amount of rows and files
#https://www.geeksforgeeks.org/how-to-create-multiple-csv-files-from-existing-csv-file-using-pandas/
def csv_splitter(csv, nfiles, nrows):
    data = pd.read_csv(csv)
    for i in range(nfiles):
        df = data[nrows*i:nrows*(i+1)]
        df.to_csv(f'row_{i+1}.csv', index=False)

#calling developed function
csv_splitter('student_extract.csv', 11, 1)

#########################################################RML mapping #########################################################
### RML-mapping
#used to execute the mapping.ttl file into the triples.nt file

import os
os.system('python -m rdfizer -c ./config.ini')

######################################################### CONVERTING NTRIPLES TO TURTLE NOTATION ############################
import rdflib

graph = rdflib.Graph()
result = graph.parse("triples.nt", format="ntriples")

output = result.serialize(format='turtle') 
print()
print()
print('TURTLE NOTATION')
print()
print(output)
print()

######################################################### SPARQL QUERIES #########################################################

graph = rdflib.Graph()
res = graph.parse("triples.nt", format="ntriples")

print()
print('SPARQL QUERIES')
print()
#Q1 -Who is a student?
#[{'who': 'Kevin%20Walker'}] 
result1 = graph.query(""" SELECT ?who WHERE { ?who <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/student>. } """)
# print(result1.serialize(format="json"))
dict1 = {}
for i in result1:
    dict1.update({'who': str(i["who"])[-14:]})
print([dict1])

#Q2 -When was Kevin Walker born?
#[{'when': '2001-07-24'}] 
#?where "2001/07/24"^^
#?where"^^
#<http://www.w3.org/2001/XMLSchema#int> .
result2 = graph.query(""" SELECT ?when WHERE { ?somebody <http://schema.org/birthDate> ?when. } """)
# print(result2.serialize(format="json"))
dict2 = {}
for i in result2:
     dict2.update({'when': str(i["when"])})
print([dict2])

#Q3 -Where does Kevin Walker live and work?
#[{'where_addr': 'Epping', 'where_loc': 'ALDI'}] 
result3 = graph.query(""" SELECT ?where_addr ?where_loc WHERE { ?somebody <http://schema.org/addressLocality> ?where_addr. ?somebody <http://schema.org/workLocation> ?where_loc. } """)
# print(result3.serialize(format="json"))
dict3 = {}
for i in result3:
    dict3.update({'where_addr': str(i["where_addr"][-6:]) , 'where_loc': str(i["where_loc"][-4:])})
print([dict3])

#Q4 -Who is a friend of whom?
# [{'who': 'Kevin%20Walker', 'whom': 'Alice%20Miller'}, {'who': 'Alice%20Miller', 'whom': 'Kevin%20Walker'}] 
result4 = graph.query(""" SELECT ?who ?whom WHERE { ?who <http://xmlns.com/foaf/0.1/knows> ?whom . } """)
# print(result4.serialize(format="json"))
dict4p1 = {}
dict4p2 = {}
for i, w in enumerate(result4):
    if i == 0:
        dict4p1.update({'who': str(w["who"][-14:]) , 'whom': str(w["whom"][-14:])})
    if i == 1:
        dict4p2.update({'who': str(w["who"][-14:]) , 'whom': str(w["whom"][-14:])})
print([dict4p1, dict4p2])


#Q5- Who is an alumna of Macquarie University and a friend of Kevin Walker?
# [{'who': 'Alice%20Miller'}] 
result5 = graph.query(""" SELECT ?who WHERE { ?who <http://schema.org/alumniOf> <http://example.org/Macquarie%20University>. ?who <http://xmlns.com/foaf/0.1/knows> <http://example.org/Kevin%20Walker>. } """)
# res5 = result5.serialize(format="json")
dict5 = {}
for i in result5:
    dict5.update({'who': str(i["who"])[-14:]})
print([dict5])

#Q6- In how many courses is Kevin Walker enrolled?
# [{'count': '2'}] 
result6 = graph.query(""" SELECT (COUNT(?subj) as ?count) WHERE { ?kevin <http://schema.org/courseCode> ?subj . } """)
# result6 = result6.serialize(format="json")
dict6 = {}
for i in result6:
    dict6.update({'count': int(i["count"])})
print([dict6])
