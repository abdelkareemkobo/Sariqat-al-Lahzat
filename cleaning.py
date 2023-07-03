import pandas as pd 

df = pd.read_csv('youtube_urls.csv')
def parse_duration(duration_str):
    try:
        if isinstance(duration_str, str):
            parts = duration_str.split(':')
            if len(parts) == 2:
                hours, minutes, seconds = 0, int(parts[0]), int(parts[1])
            elif len(parts) == 3:
                hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            else:
                raise ValueError(f"Invalid duration format: {duration_str}")

            return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)
        else:
            return pd.NaT
    except ValueError:
        return pd.NaT

df['duration'] = df['duration'].apply(parse_duration)
filtered_df = df[df['duration'] < pd.Timedelta(minutes=15)]

filtered_df.head()
#Save this filtered file 
