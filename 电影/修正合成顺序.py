import os
from concurrent.futures import ThreadPoolExecutor
import queue


class Video:
    """视频ts下载"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
    }

    def __init__(self):
        self.queue = queue.Queue()

    def get_ts(self):
        url = 'https://www.ldxmcloud.com/20230224/McubV3Kc/1100kb/hls/index.m3u8'
        reslut = requests.get(url=url, headers=self.headers)
        reslut.encoding = 'utf-8'
        res = re.findall('(https:.*jpg)', reslut.text)
        return res

    def get_video(self):
        while not self.queue.empty():
            value = self.queue.get()
            vodie = requests.get(url=value, headers=self.headers)
            with open('report/'+ value[-12:-4] + '.ts', 'ab+') as w:
                w.write(vodie.content)
                print("加载成功~", value)
            self.queue.task_done()

    def sava_Video(self):
        """合成代码"""
        path = 'report/'
        files = os.listdir(path)
        print(len(files),[_[:-3] for _ in files])
        with open('res.txt','r',encoding='utf-8') as r:
            values = r.read()
        for file_path in eval(values):
            with open(path+file_path[-12:-4]+'.ts', 'rb') as f1:
                with open(path + "电影.mp4", 'ab') as f2:
                            f2.write(f1.read())
                    
    def run(self):
        ts = self.get_ts()
        for value in ts:
            self.queue.put(value)
        with ThreadPoolExecutor(max_workers=100) as pool:
            for i in range(100):
                pool.submit(self.get_video)
            # pool.map(self.get_video,range(100))
        pool.shutdown()
        self.queue.join()
        self.sava_Video()

if __name__ == '__main__':
    video = Video()
    video.run()
