import requests
import json

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
    x = requests.post('https://search.torre.co/opportunities/_search/?[offset=0&size=01&aggregate=True&status=close]')
    if(x.status_code!=200):
       print("error")
       return 
    j_print(x.json())

data ={"offset": 0, "size": 1, "aggregate": False}
search_job(data)
