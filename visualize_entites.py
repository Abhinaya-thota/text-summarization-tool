import spacy
from spacy import displacy
from pathlib import Path
import webbrowser
import os

# Load spaCy model for entity recognition
nlp = spacy.load("en_core_web_sm")

# Function to extract entities and visualize them
def visualize_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # # Display the original text
    # print("Original Text:")
    # print(text)
    
    # Display the entities extracted from the text
    print("\nEntities:")
    print(entities)

    # Save the visualization to a file
    svg = displacy.render(doc, style="ent")
    output_path = Path(__file__).parent / "entity_visualization.html"
    output_path.write_text(svg, encoding="utf-8")
    
    # Open the visualization file in the default web browser
    webbrowser.open("file://" + os.path.abspath(output_path))

# Process text and visualize entities
    
# with open("sumdataset.txt", "r", encoding="utf8") as f:
#     text = f.read()

# visualize_entities(text)
