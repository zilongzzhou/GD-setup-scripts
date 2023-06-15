import requests
import re
import random

matchId = '1111146'
tailor_base_url = 'http://ssai-tailor-nginx-ingress-k8-pp.npe.hotstar-labs.com/' 


def getMasterManifestUrls(bearer, match_id):
    master_file = open('master.csv', 'w')
    cms_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
        'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Authorization': bearer,
        'Content-Type': 'application/json; charset=utf8',
        'Origin': 'https://admin-pp.hotstar.com',
        'Referer': 'https://admin-pp.hotstar.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'x-tenant-id': 'in'
    }
    base_url = 'https://cmsosiris-pp.pp.hotstar-labs.com/match/' + match_id
    response = requests.get(base_url, headers=cms_headers, verify=False)
    playback_sets = response.json()['body']['results']['clipPlaybackSet']

    ssai_urls = []

    for obj in playback_sets:
        playback_tags = obj['playbackTags']
        cnt_tags = 0
        for tag in playback_tags:
            if (tag['name']== 'ads'):
                cnt_tags += 1
                if tag['value'] != 'ssai':
                    break
            
            # elif (tag['name']== 'resolution'):
            #     cnt_tags += 1
            #     if tag['value'] != 'fhd':
            #         break

            if cnt_tags == 1:
                url = obj['playbackUrl']
                url = tailor_base_url + re.search(r'http(.*)(hls.*)', url).group(2)
                master_file.write(url+'\n')
                ssai_urls.append(url)
                break

    master_file.close()
    return ssai_urls


def generateFinalCSV(childUrls, out):
    n=0
    cnt_arr = [3840,2320,640,240,80,80,960,580,160,60,20,20]
    l=len(childUrls)
    for i in range(0,12):
        for j in range(0,cnt_arr[i]):
            out.write(childUrls[i]+'\n')
            n+=1

    a = ((l-12)/2)-1

    for i in range(0,800):
        ind = random.randint(12,a)
        out.write(childUrls[ind]+'\n')
        n+=1
        
    for i in range(0,200):
        ind = random.randint(a,l-1)
        out.write(childUrls[ind]+'\n')
        n+=1
    
    return n


if __name__ == '__main__' : 

    bearer = 'Bearer eyJraWQiOiI3THFQbUNNU0R2dnNKc051SXlUb1dESnRhNW9UWmZWNFBER2k0QUljU0lZIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULks5aTNPWG5rdzRjX21KbjdiOHBtLURFdS1adXQ2OGdoZjhJWGQ4aEx2TE0ub2Fya3F3OGM0ZDhoTHlLbEUxZDYiLCJpc3MiOiJodHRwczovL2ZveC5va3RhLmNvbS9vYXV0aDIvZGVmYXVsdCIsImF1ZCI6ImFwaTovL2RlZmF1bHQiLCJpYXQiOjE2ODYwNDg3ODgsImV4cCI6MTY4NjA1MjM4OCwiY2lkIjoiMG9hMWg1ZjZsajN3RmtNd3oxZDgiLCJ1aWQiOiIwMHUxbGRta2NmM29rdEF4SDFkOCIsInNjcCI6WyJvZmZsaW5lX2FjY2VzcyIsInByb2ZpbGUiLCJlbWFpbCIsIm9wZW5pZCJdLCJhdXRoX3RpbWUiOjE2ODYwNDg3NzYsInN1YiI6InByYXNvb24uYmFnaGVsQGluLnN0YXJ0di5jb20ifQ.jjmmWzVsvrsCdkynmcw6Z8jUuYVVMNZQn6Z_juA1uZuik95jzsG5n35fPFjSLO7JW0bqggQImDp5eCsBFRt7yp6HDyxwLiXCVGSJTYcMlod5lAxJWgv195EOGSUePEjCSmCfMPXrErrr8DXomOPBoVClgXE_pWTj9AiWqWjjqb4CH7TYrUemidqNwKCY4U1nFMMhVZRpGoMMCzXdlfZSxsXkDfSAXwFle_RTZ8jH3mHAZ7ilhgy9cq_ZDACS7i7hX2mHv7AjkRZ2n9-TNvsSnYjcb_NeZFxKcwQOuh1J-K4mvhAUNohSDT7_s3KsJJDSHAqiMNewlX8UuLRbMK-RWg'
    masterUrls = getMasterManifestUrls(bearer, matchId)

    print("\n******************** GOT {n} MASTER URLS ***********************************\n".format(n=len(masterUrls)))

    child = open('child_layers.csv', 'w')
    childUrls=[]
    
    cnt=1
    for master_url in masterUrls :
        manifest = requests.get(master_url)
        matches = re.finditer(r'(.*)(/hls.*)', manifest.text)
        layers = 0
        for match in matches:
            relativeUrl=match.group(2)
            childUrls.append(relativeUrl)
            child.write(relativeUrl+'\n')
            layers+=1

        print('> Parsed master manifest {cnt}. Found {layers} child layers!'.format(cnt=cnt,layers=layers))
        cnt+=1
    
    child.close()
    print('\n******************** GOT {n} CHILD LAYERS ***********************************\n'.format(n=len(childUrls)))

    print('> Generating final layes csv ... ')
    final_layer = open('layers_final.csv', 'w')
    n = generateFinalCSV(childUrls,final_layer)
    final_layer.close()

    print('\n******************** GENERATED LAYERS CSV WITH {n} ENTRIES ***************\n'.format(n=n))






