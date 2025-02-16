from aiohttp import ClientSession
from asyncio import create_task, new_event_loop, sleep
from copy import deepcopy
from os import getenv
pat = {
    "content": "@everyone 有課拉"
}

data = {
    'Semester': '1132',
    'CourseNo': '',
    'CourseName': '',
    'CourseTeacher': '蘇金輝',
    'Dimension': '',
    'CourseNotes': '',
    'ForeignLanguage': 0,
    'OnlyGeneral': 0,
    'OnleyNTUST': 0,
    'OnlyMaster': 0,
    'OnlyUnderGraduate': 0,
    'OnlyNode': 0,
    'Language': 'zh'
}
class Bot:
    def __init__(self, token):
        self.token = token
        self.session:ClientSession = None
        self.loop = new_event_loop()

    async def serve(self):
        self.session = ClientSession()
        while True:
                create_task(self.check_course())
                await sleep(5)

    async def check_course(self):
        async with self.session.post("https://querycourse.ntust.edu.tw/querycourse/api/courses", data=data) as response:
            course_info = await response.json()
            course_info = [*filter(lambda x: x["ChooseStudent"] < int(x["Restrict2"]), course_info)]
            if course_info:
                await self.send_message([f"\n{i['CourseNo']}\n> {i["ChooseStudent"] - int(i["Restrict2"])}" for i in course_info])
            print(course_info)

    async def send_message(self, course_info: list[str]):
        msg = deepcopy(pat)
        for i in course_info:
            msg["content"] += i
        async with self.session.post(self.token, json=msg) as response:
            print(await response.text())

if __name__ == "__main__":
    bot = Bot(getenv("WEBHOOK"))
    bot.loop.run_until_complete(bot.serve())