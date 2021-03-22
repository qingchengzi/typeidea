from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    分类
    """
    list_display = ("name", "status", "is_nav", "created_time", "post_count")
    fields = ("name", "status", "is_nav")

    def save_model(self, request, obj, form, change):
        """
         models中定义了owner字段,必须填写
        重写save_model()方法，将当前登录用户赋值给owner字段
        :param request: 当前请求对象，通过request.user可获取当前已经登录的用户，如果未登录获取到的是匿名用户名
        :param obj: 当前要保存的对象
        :param form: 页面提交过来表单对象
        :param change: 标志本次保存的数据是新增还是更新的
        :return:
        """
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        """
        分类下面展示多少篇文章
        :param obj:
        :return:
        """
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签
    """
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """创建文章"""
    # 页面列表展示字段，operator是自定义展示字段
    list_display = [
        "title", "category", "status", "created_time", "operator"
    ]
    # 配置哪些字段可以作为链接，点击即可进入编辑页面
    list_display_links = []
    # 配置页面过滤器字段
    list_filter = ["category"]
    # 配置搜索字段
    search_fields = ["title", "category__name"]
    # 展示在顶部动作相关
    actions_on_top = True
    # 展示在底部动作相关
    actions_on_bottom = True

    # 保存、编辑、编辑并新建按钮是否在顶部展示
    save_on_top = True

    fields = (
        ("category", "title"),
        "desc",
        "status",
        "content",
        "tag",
    )

    # 自定义列表上的编辑字段
    def operator(self, obj):
        """
        自定义字段
        :param obj: ob是固定搭配,指当前对象
        :return: 返回HTML，需要通过format_html函数处理,
        """
        return format_html(
            '<a href="{0}">编辑</a>',
            reverse("admin:blog_post_change", args=(obj.id,))
        )

    # 列表头展示文案
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
