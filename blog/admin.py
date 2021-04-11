from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry  # 查看日志

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site  # 自定义site
from typeidea.base_admin import BaseOwnerAdmin

# 查看操作日志
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["object_repr", "object_id", "action_flag", "user", "change_message"]


class PostInline(admin.TabularInline):
    """
    分类编辑中添加新增文章组件
    """
    fields = ("title", "desc")
    extra = 1  # 控制额外多几个
    model = Post


# Register your models here.
@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    """
    分类
    """
    # 分类编辑中新增/编辑文章的组件
    inlines = [PostInline, ]
    list_display = ("name", "status", "is_nav", "created_time", "post_count", "owner")
    fields = ("name", "status", "is_nav")

    # def save_model(self, request, obj, form, change):
    #     """
    #      models中定义了owner字段,必须填写
    #     重写save_model()方法，将当前登录用户赋值给owner字段
    #     :param request: 当前请求对象，通过request.user可获取当前已经登录的用户，如果未登录获取到的是匿名用户名
    #     :param obj: 当前要保存的对象
    #     :param form: 页面提交过来表单对象
    #     :param change: 标志本次保存的数据是新增还是更新的
    #     :return:
    #     """
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        """
        分类下面展示多少篇文章
        :param obj:
        :return:
        """
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    """
    标签
    """
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只展示当前用户分类，通过继承admin.SimpleListFilter类来实现自定义过滤器,
    之后把自定义过滤器配置到ModelAdmin中即可。
    SimpleListFilter类提供了两个属性和两个方法来供我们重写。
    title用来展示标题，parameter_name就是查询时URL参数的名字。
    lookups方法和queryset方法
    """
    # 展示标题
    title = "分类过滤器"
    # 查询时URL参数的名字,例如查询分类id=1的内容时，URL后面的Query部分是?owner_category=1,
    # 此时就可以通过过滤器拿这个id，从而进行过滤
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        """
        返回要展示的内容和查询用的id
        :param request:
        :param model_admin:
        :return:
        """
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        """
        根据URL Ouery内容返回列表页数据，
        :param request:
        :param queryset:
        :return:
        """
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# site=custom_site 自定义的site
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    """创建文章"""
    form = PostAdminForm
    # 页面列表展示字段，operator是自定义展示字段【操作】
    list_display = [
        "title", "category", "status", "created_time", "owner", "operator"
    ]
    # 配置哪些字段可以作为链接，点击即可进入编辑页面
    list_display_links = []
    # 配置页面过滤器字段,使用自定义的过滤器类
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段
    search_fields = ["title", "category__name"]
    # 展示在顶部动作相关
    actions_on_top = True
    # 展示在底部动作相关
    actions_on_bottom = True
    # 保存、编辑、编辑并新建按钮是否在顶部展示
    save_on_top = True

    # 编辑页面
    save_on_top = True
    # 指定owner字段不展示
    exclude = ("owner",)

    # 添加和编辑页面字段配置和字段展示的顺序
    # fields = (
    #     ("category", "title"),
    #     "desc",
    #     "status",
    #     "content",
    #     "tag",
    # )
    # 用来控制页面布局,用来替换fields
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    # 自定义列表上的编辑字段
    def operator(self, obj):
        """
        自定义字段
        :param obj: ob是固定搭配,指当前对象
        :return: 返回HTML，需要通过format_html函数处理,
        """
        # return format_html(
        #     '<a href="{0}">编辑</a>',
        #     reverse("admin:blog_post_change", args=(obj.id,))
        # )
        # 使用了typeidea下面的custom_site.py自定义的site修改如下
        return format_html(
            '<a href="{0}">编辑</a>',
            reverse("cus_admin:blog_post_change", args=(obj.id,))
        )

    # 列表头展示文案
    operator.short_description = "操作"

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(owner=request.user)

    class Media:
        css = {
            "all": ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrp.bundle.js",)
