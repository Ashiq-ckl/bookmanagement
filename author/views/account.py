from rest_framework import views,status,permissions
from rest_framework.response import Response
from .accounthelper import AdminOAuth2Token
from ..serializers.account import SigninSerializer

class Signin(AdminOAuth2Token,views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SigninSerializer
    
    def post(self,request,*args,**kwargs):
        response,status_code = {},status.HTTP_200_OK
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            response = self.generate_oauth_token(ser.data['username'],ser.data['password'])
        else:    
            response['result'],response['errors'],status_code = 'failure', {i: ser.errors[i][0] for i in ser.errors.keys()},status.HTTP_400_BAD_REQUEST
        return Response(response,status=status_code)