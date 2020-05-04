import csv, json, re, sys
import requests

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

html_tags = {
    'knowledge_panel': 'kp-blk knowledge-panel',
    'knowledge_panel1': 'kp-wholepage kp-wholepage-osrp HSryR EyBRub',
    'claimed': "Own this business?",
    'name': "K9xsvf lYo97 kno-fb-ctx",
    'Common causes of this symptom': 'BWsxhd kno-fb-ctx',
    'Self-treatment': "lNDTPb",
    'disease':"PyJv1b gsmt PZPZlf",
    'overview': "wQu7gc g6dx0b",
    'symptoms': 'CAAQAA',
    'treatment': 'vnLNtd mnr-c XleQBd B03h3d P6OZi V14nKc ptcLIOszQJu__wholepage-card wp-ms'
}

html_regexes = {
    'name': '<span>(.*?)</span>',
    'named': '<span role="heading" aria-level="1" class="xEaFBe">(.*?)</span>',
    'Common causes of this symptom': '>(.*?)</',
    'Self-treatment': '>(.*?)</',
    'Self-treatment1': '<ul><li class="rnqMqf">(.*?)</li></ul>',
    'overview':'<div class="PZPZlf" data-attrid="kc:/medicine/disease:description">(.*?)</div>',
    'overview1':'<div class="os0Kkc"><div class="m6vS6b PZPZlf" data-attrid="kc:/medicine/disease:long description">(.*?)</div></div><hr>',
    'symptoms':'>(.*?)</',
    'symptoms1':'<span>(.*)</span>',
    'treatment':'</div><div class="m6vS6b PZPZlf" data-attrid="kc:/medicine/disease:long description">(.*?)</div></div><hr>'

}

def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    return r.text

def get_string_after_tag(string, tag, regex, distance):
    if(tag not in string):
        return None

    index = string.find(tag) 
    substr =  string[index:index+distance]
    if re.search(regex,substr):
        #print(re.search(regex,substr).group(1))
        return re.search(regex,substr).group(1)
    else:
        return None

def get_details(query):
    html_results = google(query)
    results = {'query':query}
    has_knowledge_panel = html_tags['knowledge_panel'] in html_results

    if(has_knowledge_panel):
        results['exists'] = True
        results['name'] = get_string_after_tag(html_results, html_tags['name'],html_regexes['name'],300)

        causes = get_string_after_tag(html_results, html_tags['Common causes of this symptom'],html_regexes['Common causes of this symptom'],800) #280
        if(causes==None):
            results['causes'] = str("")
        else:
            results['causes']= str(causes)

        treatment1 = get_string_after_tag(html_results, html_tags['Self-treatment'],html_regexes['Self-treatment'],1000)
        treatment2 = get_string_after_tag(html_results, html_tags['Self-treatment'],html_regexes['Self-treatment1'],1000)
        clean = re.compile('<.*?>')
        treatment2=re.sub(clean, ' ', str(treatment2))
        if(treatment2==None):
            results['treatment'] = str(treatment1) 
        elif(treatment1==None):
            results['treatment'] =  str(treatment2)
        else:
            results['treatment'] = str(treatment1) + str(treatment2)

    else:
        results['exists'] = False
    
    print(results)
    return results

def get_detailsdisease(query):
    html_results = google(query)
    results = {'query':query}
    has_knowledge_panel = html_tags['knowledge_panel1'] in html_results

    if(has_knowledge_panel):
        results['exists'] = True
        results['name'] = get_string_after_tag(html_results, html_tags['disease'],html_regexes['named'],300)

        causes1 = get_string_after_tag(html_results, html_tags['overview'],html_regexes['overview'],1000) #280
        causes2 = get_string_after_tag(html_results, html_tags['overview'],html_regexes['overview1'],1000) #280
        clean = re.compile('<.*?>')
        causes2=re.sub(clean, '', str(causes2))
        if (causes1==None):
            results['causes'] =  str(causes2)
        elif(causes2==None):
            results['causes'] = str(causes1) 
        else:
            results['causes'] = str(causes1) + str(causes2)

        # print("++++++")
        # causes1 = get_string_after_tag(html_results, html_tags['symptoms'],html_regexes['symptoms'],20000)
        # symptoms2 = get_string_after_tag(html_results, html_tags['symptoms'],html_regexes['symptoms1'],1000)
        # clean = re.compile('<.*?>')
        # causes1=re.sub(clean, '', str(causes1))
        # print("---------",causes1)
        # if(symptoms):
        #     results['symptoms'] = symptoms

        # print("++++++")
        # treatment = get_string_after_tag(html_results, html_tags['treatment'],html_regexes['treatment'],20000)
        # print("_________",treatment)
        # if(treatment):
        #     results['treatment'] = treatment

    else:
        results['exists'] = False
    
    print(results)
    return results

if __name__ == "__main__":
    #get_details('diarrhea')
    #get_detailsdisease('alzheimer')
