from urllib3 import HTTPResponse


def close_conn_in_background(response: HTTPResponse | None):
    if response:
        response.close()
        response.release_conn()
