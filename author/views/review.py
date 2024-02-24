
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers.review import ReviewCreateSerializer

class ReviewView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    def get_serializer_class(self):
        group_serilizer = {
           'create':ReviewCreateSerializer,
        }
        if self.action in group_serilizer.keys():
            return group_serilizer[self.action]
        
    def create(self, request, *args, **kwargs):
        response,status_code = {},status.HTTP_200_OK
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            response['result'],response['message'] = 'success', 'Saved successfully.'
        else:    
            response['result'],response['errors'],status_code = 'failure', {i: ser.errors[i][0] for i in ser.errors.keys()},status.HTTP_400_BAD_REQUEST
        return Response(response,status=status_code)