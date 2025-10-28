from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Profile
from .serializer import RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsProfileOrReadOnly
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        data = {
            "username" : user.username, 
            "email" : user.email,
            "bio" : getattr(user, "bio", ""),
            "profile_picture" : getattr(user, "profile_picture", None ),
            "token" : token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user  = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        data = {
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, "bio", ""),
            "profile_picture": getattr(user, "profile_picture", None),
            "token": token.key
        }

        return Response(data, status=status.HTTP_200_OK)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOrReadOnly]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        target = self.get_object()  # profile to follow
        user = request.user

        if user == target:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # if user is not already following target
        if user not in target.followers.all():
            target.followers.add(user)   # add user as a follower of target
            # create notification
            Notification.objects.create(
                recipient=target,
                actor=user,
                verb='followed you',
                content_type=ContentType.objects.get_for_model(target),
                object_id=target.id
            )
            return Response({'detail': f'You followed {target.username}.'}, status=status.HTTP_200_OK)

        return Response({'detail': f'You already follow {target.username}.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])  # use POST for remove follow for parity or DELETE as you prefer
    def unfollow(self, request, pk=None):
        target = self.get_object()
        user = request.user

        # check if user currently follows target
        if target in user.following.all():
            user.following.remove(target)  # remove target from the list user is following
            return Response({'detail': f'You unfollowed {target.username}.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        profile = self.get_object()
        followers_list = profile.followers.all()
        serializer = ProfileSerializer(followers_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        profile = self.get_object()
        following_list = profile.following.all()
        serializer = ProfileSerializer(following_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)