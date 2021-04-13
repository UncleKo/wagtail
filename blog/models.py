from django import forms
# from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
# from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
# from wagtail.snippets.models import register_snippet

from streams import blocks


def paginate(request, all_posts, count):
    paginator = Paginator(all_posts, count)

    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(page.num_pages)
    
    return posts


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors"""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets."""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links",
        ),

    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


# register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]


# register_snippet(BlogCategory)


class BlogPageTag(TaggedItemBase):
  content_object = ParentalKey(
    'BlogDetailPage',
    related_name='BlogDetailPage',
    on_delete=models.CASCADE,
  )

class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.ArticleBlogPage', 'blog.VideoBlogPage']

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]


    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        # if request.GET.get('tag', None):
        #   tag = request.GET.get('tag')
        #   all_posts = all_posts.filter(tags__slug__in=[tag])

        posts = paginate(request, all_posts, 2)
        context["posts"] = posts

        context["categories"] = BlogCategory.objects.all()
        context["tags"] = Tag.objects.all()
        context["taged_items"] = BlogPageTag.objects.all()
        # context["special_link"] = self.reverse_subpage('latest_posts')
        return context

    @route(r'^category/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            messages.error(request, "指定されたカテゴリーは存在しませんでした。")
            return redirect('/blog/')
        # except BlogCategory.DoesNotExist:
        #     raise Http404("このカテゴリーは存在しません。")

        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at').filter(categories__in=[category])
        posts = paginate(request, all_posts, 1)
        context["posts"] = posts

        return render(request, "blog/blog_listing_page.html", context)

    @route(r'^tag/(?P<tag_slug>[-\w]*)/$', name="tag_view")
    def tag_view(self, request, tag_slug):
        """Find blog posts based on a tag."""
        context = self.get_context(request)

        try:
            tag = Tag.objects.get(slug=tag_slug)
        except Exception:
            messages.error(request, "指定されたタグは存在しませんでした。")
            return redirect('/blog/')

        # context["posts"] = BlogDetailPage.objects.live().public().order_by('-first_published_at').filter(tags__slug__in=[tag])
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at').filter(tags__in=[tag])
        posts = paginate(request, all_posts, 1)
        context["posts"] = posts
        
        return render(request, "blog/blog_listing_page.html", context)

    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        # context["latest_posts"] = BlogDetailPage.objects.all().order_by('-id')[:1]
        # context["latest_posts"] = BlogDetailPage.objects.live().public().order_by('-id')[:1]
        # context["latest_posts"] = BlogDetailPage.objects.live().public().reverse()[:1]
        context["latest_posts"] = context["posts"][:2]
        return render(request, "blog/latest_posts.html", context)

    @route(r'^posts/$')
    def article_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = ArticleBlogPage.objects.live(
        ).public().order_by('-first_published_at')
        return render(request, "blog/blog_listing_page.html", context)

    @route(r'^videos/$')
    def video_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = VideoBlogPage.objects.live(
        ).public().order_by('-first_published_at')
        return render(request, "blog/blog_listing_page.html", context)

    ### Other Sample Queries ###
    # posts = BlogDetailPage.objects.live().exact_type(BlogDetailPage)
    # posts = BlogDetailPage.objects.live().not_exact_type(BlogDetailPage)
    # articles = BlogDetailPage.objects.live().exact_type(ArticleBlogPage).specific(defer=False)
    # posts = BlogDetailPage.objects.live().not_exact_type(BlogDetailPage).specific()

    def get_sitemap_urls(self, request):
        # return [] # if you don't want this page on sitemap
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )

        return sitemap


class BlogDetailPage(Page):
    """Parental blog detail page."""

    parent_page_types = ['blog.BlogListingPage']
    subpage_types = []

    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
        # verbose_name="タイトル"
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    image_alt = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Add some alt text',
    )

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            # ("simple_richtext", blocks.SimpleRichTextBlock(features=["bold", "italic"])),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
        FieldPanel("image_alt", heading="Image Alt (Option)"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author",
                            min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        FieldPanel("tags"),
        StreamFieldPanel("content"),
    ]


    ### didn't work. How? ###
    # def form_valid(self, form):
    #   form.instance.author = self.request.user
    #   return super().form_valid(form)

    # First subclassed blog post


class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        InlinePanel("blog_authors", label="Author(s)", min_num=1, max_num=4),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        FieldPanel("tags"),
        StreamFieldPanel("content"),
    ]


# Second subclassed page
class VideoBlogPage(BlogDetailPage):
    """A video subclassed page."""

    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        # FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        InlinePanel("blog_authors", label="Author(s)", min_num=1, max_num=4),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        FieldPanel("tags"),
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("content"),
    ]

