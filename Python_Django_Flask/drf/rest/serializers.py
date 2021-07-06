from rest_framework import serializers

from .models import News, Comments


class NewsListSerializers(serializers.ModelSerializer):
    """List news"""

    class Meta:
        model = News
        exclude = ('user', 'many_news') # вывести все, кроме этих
        #fields = ('title', 'created_at', 'tag') # выводятся только эти поля


class CommentsCreateSerializers(serializers.ModelSerializer):
    """Comments create"""

    class Meta:
        model = Comments
        fields = '__all__'
        exclude = 'user'


class CommentsSerializers(serializers.ModelSerializer):
    """Comments"""

    class Meta:
        model = Comments
        fields = ('nickname', 'text')


class NewsDetailSerializers(serializers.ModelSerializer):
    """Detail news"""

    # comments = serializers.SlugRelatedField(slug_field='nickname', read_only=True, many=True) # по имени связанного
    # класса
    comments = CommentsSerializers(many=True) # по содержанию related_name

    class Meta:
        model = News
        fields = '__all__'
