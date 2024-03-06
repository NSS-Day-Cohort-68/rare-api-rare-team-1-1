import json
from json.decoder import JSONDecodeError
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user
from views import create_comment
from views import create_tag


class JSONServer(HandleRequests):
    def do_GET(self):
        pass

    def do_POST(self):
        url = self.parse_url(self.path)

        try:
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)
        except JSONDecodeError:
            return self.response(
                "Error -- No user information was provided.",
                status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
            )

        if url["requested_resource"] == "users":
            try:
                expected_user_keys = [
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "bio",
                    "password",
                    "profile_image_url",
                    "created_on",
                    "active",
                ]
                for key in expected_user_keys:
                    value = request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for first_name, last_name, username, and email.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            token = create_user(request_body)
            return self.response(token, status.HTTP_201_SUCCESS_CREATED.value)
        return self.response(
            "Unexpected error occurred", status.HTTP_500_SERVER_ERROR.value
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
            successfully_created = create_tag(request_body)
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
