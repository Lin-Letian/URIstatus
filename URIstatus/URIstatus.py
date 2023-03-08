import threading, re, os, sys, datetime, csv
from requests import head, get, post
from bs4 import BeautifulSoup as bs
from colorama import Fore, init

# 个人官网: https://birdy02.com
# 个人博客: https://www.birdy02.com

banner = '''
>>  多线程URI格式&状态修正_检查工具
>>  版权所有: 林乐天(LLT)

[*]  修正URL合格性，修正["htp://xx.xx","http:/xx.xx","htp/xx.xx",.....]
[*]  检测URL的可访问性
[!]  脚本运行过程中请勿强行退出

WelCome to Birdy's Blog (林乐天的个人博客)
https://www.birdy02.com
'''


class URIstatus:
    def __init__(self, conf):
        self.Ok = self.Err = self.c200 = [['状态', '请求方法', 'URL', '标题']]  # 可访问、访问失败、状态码200
        print(Fore.YELLOW + f'[-] 配置情况:\n[+] URL输入文件: {conf[0]}\n[+] 线程数: {conf[1]}')
        self.dirName = self.checkinit(conf[0])  # 获取输出结果
        Threadlist = self.getUriList(conf[0], conf[1])  # 获取url列表并根据线程数进行分配列表
        print('[*] 初始化完成，多线程启动\n')
        print(Fore.WHITE + '|  Code | Method |\t\t\t\tURL\t\t\t\t|\tTitle')
        print(Fore.WHITE + '———————————————————————————————————————————————————————————————————')
        for i in Threadlist: i.start()
        for i in Threadlist: i.join()
        print(Fore.WHITE + '———————————————————————————————————————————————————————————————————\n')
        self.write_csv()

    def checkinit(self, UriFile):  # 初始化检查
        try:
            open(UriFile)  # 判断 url.txt 是否存在
        except:
            sys.exit(Fore.RED + f"[-] 文件{UriFile}丢失")
        if not os.path.exists('output'): os.mkdir('output')  # 确保输出路径不存在无异常
        return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    def getUriList(self, ufile, xc):  # 对URI的处理
        with open(ufile) as U:  # 读取URL到列表中
            ulist = [i for i in list(set(U.read().split('\n'))) if i != '']
        print(Fore.GREEN + f'[*] 开始url读取::获取{len(ulist)}条URI(第一次去重)')
        protocol = ['https://', 'http://', 'https:/', 'http:/', 'htps://', 'htp://', 'htps:/',  # 协议库
                    'htp:/', 'https:', 'http:', 'htps:', 'htp:', 'https//', 'https/', 'http//',  # 不可改变列表顺序
                    'http/', 'htps//', 'htps/', 'htp//', 'htp/', 'https', 'http', 'htps', 'htp']
        newUlist, nuri = [], None  # 去协议之后的新列表
        print(Fore.GREEN + "[*] 开始url处理::去除(不规则)协议,去重")
        for url in ulist:  # 获取单个url
            for prot in protocol:  # 循环获取协议
                nuri = re.sub(prot, '', url, re.I)  # 正则匹配掉协议
                if url != nuri: break  # 当匹配到协议后停止循环
            newUlist.append(nuri)
        newUlist = list(set(newUlist))  # 通过set()二次去重
        print(Fore.GREEN + "[*] 开始分配线程::根据线程分配url组")
        SURI = [[] for N in range(xc)]  # 根据线程数分组
        [SURI[i % xc].append(e) for i, e in enumerate(newUlist)]  # 将总url根据线程平均分配
        return [threading.Thread(target=self.judge_status, args=(SURI[i],)) for i in range(xc)]  # 线程列表

    def judge_status(self, Ulist):
        for url in Ulist:
            new_url = f'https://{url}'
            res = self.get_statuecode(new_url)
            if res[0] != "000":
                print(Fore.WHITE + f"|  {res[0]}  |  {res[1]}  | \t{new_url}\t\t{res[-1]}")
                self.Ok.append(res)
            else:
                new_url = f'http://{url}'
                res = self.get_statuecode(new_url)
                if res[0] != "000":
                    print(Fore.WHITE + f"|  {res[0]}  |  {res[1]}  | \t{new_url}\t\t{res[-1]}")
                    self.Ok.append(res)
                else:
                    print(Fore.RED + f"|  ERR  |  NONE  | \t目标不可达::{url}")
                    self.Err.append(url)

    def get_statuecode(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
            'Host': url.split('://')[-1], 'Referer': url,
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"'
        }
        try:
            response = get(url=url, timeout=10, headers=headers)
            return [response.status_code, "GET ", url,
                    bs(response.content, 'html.parser').find('title').text.replace('\n', '').replace('\r', '')]
        except:
            try:
                response = post(url=url, timeout=10, headers=headers)
                return [response.status_code, "POST", url,
                        bs(response.content, 'html.parser').find('title').text.replace('\n', '').replace('\r', '')]
            except:
                try:
                    response = head(url=url, timeout=10, headers=headers)
                    return [response.status_code, "HEAD", url, 'HEAD方法无法获取标题']
                except:
                    return ["000", None, '']

    def write_csv(self, isc200=False):
        print(Fore.GREEN + "[*] 正在保存结果")
        dir_path = f"output\\{self.dirName}"
        if os.path.exists(dir_path):  # 判断目录是否已经存在
            input(f"检测到 {dir_path} 目录已经存在,将删除该目录并重新创建，请确认：")
            try:  # 避免人工删除目录导致的报错
                os.rmdir(dir_path)  # 当目录存在时候
            except:
                pass
        if not os.path.exists(dir_path): os.mkdir(dir_path)  # 判断目录不存在时候进行创建
        if not isc200:
            if len(self.Ok) > 1:
                with open(f'{dir_path}\\Result_Ok.csv', 'w', newline="", encoding="utf-8") as csvfile:
                    spamwriter = csv.writer(csvfile, dialect='excel')
                    for ok in self.Ok: spamwriter.writerow(ok)
            if len(self.Err) > 1:
                with open(f'{dir_path}\\Fail.csv', 'w', newline="", encoding="utf-8") as csvfile:
                    spamwriter = csv.writer(csvfile, dialect='excel')
                    for fail in self.Err: spamwriter.writerow(fail)
        if isc200:
            with open(f'{dir_path}\\Code_200.csv', 'w', newline="", encoding="utf-8") as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                for c2 in self.c200: spamwriter.writerow(c2)
        print(Fore.YELLOW + f"[-] 访问成功 {len(self.Ok)} 个")
        print(Fore.YELLOW + f"[-] 访问失败 {len(self.Err)} 个")
        print(Fore.YELLOW + f'[-] 输出文件保存至目录:: {os.getcwd()}\\{dir_path}')


if __name__ == "__main__":
    init()  # colorama.init()
    print(Fore.BLUE + banner)
    xc = input('请输入线程,县城越高,数据准确度会降低\n请根据实际网络状况来设定,建议[4-10],最大20,默认4线程:')
    try:
        xc = int(xc)  # 将输入线程转换为int类型，失败则默认4线程
        xc = xc if xc <= 20 else 20
    except:
        xc = 4
    uri = URIstatus(['url.txt', xc])
    sys.exit(input("回车结束:"))
