from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# DBのprimary_keyのセキュリティーを高める
import uuid


def upload_avatar_path(instance, filename):
    # ファイル名を「,」ごとに分解し、末尾の要素(拡張子)をext変数に代入
    ext = filename.split(',')[-1]
    # mediaのavatarsファイルに「id.拡張子/id.拡張子/」形式で保存
    return '/'.join(['avatars', str(instance.user_profile.id) + str(".") + str(ext)])


class Profile(models.Model):
    # djangoのUserモデルと１対１で対応させる
    user_profile = models.OneToOneField(
        User, related_name='user_profile',
        # Userモデルの削除後にProfileオブジェクトも自動削除
        on_delete=models.CASCADE
    )
    # プロフィール画像(アップロードなしOK,アップロード先)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    # 関数全体の返り値：インスタンス発生時にusernameの文字内容を返す
    def __str__(self):
        return self.user_profile.username


class Category(models.Model):
    item = models.CharField(max_length=100)

    # itemの文字内容を返す
    def __str__(self):
        return self.item


class Task(models.Model):
    STATUS = (
        ('1', 'Not started'),
        ('2', 'On going'),
        ('3', 'Done'),
    )
    # primary_keyとして有効, 編集不可
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    status = models.CharField(max_length=40, choices=STATUS, default='1')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 日数の最小値を0に設定
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    # Userモデルに関連付ける
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible')
    # 作成日時(オブジェクト作成日時をDBに自動登録)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # taskのタイトルを返す
    def __str__(self):
        return self.task
