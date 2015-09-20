import requests
import sys
import re

def download(url):
    video = requests.get(url, stream=True)
    with open(re.search(r'/([^/]+)$', url).group(1), 'wb') as file:
        for part in video.iter_content(chunk_size = 10485760):
            file.write(part)
            file.flush()
    print('The video is downloaded under the name "' + re.search(r'/([^/]+)$', url).group(1) + '"')
    
def main():
    if sys.argv[1].lower() == 'download':
        url = sys.argv[2]
    else:
        url = sys.argv[1]
    video_id = re.search(r'([0-9]+)$', url).group(1)
    html = requests.get('https://web.archive.org/web/9/http://blip.tv/rss/flash/' + video_id).text
    if '<p>Wayback Machine doesn&apos;t have that page archived.</p>' or '"stylesheet"' in html:
        print('This video has not been saved, has not been uploaded yet or the original version of this video was not available from blip.')
    else:
        source_video = re.search(r'"([^"]+)" blip:role=".ource"', html).group(1)
        if sys.argv[1].lower() == 'download':
            download("https://web.archive.org/web/9im_/" + source_video)
        else:
            print("The url to your video: " + requests.get("https://web.archive.org/web/9/" + source_video).url)

if __name__ == '__main__':
    try:
        main()
    except:
        print('Please provide one or two arguments, for example:\n - "python blip.tv.py 391877" to get the url to a video.\n - "python blip.tv.py http://blip.tv/stevegarfield/vlog-soup-survivor-behind-the-scenes-with-jeff-probst-391877" to get the url to a video.\n - "python blip.tv.py download 391877" to download a video.\n - "python blip.tv.py download http://blip.tv/stevegarfield/vlog-soup-survivor-behind-the-scenes-with-jeff-probst-391877" to download a video.')
