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
from views import create_post
from views import post_category
from views import create_posttag
from views import get_categories


class JSONServer(HandleRequests):

    def do_GET(self):
        http_404_message = {
            "HTTP 404": "ERROR - The requested resource is not available"
        }
        http_500_message = {"HTTP 500": "ERROR - Unexpected error occurred"}

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] == 0:
                response_body = get_all_user_posts(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_post(url["pk"])
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "categories":
            response_body = get_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "tags":
            response_body = get_and_sort_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "users":
            if "email" in url["query_params"]:
                requested_email = url["query_params"]["email"][0]
                user_token = login_user(requested_email)
                if "valid" in user_token:
                    return self.response(user_token, status.HTTP_200_SUCCESS.value)
                return self.response(
                    json.dumps(http_500_message),
                    status.HTTP_500_SERVER_ERROR.value,
                )

        else:
            return self.response(
                json.dumps(http_404_message),
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_POST(self):
        http_404_message = {
            "HTTP 404": "ERROR - The requested resource is not available"
        }
        http_500_message = {"HTTP 500": "ERROR - Unexpected error occurred"}

        url = self.parse_url(self.path)

        try:
            content_len = int(self.headers.get("content-length", 0))
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)
        except JSONDecodeError:
            http_message = {"HTTP 400": "ERROR - No request body was provided"}
            return self.response(
                json.dumps(http_message),
                status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
            )

        if url["requested_resource"] == "users":
            try:
                expected_user_keys = ["first_name", "last_name", "username", "email"]
                for key in expected_user_keys:
                    value = request_body[key]
            except KeyError:
                http_message = {
                    "HTTP 400": "ERROR - Incomplete User information. Please provide values for first_name, last_name, username, and email."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            token = create_user(request_body)
            if json.loads(token)["token"] > 0:
                return self.response(token, status.HTTP_201_SUCCESS_CREATED.value)
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "comments":
            try:
                expected_comment_keys = ["post_id", "author_id", "content"]
                for key in expected_comment_keys:
                    value = request_body[key]
            except KeyError:
                http_message = {
                    "HTTP 400": "ERROR - Incomplete Comment information. Please provide values for post_id, author_id, and content."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_comment(request_body)
            if successfully_created:
                http_message = {"HTTP 201": "SUCCESS - new Comment created"}
                return self.response(
                    json.dumps(http_message), status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "categories":
            try:
                expected_category_keys = ["label"]
                for key in expected_category_keys:
                    value = request_body[key]
            except KeyError:
                http_message = {
                    "HTTP 400": "ERROR - Incomplete Category information. Please provide a value for label."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = post_category(request_body)
            if successfully_created:
                http_message = {"HTTP 201": "SUCCESS - new Category created."}
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_201_SUCCESS_CREATED.value,
                )
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "tags":
            try:
                expected_tag_keys = ["label"]
                for key in expected_tag_keys:
                    value = request_body[key]
            except KeyError:
                http_message = {
                    "HTTP 400": "ERROR - Incomplete Tag information. Please provide a value for label."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_tag(request_body)
            if successfully_created:
                http_message = {"HTTP 201": "SUCCESS - new Tag created."}
                return self.response(
                    json.dumps(http_message), status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
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
                http_message = {
                    "HTTP 400": "ERROR - Incomplete Post information. Please provide values for user_id, category_id, title, image_url, and content."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_post(request_body)
            if successfully_created:
                http_message = {"HTTP 201": "SUCCESS - new Post created."}
                return self.response(
                    json.dumps(http_message), status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
            )

        if url["requested_resource"] == "posttags":
            try:
                expected_posttag_keys = ["post_id", "tag_id"]
                for key in expected_posttag_keys:
                    value = request_body[key]
            except KeyError:
                http_message = {
                    "HTTP 400": "ERROR - Incomplete PostTag information. Please provide values for post_id and tag_id."
                }
                return self.response(
                    json.dumps(http_message),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            successfully_created = create_posttag(request_body)
            if successfully_created:
                http_message = {"HTTP 201": "SUCCESS - new PostTag created."}
                return self.response(
                    json.dumps(http_message), status.HTTP_201_SUCCESS_CREATED.value
                )
            return self.response(
                json.dumps(http_500_message), status.HTTP_500_SERVER_ERROR.value
            )

        else:
            return self.response(
                json.dumps(http_404_message),
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
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
