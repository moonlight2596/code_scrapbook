from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    """
    A model to store our snippets
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenums = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
    editor = models.ForeignKey('Editor', related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)

    class Meta: # pylint: disable=missing-class-docstring
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` lib to create a highlighted HTML representation
        of the code snippet
        """
        lexer = get_lexer_by_name(self.language)
        linenums = 'table' if self.linenums else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenums, full=True,
                                  **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

class Editor(models.Model):
    """
    A model to store information on preferred IDEs.
    """
    release = models.DateField()
    name = models.CharField(max_length=100)
    ai_support = models.BooleanField(default=True)
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='editor_profile',
        null=True,
        blank=True,
    )
    PLATFORM_CHOICES = [
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('apple', 'Apple Silicon'),
    ]
    supported_platforms = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        default='linux'
    )

    class Meta:
        ordering = ['release']