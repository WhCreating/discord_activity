import psutil, asyncio, time, win32gui, win32process
from pypresence import AioPresence
from pypresence.types import ActivityType
from PIL import Image
import base64
from io import BytesIO
from icoextract import IconExtractor, IconExtractorError
import requests

class MonitoringWindow:
    def __init__(self):
        self.hwnd_curr = None

    async def _get_window_curr(self):
        try :
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == self.hwnd_curr:
                return None
            
            self.hwnd_curr = hwnd
            return hwnd
        except :
            return None
    
    async def monitoring_window(self, callback):
        while True:
            hwnd = await self._get_window_curr()
            if hwnd:
                await callback(hwnd)



class ActivityDS:
    def __init__(self, id_app: int, key_img: str):
        self.RPC = AioPresence(id_app)
        self.key_img = key_img
        
    async def connect(self):
        await self.RPC.connect()

    async def activity_process(self, hwnd):

        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        
        icon_url = self.get_icon_process(process.exe())

        if process.name().replace(".exe", "") == "Discord":
            pass
        else :
            await self.RPC.update(name=process.name().replace(".exe", ""), large_image=icon_url)

        if process.name().replace(".exe", "") == "explorer":
            await self.RPC.clear()

        

            

    def get_icon_process(self, path) -> str:
        try:
            extractor = IconExtractor(path)

            extractor.export_icon('./m.ico', num=0)

            buffered = BytesIO()

            img = Image.open('m.ico')
            img.save(buffered, 'png')

            icon64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            res = requests.post(
                "https://freeimage.host/api/1/upload",
                data={
                    "key": self.key_img,
                    "action": "upload",
                    "source": icon64,
                    "format": "json"
                }
            )
            
            if res.status_code == 200:
                return res.json()["image"]["url"]
            else :
                return None

        except IconExtractorError:

            print("ошибка с извлечением иконки")
    
        
