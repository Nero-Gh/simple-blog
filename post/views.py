from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework import viewsets,generics,mixins
from rest_framework.decorators import api_view,permission_classes,APIView

from .serializers import Post,PostSerializer
from account.serializers import CurrentUserPostSerializer
from django.shortcuts import get_object_or_404
from .permissions import ReadOnly,AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

# Create your views here.



class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request: Request):

    if request.method == "POST":
        data = request.data

        response = {"message": "Hello World", "data": data}

        return Response(data=response, status=status.HTTP_201_CREATED)

    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)

class PostListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):

    """
    a view for creating and listing posts
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    pagination_class = CustomPaginator
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        print(serializer)
        return super().perform_create(serializer)
        
    @swagger_auto_schema(
            operation_summary="List All Post",
            operation_description="Return all post"
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary="Create a post",
            operation_description="Creates a post"
    )
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AuthorOrReadOnly]

    @swagger_auto_schema(
            operation_summary="Retrive a post by id",
            operation_description="Retrives a post by id"
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary="Update a post by id",
            operation_description="Updates a post by id"
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary="delete a post",
            operation_description="deletes a post by id"
    )
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostSerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)

#Filtering Post List
class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None

        queryset = Post.objects.all()

        if username is not None:
            return Post.objects.filter(author__username=username)

        return queryset

    @swagger_auto_schema(
            operation_summary="List post for an author who is a user",
            operation_description="List post for an author who is a user"
    )
    def get(self, request, *args, **kwargs):   
        return self.list(request, *args, **kwargs)


