from django.db import models


class Author(models.Model):

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Author № {self.pk} - {self.name!r}'


class Category(models.Model):

    name = models.CharField(max_length=40)

    def __str__(self):
        return f'Category № {self.pk} - {self.name}'


class Tag(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return f'Tag № {self.pk} - {self.name}'

class Article(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)


    def __str__(self):
        return f'Article № {self.pk} - {self.title}.'