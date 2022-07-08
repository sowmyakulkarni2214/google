from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from search_web import *
import json
from isodate import parse_duration
import requests
from django.conf import settings
def search(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part':'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 10,
            'type':'video',
        }
        r = requests.get(search_url, params=params)
        results = r.json()['items']
        videoIds = []
        for result in results:
            videoIds.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={videoIds[0]}')

        params = {
        'part':'snippet, contentDetails, statistics',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'id': ','.join(videoIds),
        'maxResults': 10,
        }

        video_r = requests.get(video_url, params=params)
        results = video_r.json()['items']
        for result in results:
            if 'likeCount' in result['statistics']:
                likes = result['statistics']['likeCount']
            else:
                likes = 0
                continue

            title = result['snippet']['title'].replace('|',',').split(',')[0]

            if request.POST['search'].lower() not in result['snippet']['title'].lower():
                continue

            video_data = {
                    'title': title,
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'view_count': int(result['statistics']['viewCount']),
                     'likes': int(likes),
                    }
            videos.append(video_data)
            videos = sorted(videos, key=lambda item: item['likes'], reverse=True)
    context = {
        'videos': videos
            }
    # context = {'message':'hello how are a you'}
    # if request.POST:
    #     result = youtube_search(request.POST['term'])
    #     print(result)
    #     return render(request, 'searchengine/search.html', {'result':result})
    return render(request,'searchengine/search.html', context)

