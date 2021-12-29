def searchterms(term, video_ids):
    return_dic = {}
    for video in video_ids:
        count = 0
        words = []
        times = []
        f = "static/transcripts/" + str(video) + '.srt'
        file = open(f, encoding="utf8")
        for i in file:
            count += 1
            if (count - 3) % 4 == 0:
                words.append(i.strip("\n"))
            if (count - 2) % 4 == 0:
                times.append(i[:8])
        file.close()

        dic = {}
        for key in words:
            for value in times:
                dic[key] = value
                times.remove(value)
                break

        new_times = []
        for word in words:
            if term in word:
                x = dic[word]
                x = x.replace(':', '')
                try:
                    hours = int(x[0:2]) * 60 * 60
                    minutes = int(x[2:4]) * 60
                    second = int(x[4:]) + minutes + hours
                    new_times.append(second)
                except:
                    pass
        return_dic[video] = new_times
    return return_dic
