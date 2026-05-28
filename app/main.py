from class_activity import ActivityDS, MonitoringWindow
import asyncio
import sys

async def main():
    if len(sys.argv) > 1:
        id_app = sys.argv[1]
        key_api = sys.argv[2]
    else:
        id_app = int(input("Введите id приложения discord: "))
        key_api = input("Введите ключ api от freeimage.host: ")

    activity = ActivityDS(id_app, key_api)
    monitoring = MonitoringWindow()

    await activity.connect()

    async def call(hwnd):
        await activity.activity_process(hwnd)

    await monitoring.monitoring_window(call)

if __name__ == "__main__":
    asyncio.run(main())