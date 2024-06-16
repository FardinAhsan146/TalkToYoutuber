import scrapetube

videos = scrapetube.get_channel("UC9-y-6csu5WGm29I7JiwpnA")

for video in videos:
    print(video['videoId'])