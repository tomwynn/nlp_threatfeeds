# library imports
import pandas as pd
import spacy
from spacy import displacy
from spacy.tokens import DocBin
import json
from datetime import datetime
from tqdm import tqdm
import re


model_test = "it's fucking crazy we have a  attack holyshit I'm changing this text because this is epic my tear is literally dropping so I call it teardrop"

# load the trained model
nlp_output = spacy.load("outputnew/model-best")

# pass our test instance into the trained pipeline
doc = nlp_output(model_test)

# customize the label colors
colors = {"SOFTWARE": "linear-gradient(90deg, #E1D436, #F59710)"}
options = {"ents": ["SOFTWARE"], "colors": colors}

# visualize the identified entities
displacy.render(doc, style="ent", options=options)

# print out the identified entities
for ent in doc.ents:
    if ent.label_ == "SOFTWARE":
        print("software detected: "+ ent.text, "Label :"+ ent.label_)
print('text: '+model_test )