import requests
from flask import Flask, request, Response

app = Flask(__name__)

TARGET_URL = "http://213.142.135.46:9999"

@app.before_request
def proxy():
    try:
        # Buoin yung full URL kasama query params
        url = f"{TARGET_URL}{request.full_path}"
        if url.endswith("?"):
            url = url[:-1]  # alisin kung may extra '?'

        # Forward request
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        # Buoin response
        excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
        headers = [(name, value) for name, value in resp.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
