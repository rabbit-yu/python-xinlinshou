import pyttsx3

engine = pyttsx3.init()

# 设置语速
engine.setProperty("rate", 200)


def tips():
    engine.say("有新上架的了，赶紧抢购。")
    engine.runAndWait()


