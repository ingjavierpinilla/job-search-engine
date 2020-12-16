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


def j_print(obj, name):

    #J = json.dumps(obj, sort_keys=False, indent=4)
    #print(J)
    with open(f'{name}.json', 'w') as outfile:
        json.dump(obj, outfile, indent=4)

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

def search_job():
    url = 'https://search.torre.co/opportunities/_search/?currency=USD%24&page=0&periodicity=hourly&lang=en&size=2&aggregate=false&offset=0'
    header = {"content-type": "application/json"}
    payload = {"remote":{"term":True}}
    x= requests.post(url,data=json.dumps(payload), headers=header, verify=False)
    if(x.status_code!=200):
       print("error")
    j_print(x.json(),"results")

search_job()
