import requests
import re
import json

download_quality: str = '720p'
with open('urls.txt') as urls_file:
    line_number = 1
    url: str = urls_file.readline().rstrip()
    while url:
        player_url: str or None = None
        if  re.fullmatch(r'https://player\.vimeo\.com/video/\d+/?', url):
            player_url: str = url
        elif re.fullmatch(r'https://vimeo\.com/\d+/?', url):
            match: re.Match = re.search(r'\d+', url) 
            if match:
                video_id: str = match[0]
                player_url: str = f'https://player.vimeo.com/video/{video_id}'
        if player_url is None:
            print('Error: Incorrect video url')
            line_number += 1
            url: str = urls_file.readline().rstrip()
            continue
        response = requests.get(player_url)
        video_title: str = re.search(r'<title>.+from', response.text).group()[7:-5]
        video_config_str: str = re.search(r'var config = \{.+\}; if \(\!config.request\)', response.text).group()[13:-22]
        video_config: dict = json.loads(video_config_str)
        video_url = None
        for video_file in video_config['request']['files']['progressive']:
            if video_file['quality'] == download_quality:
                video_url = video_file['url']
                video_format = video_file['mime'].split('/')[1]
        if video_url is not None:
            with open(f'{video_title}.{video_format}', 'wb') as output_file:
                video = requests.get(video_url).content
                output_file.write(video)     
        else:
            print(f'Video in line {line_number} with quality {download_quality} not found.')
        line_number += 1
        url: str = urls_file.readline().rstrip()
print('Downloading is complete')