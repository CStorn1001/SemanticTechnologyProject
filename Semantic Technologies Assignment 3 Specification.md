#Semantic Technologies Assignment 3: Specification

---

### **1. Introduction**

For this assignment you have to retrieve a number of simple sentences from an existing web page, extract the relevant information from these sentences and transform this information into an RDF knowledge graph with the help of the RDF Mapping Language ([RML](https://rml.io/specs/rml/)). Once this RDF knowledge graph is available, you have to display it in Turtle notation. You also have to write a number of SPARQL queries that extract information from the knowledge graph. Finally, you have to produce a 3-minute video that explains the details of your Python implementation and how you built the RML mapping rules.

Please download the folder "[assignment-3-start.zip](https://ilearn.mq.edu.au/pluginfile.php/7626839/mod_page/content/80/assignment-3-start.zip?time=1651236988019)" to start with this assignment. This folder contains a version of [SDM-RDFizer](https://github.com/SDM-TIB/SDM-RDFizer), a configuration file "config.ini" for the RDFizer, an incomplete file "mapping.ttl" for the RML mapping rules to be added, and an HTML file "student.html" that contains the information to be extracted.

### 

### **2. Extracting Information**

Fetch the following web page ("student.html") from a browser via a HTTP request:

![Image]({"cacheID":"a18ce884-1db9-48bc-87db-80a19e6c4621","cacheDataKey":"0EXC3bAsk6TOfFEsVpfSb/Gn8LccejUe3m4DPXAGRYU=","url":"https://cache-elements.s3.amazonaws.com/document_cache/83c79dc2-0775-4c8b-857b-84c27dfe703c"})

To do this, use the command prompt and go to the folder where the HTML file "student.html" is located and start a simple Python HTTP server from the command line:

```
   C:>python -m http.server 8080
```

The Python program "student.py" should request the HTML document ("student.html") from the browser via:

```
   http://localhost:8080/student.html
```

You have to use the Python "requests" module for this task.

Afterwards, use the [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to extract the raw text from the HTML file "student.html" and [spaCy](https://spacy.io/) to extract the sentences from the text and store these sentences in a list:

```
['Kevin Walker is a student.', 
 'Kevin Walker was born on 2001/07/24.', 
 'Kevin Walker lives in Epping.', 
 'Kevin Walker works at ALDI.', 
 'Kevin is a friend of Alice Miller.', 
 'Kevin is studying at Macquarie University.', 
 'He has the student number 40048822.', 
 'He is enrolled in COMP3100 and in COMP3220.', 
 'Alice Miller is an alumna of Macquarie University.', 
 'She is a friend of him.']
```

For each of these ten sentences extract the subject (source), the predicate (edge), and the object(s) (target) and store the resulting information in **exactly** the same way as shown below in a pandas DataFrame. Again, you have to use spaCy to extract the relevant information from these sentences. It is up to you, if you only want to use the [linguistic features](https://spacy.io/usage/linguistic-features) that are available as token attributes in spaCy or spaCy's [matcher engine](https://spacy.io/usage/rule-based-matching) or a combination of both to extract the information. Note that you have also to resolve anaphoric expressions during this extraction process like: *him* --> *he* --> *Kevin* --> *Kevin Walker* and normalise these expressions (as illustrated below).

```
          source                edge                target
0   Kevin Walker                is a               student
1   Kevin Walker             born on            2001-07-24
2   Kevin Walker            lives in                Epping
3   Kevin Walker            works at                  ALDI
4   Kevin Walker        is friend of          Alice Miller
5   Kevin Walker      is studying at  Macquarie University
6   Kevin Walker  has student number              40048822
7   Kevin Walker      is enrolled in              COMP3100
8   Kevin Walker      is enrolled in              COMP3220
9   Alice Miller        is alumna of  Macquarie University
10  Alice Miller        is friend of          Kevin Walker
```

```

```

### **3. Adding RML Mapping Rules**

Take the DataFrame and translate the information in this DataFrame into suitable csv files that serve as data sources for the RML mapping document "mapping.ttl". Note that the file "mapping.ttl" initially contains only the prefixes of the IRIs for the N-Triples:

```
@base  <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <http://schema.org/> .
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .
@prefix ql: <http://semweb.mmlab.be/ns/ql#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
```

Add RML mapping rules to the file "mapping.ttl" that transform the information in the csv files into N-Triples notation. Once the RML mapping rules are defined, you can launch the transformation in the following way from your Python program:

```
   import os
   os.system("python -m rdfizer -c ./config.ini")
```

Note that you may also have to install the following two modules in order to run the rdfizer:

```
   pip install mysql-connector-python
```

```
   pip install psycopg2
```

```
If the transformation was successful, then the file "triples.nt" will contain the following N-Triples:
```

```
<http://example.org/Kevin%20Walker> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/student>.
<http://example.org/Kevin%20Walker> <http://schema.org/birthDate> "2001-07-24"^^<http://www.w3.org/2001/XMLSchema#date>.
<http://example.org/Kevin%20Walker> <http://schema.org/addressLocality> <http://example.org/Epping>.
<http://example.org/Kevin%20Walker> <http://schema.org/workLocation> <http://example.org/ALDI>.
<http://example.org/Kevin%20Walker> <http://xmlns.com/foaf/0.1/knows> <http://example.org/Alice%20Miller>.
<http://example.org/Kevin%20Walker> <http://schema.org/study> <http://example.org/Macquarie%20University>.
<http://example.org/Kevin%20Walker> <http://schema.org/identifier> "40048822"^^<http://www.w3.org/2001/XMLSchema#positiveInteger>.
<http://example.org/Kevin%20Walker> <http://schema.org/courseCode> <http://example.org/COMP3100>.
<http://example.org/Kevin%20Walker> <http://schema.org/courseCode> <http://example.org/COMP3220>.
<http://example.org/Alice%20Miller> <http://schema.org/alumniOf> <http://example.org/Macquarie%20University>.
<http://example.org/Alice%20Miller> <http://xmlns.com/foaf/0.1/knows> <http://example.org/Kevin%20Walker>
```

You can visualise the resulting N-Triples as a connected graph. You **don't** have to generate this graphical representation for this assignment, but the graph may help you to inspect the triples, when you develop the mapping rules. I used the online [RDF Grapher](https://www.ldf.fi/service/rdf-grapher) for this purpose.

### ![Image]({"cacheID":"bb323ba2-90d2-4e4b-9b00-ab50d984a615","cacheDataKey":"mQR+XbBsTkcdNKapmsB++5mE/5zcRwRv4HpExBdjOZc=","url":"https://cache-elements.s3.amazonaws.com/document_cache/e878d060-6694-4279-80bf-708fa5b58092"})

### 

### **4. Displaying N-Triples in Turtle Notation**

Use Python's rdflib library, read the file "triples.nt", and display these triples of the knowledge graph in Turtle notation. The output should look as follows:

```
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ns1: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/Alice%20Miller> ns1:alumniOf <http://example.org/Macquarie%20University> ;
    foaf:knows <http://example.org/Kevin%20Walker> .

<http://example.org/Kevin%20Walker> a <http://example.org/student> ;
    ns1:addressLocality <http://example.org/Epping> ;
    ns1:birthDate "2001-07-24"^^xsd:date ;
    ns1:courseCode <http://example.org/COMP3100>,
        <http://example.org/COMP3220> ;
    ns1:identifier "40048822"^^xsd:positiveInteger ;
    ns1:study <http://example.org/Macquarie%20University> ;
    ns1:workLocation <http://example.org/ALDI> ;
    foaf:knows <http://example.org/Alice%20Miller> .
```

```

```

### **5. Querying the RDF Knowledge Graph**

Translate the following six questions into SPARQL queries and answers these queries over in the RDF knowledge graph. Use JSON notation to display the answer for each question as illustrated below:

Who is a student?

**\[{'who': 'Kevin%20Walker'}\]** 

When was Kevin Walker born?

**\[{'when': '2001-07-24'}\]** 

Where does Kevin Walker live and work?

**\[{'where_addr': 'Epping', 'where_loc': 'ALDI'}\]** 

Who is a friend of whom?

**\[{'who': 'Kevin%20Walker', 'whom': 'Alice%20Miller'}, {'who': 'Alice%20Miller', 'whom': 'Kevin%20Walker'}\]** 

Who is an alumna of Macquarie University and a friend of Kevin Walker?

**\[{'who': 'Alice%20Miller'}\]** 

In how many courses is Kevin Walker enrolled?

**\[{'count': '2'}\]** 

### **6. Producing a Video**

Produce a 3-minute video ("student.mp4") that presents your implementation. In this video, you should walk the spectator through the code of your Python program and your RML mapping rules and **explain** the details of your implementation in your own words. Focus on those parts of the implementation that are novel and haven't already been discussed in the practical tasks of Week 7 and 8. You can use the free screen recorder [FlashBack Express](https://www.flashbackrecorder.com/express/) or [Zoom](https://zoom.us/) to produce your video.

### **7. Assessment**

This assignment is worth **20 marks** in total. You will be awarded marks for the correctness and quality of your code and the content of your video according to the following criteria:

|Criteria |Marks   |Explanation |
|---|---|---|
|Code Quality<br> |3<br> |Your code follows a consistent style, is easy to understand, and has been well-documented.<br> |
|Information Extraction<br> |5<br> |All the textual information is extracted and represented <br> |
|RML Rules<br> |4<br> |The information in the pandas DataFrame is translated into suitable csv files of your choice (1 mark); RML mapping rules then take these csv files as data sources and produce N-Triples as output (in the file "triples.nt") as illustrated above (3 marks).<br> |
|N-Triples in Turtle Notation<br> |1<br> |Using Python's rdflib library, the N-Triples are read from the file "triples.nt" and displayed in Turtle notation.<br> |
|SPARQL Queries<br> |3<br> |The six SPARQL queries that are answered over the knowledge graph and the correct answers to these queries are displayed in JSON notation as illustrated above.<br> |
|Video<br> |4<br> |The video explains the Python code (2 marks)  and the RML mapping rules (2 marks) in detail, with a particular focus on the new elements of your solution.<br> |
