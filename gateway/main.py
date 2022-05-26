import json
from nameko.web.handlers import http
from werkzeug import Request, Response
from werkzeug.datastructures import Headers
from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError, Forbidden
from nameko.rpc import RpcProxy
import redis

class GatewayService:
    name = "gateway_service"

    user_rpc = RpcProxy("user_service")
    calc_rpc = RpcProxy("calculation_service")

    redis_client: redis.Redis 

    def __init__(self) -> None:
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)

    @http("POST", "/login")
    def login(self, request: Request) -> Response:
        data = request.json()
        result = self.user_rpc.login(data["username"], data["password"])
        if result is None:
            raise InternalServerError()
        
        if result['error'] != 0:
            raise BadRequest(result['message'])

        return Response(
            json.dump(
                {
                    "result": 1,
                    "_token": result['token'],
                }
            ),
            status=200,
        )

    @http("POST", "/register")
    def register(self, request: Request) -> Response:
        data = request.json()
        if data["username"] is None or data["password"] is None:
            raise BadRequest("Invalid request body")

        result = self.user_rpc.register(data["username"], data["password"])
        if result is None:
            raise InternalServerError()

        if result["error"] != 0:
            raise BadRequest(result["message"])

        return Response(
            json.dump(
                {
                    "_token": result["token"],
                }
            ),
            status=200,
        )

    @http("POST", "/permutation")
    def permutation(self, request: Request) -> Response:
        token = self.__validate_auth(request.headers)
        if not token:
            raise Forbidden("Need login to access")

        username = self.__validate_session(token)
        if username is None:
            raise Forbidden("Invalid session")

        data = request.json()
        if data['value'] is None:
            raise BadRequest("No value in request body")

        result = self.calc_rpc.permutation(data['value'])
        if result['error'] != 0:
            raise BadRequest(f"Error {result['message']}")

        return Response(json.dump({ 'result': result['result'] }))

    @http("POST", "/combination")
    def combination(self, request: Request) -> Response:
        token = self.__validate_auth(request.headers)
        if not token:
            raise Forbidden("Need login to access")

        username = self.__validate_session(token)
        if username is None:
            raise Forbidden("Invalid session")

        data = request.json()
        if data['value'] is None:
            raise BadRequest("No value in request body")

        result = self.calc_rpc.combination(data['value'])
        if result['error'] != 0:
            raise BadRequest(f"Error {result['message']}")

        return Response(json.dump({ 'result': result['result'] }))

    def __validate_auth(self, headers: Headers) -> str|False:
        auth = headers.get('Authorization', "")
        if auth == "":
            return False
        
        auth_split = auth.split(' ', 1)
        auth_type = auth_split[0]
        auth_token = auth_split[1]

        if auth_type.lower() == "bearer":
            return auth_token
        return False

    def __validate_session(self, token: str) -> str|False:
        username = self.redis_client.get(token)
        return username if username is not None else False
            