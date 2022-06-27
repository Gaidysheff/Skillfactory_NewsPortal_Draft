from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):

        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentsRat = self.authorUser.comments_set.all(
        ).aggregate(commentsRating=Sum('rating'))
        cRat = 0
        cRat += commentsRat.get('commentsRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name='Автор:')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    STATUS_CHOICES = [
        ('d', 'Черновик'),
        ('p', 'Опубликовано'),
        ('w', 'в архиве'),
    ]

    categoryType = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name='Тип публикации')
    dateCreation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ManyToManyField(
        Category, through='PostCategory', verbose_name='Категория поста')
    title = models.CharField(max_length=128, verbose_name='Заголовок поста')
    text = models.TextField(null=True, blank=True, verbose_name='Текст поста (необязательно)',
                            help_text='Введите здесь текст своего Поста, хотя можете и не вводить, если нет желания!')
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name='Изображение')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг:')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='d', verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-dateCreation']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def display_category(self):
        return '\n'.join([c.categoryThrough for c in self.postCategory.all()])

    display_category.short_description = 'Категория'

    # def display_category(self):
    #     return ', '.join([postCategory.categoryThrough for postCategory in self.postCategory.all()
    #                       # [:3]
    #                       ])
    # display_category.short_description = 'Категория'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория поста')

    def __str__(self):
        return f'{self.postThrough}{self.categoryThrough}'


class Comments(models.Model):
    commentPost = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Заголовок поста')
    commentUser = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите здесь текст своего комментария')
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг:')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:10]}...'
