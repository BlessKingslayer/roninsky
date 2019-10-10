from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from roninsky.custom_site import custom_site
from roninsky.base_admin import BaseOwnerAdmin

# Register your models here.


class PostInline(admin.TabularInline):  # StackedInline 样式不同 TabularInline
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'    


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'  # 展示标题
    parameter_name = 'owner_category'  # 查询时url参数名字

    # 返回要展示的内容和查询用的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()  # parameter_name传递的值
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'owner'
    ]
    list_display_links = []  # 配置哪些字段作为链接

    list_filter = [CategoryOwnerFilter]  # 配置页面过滤器, 需要通过哪些字段来过滤页面
    search_fields = ['title', 'category__name']  # 配置搜索字段

    actions_on_top = True  # 动作相关的配置，是否展示在顶部
    action_on_bottom = True  # 动作相关的配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存、编辑、编辑并新建按钮是否展示在顶部

    # 不展示的字段
    exclude = ('owner',)

    # 限制要展示的字段，并配置展示字段的顺序
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )

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
                'desc', 'content'
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag', ),
        })
    )

    # 自定义字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'  # 指定表头的展示文案

    # 自定义资源引入
    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css'),
        }
        js = ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.js',)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
