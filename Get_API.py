# -*- encoding: utf-8 -*-
'''
@Project_name    :  OhMyChat_API
@ProjectDescription: ..........
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/8/8 9:25     zxy       1.0         None
'''
import datetime
import json
import time
import traceback
import uuid
from operator import index

import requests
from .AI_GUI import AIGUI
from uuid import uuid4


class GetAPI(AIGUI):
    def __init__(self, api_key="",is_need_GUI=False):
        self.api_key = api_key
        self.is_need_GUI = is_need_GUI
        if is_need_GUI:
            AIGUI.__init__(self)
        self.uuid__ = str(uuid.uuid4())

    def timeStamp_to_datetime(self, timeStamp):
        timeStamp = float(timeStamp)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_qiuyu_chat3_api(self,query="", rety_num=0):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "http://postfixmail.cn:3000",
            "Pragma": "no-cache",
            "Referer": "http://postfixmail.cn:3000/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        url = "http://postfixmail.cn:9988/api/send-message"
        data = {
            "message": query,
            "userId": self.uuid__,
            "model": "superAI-4"
        }
        data = json.dumps(data, separators=(',', ':'))
        try:
            if query:
                response = requests.post(url, headers=headers, data=data, stream=True, timeout=10)
                if response.status_code!=200:
                    return
                response = requests.get(f"http://postfixmail.cn:9988/api/bot-sse/{self.uuid__}",
                                        headers=headers, verify=False, stream=True, timeout=10)
                for index, line in enumerate(response.iter_lines()):
                    yield bytes.decode(line), index
        except:
            if rety_num < 3:
                for line_data, index in self.get_qiuyu_chat3_api(query, rety_num + 1):
                    yield line_data, index
        else:
            return None

    def get_chat_api(self, query="", rety_num=0):
        url = "https://cfwus02.opapi.win/v1/chat/completions"

        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
            "stream": True
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            "Authorization": "Bearer {api_key}".format(api_key=self.api_key),
            'Content-Type': 'application/json'
        }
        try:
            if query:
                if not rety_num:
                    raise
                response = requests.post(url, headers=headers, data=payload, stream=True,timeout=10)
                for index, line in enumerate(response.iter_lines()):
                    yield bytes.decode(line), index
        except:
            if rety_num < 3:
                for line_data, index in self.get_chat_api(query, rety_num + 1):
                    yield line_data, index
        else:
            return None

    def handler_qiuyu_chat3_api_result(self,line_data:str,index:int):
        if not line_data :
            return

        data = json.loads(str(line_data).split(":", 1)[-1])
        if not index:
            username = "User"
            start_str = f"{username}({str(datetime.datetime.now())[:19]}){'=' * 100}"
            is_wrap = True
            yield start_str, is_wrap
            self.header_lenth = len(start_str)

        if data.get("content") is None:
            equalSign_num = (self.header_lenth - 14) // 2

            is_wrap = True
            yield f"\n{'=' * equalSign_num} divisionLine {'=' * equalSign_num}", is_wrap
        else:
            yield data.get("content"),False

    def handler_api_result(self, line_data: str, index: int):
        if not line_data or line_data.endswith("[DONE]"):
            return
        data = json.loads(str(line_data).split(":", 1)[-1])
        if not index:
            release_time = self.timeStamp_to_datetime(data["created"])
            model = data["model"]
        else:
            release_time, model = "", ""
        for choice in data["choices"]:
            if not index:
                username = choice["delta"]["role"]
                start_str = f"{username}({model})({release_time}){'=' * 100}"
                is_wrap = True
                yield start_str,is_wrap
                self.header_lenth = len(start_str)
            if choice["finish_reason"]:
                equalSign_num = (self.header_lenth - 14) // 2

                is_wrap = True
                yield f"\n{'=' * equalSign_num} divisionLine {'=' * equalSign_num}",is_wrap
            else:
                content = choice["delta"]["content"]
                is_wrap = False
                yield content,is_wrap
    def run_cmd(self):

        while True:
            try:
                query = input("please input your question:")
                if not query:
                    continue
                elif query.lower() in ('q', 'quit', 'exit'):
                    while True:
                        query = input("Do you want to terminate (Y/N)?:")
                        if query.lower() == "y":
                            print("Welcome to use it next time")
                            return
                        elif query.lower() == 'n':
                            break
                        else:
                            print("Your input is illegal!")
                            continue
                    continue
                else:
                    print("Please be patient and wait for a response . . .")
                print(f"User({str(datetime.datetime.now())[:19]}):",query)

                # for line_data, index in self.get_chat_api(query):
                #     for text,is_warp in self.handler_api_result(line_data, index):
                #         if is_warp:
                #             print(text)
                #         else:
                #             print(text,end="")

                for line_data, index in self.get_qiuyu_chat3_api(query):
                    for text,is_warp in self.handler_qiuyu_chat3_api_result(line_data, index):
                        if is_warp:
                            if text is not None:
                                print(text)
                        else:
                            print(text,end="")

            except:
                traceback.print_exc()
                print("There is a problem with your API interface !!!")
                return
    def run(self):
        if self.is_need_GUI:
            self.run_gui()
        else:
            self.run_cmd()


