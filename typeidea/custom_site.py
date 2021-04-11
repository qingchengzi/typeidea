#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： 青城子
# datetime： 2021/4/11 18:43 
# ide： PyCharm

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = "Typeidea"
    site_title = "Typeidea管理后台"
    index_title = "首页"


custom_site = CustomSite(name="cus_admin")
