import requests
import json
from

def j_keys(obj):
    try:
        for key in obj.keys(): 
            print(key)
    except:
        try:
            print(len(obj))
        except:
            return


def j_print(obj):

    J = json.dumps(obj, sort_keys=False, indent=4)
    print(J)

def get_user_by_username(username):

    x = requests.get(f'https://torre.bio/api/bios/{username}')
    if(x.status_code!=200):
        return 
    j_keys(x.json())

def get_opportunity_by_id(id):

    x = requests.get(f'https://torre.co/api/opportunities/{id}')
    if(x.status_code!=200):
        return 
    j_keys(x.json())

def search_job(*args, **kwargs):
    x = requests.post('https://search.torre.co/opportunities/_search/?[offset={offset}&size={size}&aggregate={aggregate}]'.format(**data))
    if(x.status_code!=200):
       return 
    j_keys(x.json()["results"])

data ={"offset": 0, "size": 2, "aggregate":""}
search_job(data)
