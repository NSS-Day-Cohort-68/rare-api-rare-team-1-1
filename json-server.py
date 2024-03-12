import json
from json.decoder import JSONDecodeError
from http.server import HTTPServer
from handler import HandleRequests, status

from views import (
    login_user,
    create_user,
    get_all_user_posts,
    get_post,
)
from views import create_comment
from views import create_tag, get_and_sort_tags
from views import create_post, get_all_posts
from views import post_category
from views import create_posttag
from views import get_categories


class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] == 0:
                if "user_id" in url["query_params"]:
                    logged_in_user_id = url["query_params"]["user_id"][0]
                    response_body = get_all_user_posts(logged_in_user_id)
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                response_body = get_all_posts()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            else:
                response_body = get_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            response_body = get_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            response_body = get_and_sort_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "users":
            if "email" in url["query_params"]:
                requested_email = url["query_params"]["email"][0]
                user_token = login_user(requested_email)
                if "valid" in user_token:
                    self.response(user_token, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "Unexpected error occurred",
                        status.HTTP_500_SERVER_ERROR.value,
                    )

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        url = self.parse_url(self.path)

        try:
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)
        except JSONDecodeError:
            return self.response(
                "Error -- No information was provided.",
                status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
            )

        if url["requested_resource"] == "users":
            try:
                expected_user_keys = ["first_name", "last_name", "username", "email"]
                for key in expected_user_keys:
                    value = request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for first_name, last_name, username, and email.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            token = create_user(request_body)
            if json.loads(token)["token"] > 0:
                return self.response(token, status.HTTP_201_SUCCESS_CREATED.value)
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "comments":
            try:
                expected_comment_keys = ["post_id", "author_id", "content"]
                for key in expected_comment_keys:
                    value = request_body[key]
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
            try:
                expected_category_keys = ["label"]
                for key in expected_category_keys:
                    value = request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for category label.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = post_category(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created",
                    status.HTTP_201_SUCCESS_CREATED.value,
                )
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "tags":
            try:
                expected_tag_keys = ["label"]
                for key in expected_tag_keys:
                    value = request_body[key]
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
            try:
                expected_post_keys = [
                    "user_id",
                    "category_id",
                    "title",
                    "image_url",
                    "content",
                ]
                for key in expected_post_keys:
                    value = request_body[key]
            except KeyError:
                return self.response(
                    "Incomplete user information. Please provide values for user_id, category_id, title, image_url, and content.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_post(request_body)
            if successfully_created:
                return self.response(
                    "Successfully created", status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                "An unexpected error occurred.", status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "posttags":
            try:
                expected_posttag_keys = ["post_id", "tag_id"]
                for key in expected_posttag_keys:
                    value = request_body[key]
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
