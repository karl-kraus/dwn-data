import re

import pandas as pd

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import extract_fulltext, get_xmlid, check_for_hash

regex = r"DWrs\w+\d{3}"
subst = ""
file = "./orig_data/Gesamt.xml"
KWIC_SIZE = 40
tag_blacklist = [
    "{http://www.tei-c.org/ns/1.0}ref",
    "{http://www.tei-c.org/ns/1.0}sic",
    "{http://www.tei-c.org/ns/1.0}fw",
]
doc = TeiReader(file)
items = []
for x in doc.any_xpath(".//tei:rs[@type='person'][@key]"):
    item = {}
    mention_id = get_xmlid(x)
    item_key = check_for_hash(x.attrib["key"])
    item["id"] = mention_id
    item["entity_id"] = item_key
    parent_node = x.xpath("ancestor::tei:p[1]", namespaces=doc.nsmap)[0]
    # parent_node = x.getparent().getparent()
    try:
        x.text = x.text + mention_id
    except TypeError:
        x.text = mention_id
    entity_text = extract_fulltext(x, tag_blacklist=tag_blacklist)
    fulltext = extract_fulltext(parent_node, tag_blacklist=tag_blacklist)
    if entity_text:
        mark_up = f"<span>{entity_text}</span>"
        kwic = fulltext.replace(entity_text, mark_up)
        parts = kwic.split(mark_up)
        prev, next = parts
        prev = re.sub(regex, subst, prev, 0, re.MULTILINE)
        next = re.sub(regex, subst, next, 0, re.MULTILINE)
        short_kwic = f"{prev[-KWIC_SIZE:]}{mark_up}{next[:KWIC_SIZE]}"
        short_kwic = short_kwic.replace(f"{mention_id}", "")
        item["kwic"] = short_kwic
    items.append(item)


df = pd.DataFrame(items)
df.to_csv("hansi.csv", index=False)
