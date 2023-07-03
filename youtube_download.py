#pip install pytube
import pandas as pd 
import pytube
downloaded_youtube = "downloaded_youtube"

filtered_df = pd.read_csv("youtube_urls.csv")
print(filtered_df.head())

for index,row in filtered_df.iterrows():
    url = row['url']
    filename =  downloaded_youtube + "/"+ row['id'] +".mp3"
    yt = pytube.YouTube(url)
    # print(yt,"\n",url,"\n")
    yt.streams.filter(only_audio=True).first().download(filename=filename)
