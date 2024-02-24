from django.core.paginator import Paginator
from django.db.models import Prefetch,Count

from rest_framework import viewsets,status,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers.author import AuthorCreateSerializer,AuthorListSerializer,AssignBookSerializer
from ..models import Book,Author,AuthorBook

class AuthorView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    def get_serializer_class(self):
        group_serilizer = {
           'create':AuthorCreateSerializer,
           'list':AuthorListSerializer,
           'assign_book':AssignBookSerializer
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
    
    def list(self,request, *args, **kwargs):
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',10)
        queryset = Author.objects.prefetch_related('author_review',Prefetch('author',queryset=AuthorBook.objects.select_related('book'))).\
            annotate(assigned_books_count=Count('author'),review_count=Count('author_review')).all()
        pagination = Paginator(queryset, limit)
        records = pagination.get_page(page)
        has_next = records.has_next()
        has_previous = records.has_previous()
        ser = self.get_serializer(records,many=True,context={'request':request})
        return Response({'result':'success','records':ser.data,'has_next':has_next,'has_previous':has_previous})
    
    def assign_book(self, request, *args, **kwargs):
        response,status_code = {},status.HTTP_200_OK
        ser = self.get_serializer(data=request.data,context={'id':self.kwargs['pk']})
        if ser.is_valid():
            ser.save()
            response['result'],response['message'] = 'success', 'Assigned successfully.'
        else:    
            response['result'],response['errors'],status_code = 'failure', {i: ser.errors[i][0] for i in ser.errors.keys()},status.HTTP_400_BAD_REQUEST
        return Response(response,status=status_code)