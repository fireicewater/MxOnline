from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from pure_pagination import Paginator

from organization.models import CourseOrg,CityDict
from organization.forms import UserAskForm


class AddUserAsk(View):
    def post(self,request):
        user_askform=UserAskForm(request.POST)
        if user_askform.is_valid():
            user_askform.save(commit=True)
            return JsonResponse("{'status':'success'}")
        else:
            return JsonResponse("{'status':'fail','msg':{0}}".format(user_askform.errors))


class OrgView(View):
    def get(self,request):
        # 课程机构
        all_orgs=CourseOrg.objects.all()
        city=request.GET.get("city","")
        category=request.GET.get("category","")
        sort=request.GET.get("sort","")
        hot_orgs=CourseOrg.objects.order_by("-click_num")[:3]
        if city:
            all_orgs= all_orgs.filter(city_id=city)
        if category:
            all_orgs= all_orgs.filter(category=category)
        if sort:
            if sort=="students":
                all_orgs= all_orgs.order_by("-studnets")
            elif sort=="courses":
                all_orgs= all_orgs.order_by("-course_nums")
        #城市名
        all_citys=CityDict.objects.all();
        page = request.GET.get('page', 1)
        p = Paginator(all_orgs,5,request=request)
        page_obj = p.page(page)
        return render(request,"org-list.html",
                      {"all_orgs":page_obj,
                       "all_citys":all_citys,
                       "ciytid":city,
                        "category":category,
                       "hot_orgs":hot_orgs,
                       "sort":sort
                       })