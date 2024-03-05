import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user, post_category


class JSONServer(HandleRequests):
    def do_GET(self):
        pass

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "categories":
            test = post_category(request_body)
            return self.response(
                "endpoint is working",
                status.HTTP_200_SUCCESS.value,
            )

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
