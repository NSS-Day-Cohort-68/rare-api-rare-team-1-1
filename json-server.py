import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user
from views import create_comment


class JSONServer(HandleRequests):
    def do_GET(self):
        pass

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            test = create_user(request_body)
            return self.response(
                "endpoint is working",
                status.HTTP_200_SUCCESS.value,
            )

        if url["requested_resource"] == "comments":
            successfully_created = create_comment(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )

            return self.response(
                "Invalid data", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
            )

        if url["requested_resource"] == "tags":
            successfully_created = create_comment(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )

            return self.response(
                "Invalid data", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
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
