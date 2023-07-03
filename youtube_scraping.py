import pandas as pd 
import asyncio
from typing import List,Dict

df = pd.read_csv("youtube_urls.csv")
# df = pd.DataFrame(columns=["id","type","title","publishedTime","duration","viewCount","url"])

from youtubesearchpython.__future__ import VideosSearch
keywords = [
    "الحمدلله",
    "سبحان الله ",
    "صل الله علي محمد ",
    "الله أكبر",
    "لا حول ولا قوة الا بالله ",
    "فضل الاذكار",
    "قول سبحان الله والحمد لله",
    "الصلاة علي النبي ",
]

async def search_videos(df, keyword):     videosSearch = VideosSearch(keyword, limit=50, region="EG")
    videosResult = await videosSearch.next()
    for video in videosResult["result"]:
        video_data = {
            "id": video["id"],
            "type": video["type"],
            "title": video["title"],
            "publishedTime": video["publishedTime"],
            "duration": video["duration"],
            "viewCount": video["viewCount"],
            "url":video["link"],
        }
        df = pd.concat([df, pd.DataFrame(video_data)], ignore_index=True)
    return df


async def search_all_videos(df):
    for keyword in keywords:
        df = await search_videos(df, keyword)
    df.to_csv("youtube_urls.csv", index=False)
    return df


if __name__ == "__main__":
    asyncio.run(search_all_videos(df))