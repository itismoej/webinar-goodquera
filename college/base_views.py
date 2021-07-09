from rest_framework.views import APIView as _APIView


class APIView(_APIView):

    def get_permissions(self):
        # Instances and returns the dict of permissions that the view requires.
        return {
            key: [permission() for permission in permissions]
            for key, permissions in self.permission_classes.items()
        }

    def check_permissions(self, request):
        # Gets the request method and the permissions dict, and checks the permissions defined in the key matching
        # the method.
        method = request.method.lower()
        for permission in self.get_permissions()[method]:
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        method = request.method.lower()
        for permission in self.get_permissions()[method]:
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )
