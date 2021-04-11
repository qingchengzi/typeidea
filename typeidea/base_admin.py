#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： 青城子
# datetime： 2021/4/11 19:13 
# ide： PyCharm

from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
