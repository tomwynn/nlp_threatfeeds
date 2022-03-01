# library imports
import pandas as pd
import spacy
from spacy import displacy
from spacy.tokens import DocBin
import json
from datetime import datetime
from tqdm import tqdm
import re

def read_sw_csv():
    col_list = ["Name"]
    df = pd.read_csv(("mitre attck software - Sheet1.csv"), usecols=col_list)
    sw_list = df["Name"].tolist()
    sw_list = df["Name"].str.lower()
    print(sw_list)
    return sw_list

def read_corpus_csv():
    col_corpus = ["content"]
    df = pd.read_csv("gather.csv",nrows=5, usecols=col_corpus)
    #print(df)
    corpus = df["content"].tolist()
    merged = ' '.join(corpus)
    print(merged)
    return merged

def structure_training_data(merged, sw_list):
    results = []
    entities = []
    collective_dict = {'TRAINING_DATA': []}
    # search for instances of keywords within the text (ignoring letter case)
    for kw in tqdm(sw_list):
        match = re.finditer(r'(?:\b%s\b\s?)+' % kw, merged, flags=re.IGNORECASE)
        
        # store the start/end character positions
        all_instances = [[m.start(),m.end()] for m in match] 
        
        # if the callable_iterator found matches, create an 'entities' list
        if len(all_instances)>0:
            for i in all_instances:
                start = i[0]
                end = i[1]
                entities.append((start, end, kw, "SOFTWARE"))
                #entities.append((start, end, kw, "SOFTWARE"))
        # alert when no matches are found given the user inputs
        else:
            print("No pattern matches found. Keyword:", kw)
                
    # add any found entities into a JSON format within collective_dict
    if len(entities)>0:
        results = [merged, {"entities": entities}]
        collective_dict['TRAINING_DATA'].append(results)
    print(collective_dict)
    return collective_dict

# def create_training(collective_dict):
#     nlp = spacy.blank('en')
#     TRAIN_DATA = collective_dict['TRAINING_DATA']
#     db = DocBin()
#     for text, annot in tqdm(TRAIN_DATA):
#         doc = nlp.make_doc(text)
#         ents = []

#         # create span objects
#         for start, end, label in annot["entities"]:
#             span = doc.char_span(start, end, label=label, alignment_mode="contract") 

#             # skip if the character indices do not map to a valid span
#             if span is None:
#                 print("Skipping entity.")
#             else:
#                 ents.append(span)
#                 # handle erroneous entity annotations by removing them
#                 try:
#                     doc.ents = ents
#                 except:
#                     # print("BAD SPAN:", span, "\n")
#                     ents.pop()
#         doc.ents = ents

#         # pack Doc objects into DocBin
#         db.add(doc)
#     return db
    

if __name__ == '__main__':
    #text1 = "'HAWKBALL"
    sw_list = read_sw_csv()
    corpus = read_corpus_csv()
    collective_dict = structure_training_data(corpus, sw_list)
    # train_data_doc = create_training(collective_dict)
    # train_data_doc.to_disk("TRAIN_DATA.spacy")

    
