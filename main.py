from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from time import time

app = Flask(__name__)

@app.route("/api/fluxus", methods=["GET"])
def fluxus():
    json_data = {"key": "", "made by Faisal": "Thank you"}

    hwid = request.args.get("hwid")
    if hwid:
        try:
            start_time = time()
            print("HWID: " + hwid)

            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": "PHPSESSID=5t4uo40cp95kr6ns5bon5rots3",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows"
            }

            endpoint = [
                {"url": "https://flux.li/android/external/start.php?HWID=" + hwid, "referer": "https://linkvertise.com/"},
                {"url": "https://flux.li/android/external/check1.php", "referer": "https://linkvertise.com/"},
                {"url": "https://flux.li/android/external/main.php", "referer": "https://linkvertise.com/"}
            ]

            for i in range(len(endpoint)):
                headers["referer"] = endpoint[i]["referer"]
                r = requests.get(endpoint[i]["url"], headers=headers)
                if r.status_code == 200 and endpoint[i]["url"] == endpoint[2]["url"]:
                    soup = BeautifulSoup(r.text, "html.parser")
                    key = soup.find_all("code")
                    if len(key) > 0:
                        if key:
                            json_data["key"] = key[0].text.strip()
                        else:
                            print("Failed to bypass")
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": str(e)}), 500

    return jsonify(json_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
