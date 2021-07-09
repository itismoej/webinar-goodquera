from rest_framework.permissions import BasePermission

from college.models import College


class IsCollegeMember(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if college_id := view.kwargs.get('college_id', None):
            if college := College.objects.filter(id=college_id).first():
                return college.has_member(request.user)

        return False
