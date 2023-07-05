import requests
import re
import random

tailor_host = 'http://ssai-tailor-nginx-ingress-k8-pp.npe.hotstar-labs.com'
# Please replace the s3 path and manipulators with the one you need
mock_server_url = 'https://har-mock-server-dev.npe.hotstar-labs.com/reloader?s3=03_april_tailor_05.har&manipulators=LayerReplicatorManipulator'

def get_urls_from_mock_server():
  response = requests.get(mock_server_url, timeout=200)
  if response.status_code != 200:
    print(response.status_code)
  mock_urls = response.json()['urls']
  return mock_urls

def filter_urls(urls):
  child_urls, master_urls = [], []
  for url in urls:
    if re.match(".*master_\d.*m3u8", url):
      child_urls.append(url)
    else:
      master_urls.append(url)
  return child_urls, master_urls

def remove_host(url):
  return re.search('http.*(/hls.*)', url).group(1)

def generate_tailor_urls(urls):
  template = "{path}?random=1-inallow-test-2023&content_id={content_id}&language={language}&resolution={resolution}&hash=28ea&bandwidth=169400&media_codec=h264&audio_codec=aac&layer=child&playback_proto={playback_proto}&playback_host={playback_host}&si_match_id={si_match_id}&nocache={cache_bypass}"
  content_id = '1910024992'
  language = 'english'
  resolution = '320x180'
  si_match_id = '112259'
  playback_proto = 'https'
  playback_host = 'har-mock-server-dev.npe.hotstar-labs.com'
  cache_bypass = 'true'
  tailor_urls = []
  for url in urls:
    try:
      url = remove_host(url)
    except:
      print(url)
      continue
    tailor_urls.append(template.format(
      path=url,content_id=content_id,language=language,resolution=resolution,
      playback_proto=playback_proto,playback_host=playback_host,si_match_id=si_match_id,cache_bypass=cache_bypass
    ))
  return tailor_urls

def generate_final_csv(urls, out_fname):
  with open(out_fname, 'w') as out:
    n=0
    cnt_arr = [3840,2320,640,240,80,80,960,580,160,60,20,20]
    l=len(urls)
    for i in range(0,12):
      for j in range(0,cnt_arr[i]):
        out.write(urls[i]+'\n')
        n+=1

    a = ((l-12)/2)-1

    for i in range(0,800):
      ind = random.randint(12,a)
      out.write(urls[ind]+'\n')
      n+=1

    for i in range(0,200):
      ind = random.randint(a,l-1)
      out.write(urls[ind]+'\n')
      n+=1

    return n

if __name__ == "__main__":
  mock_urls = get_urls_from_mock_server()
  child_urls, master_urls = filter_urls(mock_urls)
  tailor_urls = generate_tailor_urls(child_urls)
  test_url = tailor_host + tailor_urls[random.randint(0, len(tailor_urls)-1)]
  print(test_url)
  test_resp = requests.get(test_url, timeout=5)
  if test_resp.status_code == 200:
    print(test_resp.text)
  else:
    print(test_resp.status_code)
    print(test_resp.text)

  out_fname = "layers-mock.csv"
  generate_final_csv(tailor_urls, out_fname)


