import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
from utils import create_Or_reset_dir
from tqdm import tqdm


def remove_nullp(ps):
    nps = []
    for p in ps:
        text = p.get_text()
        if text != "" and "Chapter" not in text:
            nps.append(text)
    return nps


def get_numandhead(text):
    text = text.replace("Chapter","")
    text = text.replace("-","")
    # text = text.strip()
    rawlist = text.split(" ")
    head = []
    for raw in rawlist:
        if not str.isdigit(raw):
            head.append(raw)
    return "# " + " ".join(head).strip()


def gettext(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.select('.section-content > div:nth-child(4) > div:nth-child(1)')[0]
    # regex1 = re.compile('Chapter \d.*?Chapter', re.S)
    # text = regex1.findall(text)
    h = text.select('h4')[0].get_text()
    head = get_numandhead(h)
    ps = remove_nullp(text.select('p'))
    ps.insert(0, head)
    return ps

class mytest:

    def __init__(self):
        pass

    def main(self, offset):
        # offset = offset[0]
        # print(offset)
        # print(type(offset))
        prefix = 'https://www.wuxiaworld.com/novel/rmji/rmji-chapter-'
        response = requests.get(prefix + offset)
        html = response.text
        text_list = gettext(html)
        with open("test/" + offset +".md", 'w', encoding='utf-8') as file:
            file.write("\n\n".join(text_list))
        # global Chapterlist
        # global nametuple
        # self.Chapterlist.append(self.nametuple(head,text_list))
        # print(offset, text)
        # print(offset,"完毕")

    def test(offset):
        print(str(offset))

    def run(self):
        i=1
        max_i = 1000
        # starttime = time.time()
        # while i <= max_i:
        #     self.main(i)
        #     i+=1
        # print(time.time()-starttime)
        starttime = time.time()
        pool = Pool(4)
        for _ in tqdm(pool.imap_unordered(self.main,
                          [str(i+1) for i in range(max_i)]),
                      total=max_i):
            pass
        pool.terminate()
        # pool.map(self.main, [str(i+1) for i in range(max_i)])
        print(time.time()-starttime)

if __name__ == '__main__':
    dir = "test/"
    create_Or_reset_dir(dir)
    test1 = mytest()
    test1.run()
    from tqdm import trange

    # for i in trange(100):
    #     # do something
    #     pass