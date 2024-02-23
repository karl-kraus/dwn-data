import lxml.etree as ET
import os
import shutil
from acdh_tei_pyutils.tei import TeiReader

editions_folder = os.path.join("data", "editions")
shutil.rmtree(editions_folder, ignore_errors=True)
os.makedirs(editions_folder, exist_ok=True)

file = "./orig_data/Gesamt.xml"
doc = TeiReader(file)

direct_children = [x.tag for x in doc.any_xpath(".//tei:body/*")]
tree = doc.tree
items = []
counter = -1
for i, x in enumerate(doc.any_xpath(".//tei:body/*")):
    try:
        p_number = x.attrib["n"]
    except KeyError:
        p_number = False
    
    if x.tag.endswith("p") and p_number:
        items.append([x])
        counter += 1
    else:
        items[counter].append(x)


for x in items:
    number = f"dwn-{x[0].attrib['n']}"
    file_name = f"{number}.xml"
    save_path = os.path.join(editions_folder, file_name)
    doc = TeiReader(file)
    for bad in doc.any_xpath(".//tei:body"):
        bad.getparent().remove(bad)
    text_node = doc.any_xpath(".//tei:text")[0]
    body = ET.Element("{http://www.tei-c.org/ns/1.0}body")
    text_node.append(body)
    for y in x:
        body.append(y)
    doc.tree_to_file(save_path)









