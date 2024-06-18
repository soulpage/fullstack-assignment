from rest_framework import permissions

class IsAdminOrUploader(permissions.BasePermission):
    """
    Custom permission to allow only admin users or the uploader of the file to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET requests (read-only) for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow admin users to perform any action
        if request.user.is_superuser:
            return True

        # Check if the user is the uploader of the file
        return obj.uploaded_by == request.user
