import requests
import json
import difflib
requests.packages.urllib3.disable_warnings()

def jprint(x):
    print(json.dumps(x, indent=4))

def get_opportunity_by_id(id):

    x = requests.get(f'https://torre.co/api/opportunities/{id}')
    if(x.status_code!=200):
        return 
    j_keys(x.json())

def get_aggregators():
    """[summary]
    will return information about  valid aggregators and their valid values and total
    Returns:
        [dictionay]: {'remote': [{'total': 37076, 'value': 'yes'}, {'total': 18987, 'value': 'no'}], 'skill': [{'total': 5082, 'value': 'Software Development'}
    """
    url = 'https://search.torre.co/opportunities/_search/?currency=USD%24&page=0&periodicity=hourly&lang=en&size=0&aggregate=true&offset=0'
    header = {"content-type": "application/json"}
    x = requests.post(url, headers=header, verify=False)
    keys = x.json()['aggregators']
    keys.pop('organization')
    keys.pop('status')
    return keys

def payload_generator(remote = False, skills = [], type = [], compensationrange = [], timezone = []):
    """[summary]
        generate a valid payload to generate a post request, it will take tha values in the different lists
        and generate the payload depending on each specific field
    Args:
        remote (bool, optional): [description]. Defaults to False.
        skills (list, optional): [description]. Defaults to [].
        type (list, optional): [description]. Defaults to [].
        compensationrange (list, optional): [description]. Defaults to [].
        timezone (list, optional): [description]. Defaults to [].

    Returns:
        [dictionary]: A dictionary with the form {"and": [{"remote": {"term": True}}, {"skill": {"term": skill, "experience": "potential-to-develop"}}]}
    """
    l = []

    l.append({"remote": {"term": remote}})
    if len(skills) != 0:
        for skill in skills:
            l.append({"skill": {"term": skill, "experience": "potential-to-develop"}})
    
    if len(type) != 0:
        for t in type:
            {"type": {"code": t}}

    if len(compensationrange) != 0:
        for range in compensationrange:
            l.append({"skill": {"term": skill, "experience": "potential-to-develop"}})

    if len(timezone) != 0:
        for zone in timezone:
            l.append({"skill": {"term":skill, "experience": "potential-to-develop"}})

    return {"and": l}


def search_job(main_seacrh = "", size = 2, place = [], remote = False, skills = [], type = [], compensationrange = [], timezone = []):
    url = f'https://search.torre.co/opportunities/_search/?currency=USD%24&page=0&periodicity=hourly&lang=en&size={size}&aggregate=false&offset=0'
    header = {"content-type": "application/json"}
    payload = payload_generator(remote, skills = skills, type = type)
    x = requests.post(url,data=json.dumps(payload), headers=header, verify=False)
    if(x.status_code!=200):
       return None
    return x.json()['results']
 
