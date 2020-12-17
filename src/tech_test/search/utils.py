import nltk
import re
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from autocorrect import Speller
from .dictionaries import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .models import Job
from iso3166 import countries

def get_query_request_handle(request, *args):
    """gets the users inputs and extracts the most correct filters

    Args:
        request and 3 lists with possible aggregators skills, type and organization

    Returns:
        a context dictionary and the same three lists after checking if the checkboxes are ticked 
    """
    context = {}

    job_search = request.GET.get('job_search',"")
    context['job_search'] = job_search

    place_search = request.GET.get('place_search',"")
    try:
        place_search = countries.get(place_search[4])
    except:
        place_search = ''
    context['place_search'] = place_search

    if request.GET.get('remote_search',"") == 'on':
        remote_search = 'checked'
    else:
        remote_search = ''
    context['remote_search'] = remote_search
    skill_, type_ = main_search_handler(job_search)
    skills = set()
    types = set()
    orgs = set()
    if skill_ is not None:
        skills.add(skill_)

    if type_ is not None:
        types.add(type_)

    for val in request.GET.keys():
        if 'skill.' in val:
            aux  = val.split(".", 1)[1]
            skills.add(aux)
        if 'type.' in val:
            aux  = val.split(".", 1)[1]
            types.add(aux)
        if 'org.' in val:
            aux  = val.split(".", 1)[1]
            org.add(aux)
    
 
    args = args[0]

    skills_checkbox = args[0]
    for skill in skills_checkbox:
        if skill.get('value') in skills:
            skill['checked'] = 'checked'
    context['skills_checkbox'] = skills_checkbox

    type_checkbox = args[1] 
    for type in type_checkbox:
        if type.get('value') in types:
            type['checked'] = 'checked'
    context['type_checkbox'] = type_checkbox

    org_checkbox = args[2] 
    for org in org_checkbox:
        if org.get('value') in orgs:
            org['checked'] = 'checked'
    context['org_checkbox'] = org_checkbox

    skills = list(skills)
    types = list(types)
    orgs = list(orgs)

    filters = skills + types + orgs + [place_search]
    if remote_search != '':
        filters += ['Remote']
    context['filters'] =  filters 

  
    return context, skills, types, orgs

def parse_jobs(jobs):
    """Create the object jobs with the information getted

    Args:
        jobs ([type]): a list of dictionaries with jobs 
    """
    for job in jobs:
        id = job.get('id', '')
        objective = job.get('objective', '')
        type = job.get('type', '')
        organization_name = ''
        organization_picture = ''
        try:
            organization_name = job.get('organizations')[0].get('name')
        except :
            break
        try:
            organization_picture = job.get('organizations')[0].get('picture')
        except :
            pass

        locations = job.get('locations', '')
        remote = job.get('remote', '')
        if remote:
            locations.append("Remote")
        if len(locations) != 0:
            locations = ', '.join(locations)
        skills =[]
        for skill in job.get('skills'):
            skills.append(skill.get('name', ''))
        skills = ', '.join(skills)
        if job.get('compensation') != None:
            if job.get('compensation').get('visible') != None:
                try:
                    min = str(job.get('compensation').get('data').get('minAmount'))
                    max = str(job.get('compensation').get('data').get('maxAmount'))
                    curr = str(job.get('compensation').get('data').get('currency'))
                    per = str(job.get('compensation').get('data').get('periodicity'))
                    if min == 'None':
                        max = max.split('.', 1)[0]
                        compensation = f'{max} {curr}/{per}'
                    elif max == 'None':
                        min = min.split('.', 1)[0]
                        compensation = f'{min} {curr}/{per}'
                    else:
                        min = min.split('.', 1)[0]
                        max = max.split('.', 1)[0]
                        compensation = f'{min} - {max} {curr}/{per}'
                except:
                    pass
                
            else:
                compensation = ''
        else:
            compensation = ''
        obj = Job.objects.create(_id = id, objective = objective, type = type, organization_name = organization_name,
        organization_picture = organization_picture, locations = locations, remote = remote, skills = skills,
        compensation = compensation)


def main_search_handler(search):
    """Using nlp extracts the most accurate filters to be used

    Args:
        search ([string]): users input

    Returns:
        returns the best filter of skill and type
    """
    search = re.sub(r'[^a-zA-Z ]', '', search)
    search = search.lower()
    tokenized_search = word_tokenize(search)
    for word in tokenized_search:
        if word in stopwords.words('english'):
            tokenized_search.remove(word)

    stemmer = PorterStemmer()
    spell = Speller(lang='en')
    for i in range(len(tokenized_search)):
        tokenized_search[i] = stemmer.stem(spell(tokenized_search[i]))

    skill_val = None
    type_val = None
    d_s = {}
    for word_seach in tokenized_search:
        w1 = wordnet.synsets(word_seach)
        s_skill = 0
        s_type = 0
        for skill in skills_d.keys():
            w2 = wordnet.synsets(skill)
            if w1 and w2: #Thanks to @alexis' note
                s = w1[0].wup_similarity(w2[0])
                if(s is not None and s > s_skill and s > 0.8):
                    s_skill = s
                    skill_val = skills_d.get(skill,'')
        d_s[s_skill] = skill_val
        for type in types_d.keys():
            w2 = wordnet.synsets(type)
            if w1 and w2: #Thanks to @alexis' note
                s = w1[0].wup_similarity(w2[0])
                if(s is not None and s > s_type and s > 0.8):
                    s_type = s
                    type_val = types_d.get(skill,'')
    return skill_val, type_val


