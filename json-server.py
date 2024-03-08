import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user, get_all_user_posts
from views import create_comment
from views import create_tag
from views import create_post
from views import post_category


class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] == 0:
                response_body = get_all_user_posts(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            else:
                return self.response(
                    "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                )

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
            try:
                expected_comment_keys = ["post_id", "author_id", "content"]
                for key in expected_comment_keys:
                    request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for post_id, author_id, content.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_comment(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "categories":
            successfully_created = post_category(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created",
                    status.HTTP_201_SUCCESS_CREATED.value,
                )

            return self.response(
                "Invalid data", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
            )

        if url["requested_resource"] == "tags":
            try:
                expected_tag_keys = ["label"]
                for key in expected_tag_keys:
                    request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for tag label.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_tag(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "posts":
            successfully_created = create_post(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )

            return self.response(
                "Invalid data", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
            )

        if url["requested_resource"] == "posttags":
            try:
                expected_posttag_keys = ["post_id", "tag_id"]
                for key in expected_posttag_keys:
                    request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for post_id and tag_id.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_posttag(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
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
