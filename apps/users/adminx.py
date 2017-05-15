import xadmin
from users.models import EmailVerifyRecord, Banner
from xadmin import views


# 全局设置
class BaseSetting(object):
    # 主题功能开启
    enable_themes=True
    use_bootswatch=True
# 页面页头页脚
class GlobalSetting(object):
    site_title="暮雪后台管理系统"
    site_footer="暮雪在线网"
    # 菜单收起
    menu_style="accordion"

class EmailVerifyRecordAdmin (object):
    list_display=["code","email","send_type","send_time"]
    search_fields=["code","email","send_type"]
    list_filter=["code","email","send_type","send_time"]

class BannerAdmin(object):
    list_display=["title","image","url","index","add_time"]
    search_fields=["title","image","url","index"]
    list_filter=["title","image","url","index","add_time"]


xadmin.site.register (EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register (Banner, BannerAdmin)
# 注册全局views
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 页面页头页脚
xadmin.site.register(views.CommAdminView,GlobalSetting)
