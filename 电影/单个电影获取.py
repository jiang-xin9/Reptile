from tqdm import tqdm
import os

class Video:
    """视频ts下载"""
    def get_ts(self):
        url = 'https://www.ldxmcloud.com/20230224/McubV3Kc/1100kb/hls/index.m3u8'
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
        }
        reslut = requests.get(url=url,headers=headers)
        reslut.encoding='utf-8'
        # print(reslut.text)
        res = re.findall('(https:.*jpg)',reslut.text)
        for value in res:
            vodie = requests.get(url=value, headers=headers)
            with open('report/' + value[-12:-4] + '.ts','ab+') as w:
                w.write(vodie.content)
                print("加载成功~",value)

    def sava_Video(self):
        """合成代码"""
        path = 'report/'
        files = os.listdir(path)
        print(files)
        for file in tqdm(files, desc="正在转换视频格式："):
                if os.path.exists(path + file):
                    with open(path + file, 'rb') as f1:
                        with open(path + "电影.mp4", 'ab') as f2:
                            f2.write(f1.read())
                else:
                    print("失败")
    def run(self):
        self.get_ts()
        self.sava_Video()

if __name__ == '__main__':
    video = Video()
    video.run()