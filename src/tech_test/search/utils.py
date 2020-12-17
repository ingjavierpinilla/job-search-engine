def get_query_request_handle(request, *args):
    context = {}

    job_search = request.GET.get('job_search',"")
    context['job_search'] = job_search

    place_search = request.GET.get('place_search',"")
    context['place_search'] = place_search

    if request.GET.get('remote_search',"") == 'on':
        remote_search = 'checked'
    else:
        remote_search = ''
    context['remote_search'] = remote_search

    skills = []
    types = []
    for val in request.GET.keys():
        if 'skill.' in val:
            aux  = val.split(".", 1)[1]
            skills.append(aux)
        if 'type.' in val:
            aux  = val.split(".", 1)[1]
            types.append(aux)
    
 
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
    filters = skills + types
    if remote_search != '':
        filters += ['Remote']
    context['filters'] =  filters  
    return context, skills, types

def parse_jobs(jobs):
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

