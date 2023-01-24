import threading, colorama, re, os, base64, sys, time
from requests.packages import urllib3 as ulib
from requests import head as HEAD
from colorama import Fore

# 多线程URI格式&状态检查工具  v1.2
# 版权所有: 林乐天(LLT)
# 个人官网: https://birdy02.com
# 个人博客: https://www.birdy02.com

help, banner = str(base64.b64decode("VXNhZ2U6IFVSSVN0YXR1cy5leGUgW29wdGlvbnNdCgpPcHRpb25zOgoKICAgIHMgLyAtcyAvIHNldHRpbmcgICAgc2V0IGZpbGUgYW5kIHNjYW4gdGhyZWFkICjorr7nva7mlofku7blkoznur/nqIspCiAgICBoIC8gLWggLyBoZWxwICAgICAgIGZvciBoZWxwICjluK7liqkpCiAgICBkIC8gLWQgLyBkZWZhdWx0ICAgIFVzZSB0aGUgZGVmYXVsdCBvcHRpb24gKOS9v+eUqOm7mOiupOmFjee9rikKICAgIGQgLyAtZCAvIGRlZmF1bHQgIG51bSAgICB1c2UgZGVmYXVsdCBmaWxlIGFuZCBzZXQgc2NhbiB0aHJlYWQgKOS9v+eUqOm7mOiupOaWh+S7tuW5tuiuvue9rue6v+eoi+aVsCkKCi5cVVJJU3RhdHVzLmV4ZQoKV2VsQ29tZSB0byBCaXJkeSdzIEJsb2co5p6X5LmQ5aSp55qE5Liq5Lq65Y2a5a6iKQpodHRwczovL3d3dy5iaXJkeTAyLmNvbQ==").decode("utf-8")), str(base64.b64decode("IwojICAgICAgICAgICAgICAgX18gICAgICAgICAgICAgIF9fICAgICAgICAgICBfX19fX19fX19fX18gCiMgICAgICAgICAgICAgIHwgIHwgICAgICAgICAgICB8ICB8ICAgICAgICAgfF9fX18gICAgX19fX3wKIyAgICAgICAgICAgICAgfCAgfCAgICAgICAgICAgIHwgIHwgICAgICAgICAgICAgIHwgIHwKIyAgICAgICAgICAgICAgfCAgfCAgICAgICAgICAgIHwgIHwgICAgICAgICAgICAgIHwgIHwKIyAgICAgICAgICAgICAgfCAgfF9fX19fXyAgICAgIHwgIHxfX19fX18gICAgICAgIHwgIHwKIyAgICAgICAgICAgICAgfF9fX19fX19fX3wgICAgIHxfX19fX19fX198ICAgICAgIHxfX3wKIwojCiMKIyAgICAgICAgICAgICAgICDlpJrnur/nqIvmibnph49VUknmoLzlvI8m54q25oCB5qOA5p+l5bel5YW3ICB2IDEuMgojCiMgICAgICAgICAgICAgICAg54mI5p2D5omA5pyJ77ya5p6X5LmQ5aSpIExMVAojCiMKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKClsqXSAg5L+u5q2jVVJM5ZCI5qC85oCn77yM5L+u5q2jWyJodHA6Ly94eC54eCIsImh0dHA6L3h4Lnh4IiwiaHRwL3h4Lnh4IiwuLi4uLl0KWypdICDmo4DmtYtVUkznmoTlj6/orr/pl67mgKcKWypdICBVc2UgaCAvIC1oIC8gaGVscCAgZm9yIGhlbHAKClsrXSDohJrmnKzov5DooYzov4fnqIvkuK3or7fli7/lvLrooYzpgIDlh7oKCldlbENvbWUgdG8gQmlyZHkncyBCbG9nKOael+S5kOWkqeeahOS4quS6uuWNmuWuoikKaHR0cHM6Ly93d3cuYmlyZHkwMi5jb20=").decode("utf-8")) + "\n"

class URIstatus:
    def __init__(self, file, xc):
        self.yes, self.no = 0, 0
        if not os.path.exists('output'): os.mkdir('output')
        self.URIstatusX(self.urIp(file, xc))

    def URIstatusX(self, URIS):
        thread_list = [threading.Thread(target=self.URIstatus, args=(URIS[i],)) for i in range(len(URIS))]
        for t in thread_list: t.start()
        for t in thread_list: t.join()

    def URIstatus(self, Ulist):
        global num, time
        for url in Ulist:
            status, Temp_url = self.URIStatue("https://" + url), ("https://" + url)
            if status == 999:
                status, Temp_url = self.URIStatue("http://" + url), ("http://" + url)
                self.write_file(Temp_url, f"{result}") if status != 999 else self.write_file(url, f"{fail}")
            else: self.write_file(Temp_url, f"{result}")
            print(Fore.YELLOW + f'\r  Running: 第 {num}/{len(self.ucount)} 条. 成功{self.yes}条. 失败{self.no}条', end='')
            num = num + 1

    def URIStatue(self, url):
        try:
            ulib.disable_warnings()
            return int(HEAD(url=url, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39', 'HEAD': f"/{url}", 'Host': url.split('://')[1], 'Referer': f'{url}'}).status_code)
        except: return 999

    def write_file(self, data, file):
        if "_Result.txt" in file: self.yes = self.yes + 1
        if "_Fail.txt" in file: self.no = self.no + 1
        File = open(f"./output/{str(file)}", 'a')
        File.seek(0), File.write(f"{data}\n"), File.close()

    def urIp(self, ufile, xc):
        self.ucount = ulist = self.CountURI(ufile)
        print(Fore.WHITE + "\n[+]\tURI:   " + str(len(ulist)) + "个\n", end='')
        ulist, ulists, SURI = self.urlProtocol(ulist), [], [[] for i in range(xc)]
        for i, e in enumerate(ulist): SURI[i % xc].append(e)
        for i in SURI: ulists.append(i)
        return ulists

    def urlProtocol(self, sUlist):
        print(Fore.YELLOW + "\n\n数据整理中，即将开始...", end='')
        NURI = []
        for url in sUlist:
            protocol = ['https://', 'http://', 'https:/', 'http:/', 'htps://', 'htp://', 'htps:/', 'htp:/', 'https:', 'http:', 'htps:', 'htp:', 'https//', 'https/', 'http//', 'http/', 'htps//', 'htps/', 'htp//', 'htp/', 'https', 'http', 'htps', 'htp']
            for i in range(len(protocol)):
                nurI = re.sub(protocol[i], '', url, re.I)
                if url != nurI: break
            NURI.append(nurI)
        return NURI

    def CountURI(self, ufile):  # 统计URL
        try:
            with open(ufile, 'r', encoding='utf-8') as U: ulist = [i for i in list(set(U.read().split('\n'))) if i != '']
        except: ulist = []
        return ulist

    def __del__(self, ): print(Fore.GREEN + "\n\n\n\n\t\t>>> 成功 " + str(len(self.CountURI("./output/" + result))) + " 个，请在./output目录" + result + "文件中查看\n\n" + Fore.GREEN + "\t\t>>> 失败 " + str(len(self.CountURI("./output/" + fail))) + " 个，请在./output目录" + fail + "文件中查看\n\n\n", end=''),print(Fore.WHITE+"exit")

class InitStatue:
    def getArgv(self):
        if len(sys.argv) >2: thread = int(sys.argv[2]) if int(sys.argv[2]) >0 else 4
        try: return ['url.txt', thread if len(sys.argv) >2 else 4] if sys.argv[1] in ['-d', 'default', 'd'] else self.getSet() if sys.argv[1] in ['-s', 's', 'setting'] else sys.exit()
        except:sys.exit(help)

    def getSet(self, dft=['url.txt', 4], inputs=[]):
        inputs.append(input("请选择Url文件:")), inputs.append(input("线程(1-40):"))
        try: return inputs if inputs[0] != '' and inputs[1] != '' else dft
        except: return dft

    def IsFile(self, arg):
        try: return [arg[0] if open(arg[0]) else sys.exit(), int(arg[1])]
        except: sys.exit(f"\n\n\r文件{arg[0]}丢失\t或{arg[1]}非数字")

if __name__ == "__main__":
    All_list, result, fail, num, file, xc = [], f"{int(time.time())}_Result.txt", f"{int(time.time())}_Fail.txt", 1, None, None
    try:
        ini = InitStatue().IsFile(InitStatue().getArgv())
        os.system('cls'), colorama.init(), print(Fore.BLUE + banner, end=''), print(Fore.GREEN + f"\n{str(ini)}"), URIstatus(ini[0], ini[1] if int(ini[1]) < 41 and int(ini[1]) > 0 else 4), sys.exit(input(Fore.GREEN + '\n回车结束：'))
    except Exception as e: sys.exit(f"{str(e)}")