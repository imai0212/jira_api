# GETメソッドでJSONオブジェクトを要求する際の詳細設定を行う
from rest_framework import serializers
from .models import Category, Task, Profile
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    # ユーザーの属性を設定
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        # パラメータに対する追加オプション(閲覧不可、必須項目)
        extra_kwargs = {'password':{'write_only': True, 'required': True}}
    # passwordのハッシュ化
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        # プロフィールはdjangoが自動で行うため閲覧のみ
        extra_kwargs = {'user_profile': {'read_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','item']


class TaskSerializer(serializers.ModelSerializer):
    # categoryモデルのitem(文字列)情報を受け取る(モデルが別クラス参照時の記法)
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)
    responsible_username = serializers.ReadOnlyField(source='responsible.username', read_only=True)
    # display：STATUSの文字列
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name', 'category', 'category_item',
                  'estimate','responsible','responsible_username','owner','owner_username', 'created_at','updated_at']
        extra_kwargs = {'owner': {'read_only': True}}
