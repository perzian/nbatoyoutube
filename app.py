import yt
import resourcedownloader
from bs4 import BeautifulSoup
import argparse
import requests
import untangle


def execute():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--display", action='store_true')
    parser.add_argument("video_position", nargs='*', help="Position of video on page", type=int)
    args = parser.parse_args()
    soup = BeautifulSoup(requests.get("https://www.nba.com/raptors/video").text, "html.parser")
    all_a_video_tags = soup.select(".video-thumbnail-image a[data-videoid]")

    if args.display:
        print ("is not none")
        i = 1
        for a in all_a_video_tags:
            print(str(i) + ": " + a['aria-label'])
            i = i+1

    a_tags = []
    for i in args.video_position:
        a_tags.append(all_a_video_tags[i - 1])

    bit_rates = ["1280x720_3072", "960x540_2104", "68x432_1404"]
    video_list = []
    for a in a_tags:
        video_id = a["data-videoid"]
        url = 'https://www.nba.com//raptors/video/' + video_id + '.xml'
        obj = untangle.parse(requests.get(url).text)
        name = obj.video.headline.cdata
        files = obj.video.files.file
        for f in files:
            found = False
            for b in bit_rates:
                if f.get_attribute("bitrate") == b:
                    video_url = f.cdata
                    found = True
                    break
            if found:
                video_list.append((name, video_url))
                break

    print("Found " + str(len(video_list)))
    for v in video_list:
        print("Downloading " + v[0] + ": " + v[1])
        downloaded_file = resourcedownloader.download_file(v[1])
        print("Finished downloading, now uploading")
        yt.execute_youtube_upload(downloaded_file, v[0], v[0], 17)
        print("Finished uploading")


if __name__ == '__main__':
    execute()
