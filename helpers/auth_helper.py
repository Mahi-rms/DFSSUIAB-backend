import jwt,uuid
from rest_framework.response import Response
from rest_framework import status
from backend.settings import JwtConstants
from helpers.api_helper import api_response, API_Messages, ResponseType
from app.models import TokenBlackList, User

def login_required():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                token = request.headers['Authorization'].split(" ")[-1]
                TokenBlackList.objects.get(token=token)
                return Response(api_response(ResponseType.FAILED, API_Messages.SESSION_EXPIRED), status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                try:
                    payload = jwt.decode(token,
                        JwtConstants.SECRET_KEY,
                        algorithms=JwtConstants.JWT_ALGORITHM,
                    )
                    try:
                        request.user = User.objects.get(id=uuid.UUID(payload["id"]))
                    except:
                        return Response(api_response(ResponseType.FAILED, API_Messages.LINK_BROKEN), status=status.HTTP_401_UNAUTHORIZED)
                    return func(request, *args, **kwargs)
                except Exception as exp:
                    return Response(api_response(ResponseType.FAILED, API_Messages.SESSION_EXPIRED), status=status.HTTP_401_UNAUTHORIZED)
        return wrapper
    return decorator