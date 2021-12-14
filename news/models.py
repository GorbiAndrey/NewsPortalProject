from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRating = self.post_set.aggregate(postRatings = Sum('rating'))
        pRat = 0
        pRat += postRating.get('postRating')

        commentRating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        comRat = 0
        comRat += commentRating.get('commentRating')

        self.ratingAuthor = pRat * 3 + comRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    post = 'PT'
    news = 'NS'

    TOPIC = [
        (post, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    topic = models.CharField(max_length=2,
                                choices=TOPIC,
                                default=news)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.TextField(max_length=128)
    post_text = models.TextField(default='Текст статьи')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='no comments')
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
