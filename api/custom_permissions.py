from rest_framework import permissions

# owner権限(ownerのidに一致する場合のみ更新・削除可能)
class OwnerPermission(permissions.BasePermission):
    # override
    def has_object_permission(self, request, view, obj):
        # GETメソッド(情報取得のみ)でアクセス時は許可
        if request.method in permissions.SAFE_METHODS:
            return True
        # それ以外でのアクセスはownerのidと一致する場合のみ許可
        return obj.owner.id == request.user.id
