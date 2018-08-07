from rest_framework import viewsets
from task.models import Group, Element
from api.serializers import GroupSerializer, ElementSerializer
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
        )


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.filter(check_by_moderator=True)
    serializer_class = ElementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


@csrf_exempt
@api_view(['GET'])
def elements_by_group(request, pk):
    group = Group.objects.filter(id=pk)[0]
    group_elements = group.elements.all()
    serializer_context = {'request': request}
    serializer = ElementSerializer(group_elements, many=True, context=serializer_context)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def children_by_group(request, pk):
    group = Group.objects.filter(id=pk)[0]
    group_children = group.get_children()
    serializer_context = {'request': request}
    serializer = GroupSerializer(group_children, many=True, context=serializer_context)
    return Response(serializer.data)


# @csrf_exempt
# @api_view(['GET'])
# def elements(request):
#     elements = Element.objects.filter(check_by_moderator=True)[0]
#     serializer_context = {'request': request}
#     serializer = ElementSerializer(elements, many=True, context=serializer_context)
#     return Response(serializer.data)