from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

#pagination
def pagination(queryset,request,serializer):
    page = 1
    items =10
    if "page" in request.query_params:
        page=request.query_params.get('page')
    if "item" in  request.query_params:
        items=request.query_params.get('item')
    paginator = Paginator(queryset,items)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    data = serializer(data, many= True).data
    total_page=(int(queryset.count())/int(items))
    if total_page == 0 and queryset.count() > 0:
        total_page=1
    result={
            "total_pages":math.ceil(total_page),
            "total_count":queryset.count(),
            "data":data,
        }
    return result