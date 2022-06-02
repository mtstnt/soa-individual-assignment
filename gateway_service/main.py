from http import HTTPStatus
import json
from nameko.web.handlers import http
from werkzeug import Request, Response
from werkzeug.datastructures import Headers
from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError, Forbidden
from nameko.rpc import RpcProxy
import session

SESSID_KEY = "CALC_SESSID"

class GatewayService:
    name = "gateway_service"

    user_rpc = RpcProxy("user_service")
    calc_rpc = RpcProxy("calculation_service")

    redis_client = session.RedisApi()

    @http("POST", "/login")
    def login(self, request: Request) -> Response:
        data = request.json
        result = self.user_rpc.login(data["username"], data["password"])
        print(result)
        if result is None:
            return Response("Internal server error", HTTPStatus.INTERNAL_SERVER_ERROR)

        if result["error"] != 0:
            return Response(result["message"], HTTPStatus.BAD_REQUEST)

        token = result["token"]
        self.redis_client.set(token, result["user_id"])
        response = Response(
            json.dumps(
                {
                    "message": result["message"],
                    "_token": result["token"],
                }
            ),
            status=HTTPStatus.OK,
        )

        response.set_cookie("CALC_SESSID", token)

        return response

    @http("POST", "/register")
    def register(self, request: Request) -> Response:
        data = request.json
        print(data)
        if data["username"] is None or data["password"] is None:
            return Response(
                "Invalid request body. Required: username (string), password (string)",
                HTTPStatus.BAD_REQUEST,
            )

        result = self.user_rpc.register(data["username"], data["password"])
        if result is None:
            return Response("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

        if result["error"] != 0:
            return Response(result["message"], HTTPStatus.BAD_REQUEST)

        token = result["token"]
        self.redis_client.set(token, result["user_id"])
        response = Response(
            json.dumps(
                {
                    "message": result["message"],
                    "_token": result["token"],
                }
            ),
            status=HTTPStatus.OK,
        )

        response.set_cookie(SESSID_KEY, token)

        return response

    @http("POST", "/permutation")
    def permutation(self, request: Request) -> Response:
        session_data = self._validate_session(request.cookies)
        if session_data is None:
            return Response("Invalid session", HTTPStatus.FORBIDDEN)

        data = request.json
        if data["value"] is None:
            return Response(
                "Invalid request body. Required: value (list)", HTTPStatus.BAD_REQUEST
            )

        result = self.calc_rpc.permutation(data["value"])
        if result["error"] != 0:
            return Response(result["message"], HTTPStatus.BAD_REQUEST)

        return Response(
            json.dumps(
                {"user_id": session_data.decode(), "result": result["permutations"]}
            )
        )

    @http("POST", "/combination")
    def combination(self, request: Request) -> Response:
        session_data = self._validate_session(request.cookies)
        if session_data is None:
            return Response("Invalid session", HTTPStatus.FORBIDDEN)

        data = request.json
        if data["value"] is None:
            return Response(
                "Invalid request body. Required: value (list)", HTTPStatus.BAD_REQUEST
            )

        result = self.calc_rpc.combination(data["value"])
        if result["error"] != 0:
            return Response(result["message"], HTTPStatus.BAD_REQUEST)

        return Response(
            json.dumps(
                {"user_id": session_data.decode(), "result": result["combinations"]}
            )
        )

    def _validate_session(self, cookies: dict) -> any:
        token = cookies.get(SESSID_KEY)
        print("Token:", token)
        if token == "" or token is None:
            return None

        session_data = self.redis_client.get(token)
        return session_data
