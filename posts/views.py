from .models import Post
from .serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

import math


# Create your views here.
class Posts(APIView):
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = 5
        data = Post.objects.all()[(page-1)*page_size:page*page_size]
        count = Post.objects.all().count()
        max_page = math.ceil(count/page_size)
        next = f"http://localhost:8000/api/v1/posts/?page={page+1}" if max_page >= page+1 else None
        previous = f"http://localhost:8000/api/v1/posts/?page={page-1}" if page-1 > 0 else None
        serializer = PostSerializer(data, many=True)
        return Response({
            "count": count,
            "next":next,
            "previous": previous,
            "results": serializer.data
        })
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PostsDetail(APIView):
    def get_object(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)