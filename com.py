import requests
import time
import json
import pickledb
from bs4 import BeautifulSoup
 
 
 
 
db = pickledb.load('data.db', False)


to_strip = ["<td>", "</td>", "<h3>", "</h3>"]
selectors = {
    'name' : ".sign-head > h3",
}
BASE_URL = "https://www.covenantofmayors.eu/about/covenant-community/signatories/{cat}.html?scity_id={id}"


data_types = [
'estimated_reduction', 
'expected_evolution', 
'estimated_reduction_2030',
'expected_evolution_2030',
'estimated_reduction_longterm',
'expected_evolution_longterm',]

DATA_URL = "https://www.covenantofmayors.eu/about/covenant-community/signatories/action-plan.html?task=actionplan.{data_type}&orgid={id}"
categories = ["overview", "baseline-review", "action-plan", "progress"]

def dump_url(id):
    url = BASE_URL.format(cat=categories[0], id=id)
    page = requests.get(url)
    if not page: return False
    
    name = extract_name(page)
    if not name: return False, False
    
    dumps = dump_ajax_data(id)
    
    
    return name, dumps

def extract_name(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    data = {}
    for name, sel in selectors.items():
        results = soup.select(sel)
        r = str(results[0])
        r = sanitize(r)
        data[name] = r
    name = data.get('name', False)
    return name
        
def dump_ajax_data(id):
    dumps = {}
    for data_type in data_types:
        dumps['id'] = id
        page = requests.get(DATA_URL.format(data_type=data_type, id=id))
        extract_ajax_data(page, dumps, data_type)
    return dumps

def extract_ajax_data(page, dumps, data_type):
    jpage = page.json()
    
    if jpage.get('rstatus', False):
        dumps[data_type] = jpage
        
        names = jpage.get('rname')
        values = jpage.get('rvalue')
        percs = jpage.get('percentage')
        data = {}
        for i in range(0, len(names)):
            data[names[i]] = values[i]
            data[names[i]+'perc'] = percs[i]
        dumps[data_type] = data
    else:
        dumps[data_type] = "N/A"
        
def sanitize(s):
    for dead in to_strip:
        s = s.replace(dead, "")
    return s
    



start_index = db.get('i')
if __name__ == "__main__":
    for id in range(start_index, 29999):
        if not id%25: print(id)
        time.sleep(0.33)
        name, dump = dump_url(id)
        if name:
            print(name)
            db.set(name, dump)
        db.set('i', id)
        db.dump()

