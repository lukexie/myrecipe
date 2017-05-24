"""
    メニュー関連
"""
import logging
from django.shortcuts import render
from django.http import HttpRequest
from django.views import generic
from common.models import Cuisine, Instruction, Quantity, Foodstuff
from .forms import CuisineForm

def cuisine_add(request: HttpRequest):
    """
    料理追加
    @param request
    @return: django template
    """
    return render(request, 'cuisine/edit.dhtml', {
        'title': 'レシピ追加',
        'cuisine': Cuisine(),
        'classification': (('', ''), ('1', '主菜'), ('2', '主食'), ('3', '副菜'), ('4', 'デザート')),
        'foodstuff_classification': (('', ''), ('1', '野菜'), ('2', '肉'), ('3', '調味料')),
    })

class CuisineListView(generic.ListView):
    """ 料理一覧 """
    model = Cuisine
    form_class = CuisineForm
    template_name = 'cuisine/index.dhtml'

    def __init__(self):
        self.title = 'レシピ一覧'
        self.classifications = ['主菜', '副菜', '主食', 'デザート', 'その他']

    def get(self, request: HttpRequest, *args, **kwargs):
        """ 初期表示 """
        return render(request, self.template_name, {
            'title': self.title,
            'form': self.form_class(),
            'classifications': self.classifications,
        })

    def post(self, request: HttpRequest, *args, **kwargs):
        """ 検索 """
        form = self.form_class(request.POST)
        obj = Cuisine.objects

        if form.is_valid():

            # 値を取得
            name = form.cleaned_data['name']
            classification = form.cleaned_data['classification']
            ingestion_kcal = form.cleaned_data['ingestion_kcal']

            # フィルタ
            obj = obj.filter(name__contains=name) if name else obj
            obj = obj.filter(classification__exact=classification) if classification else obj
            obj = obj.filter(ingestion_kcal__exact=ingestion_kcal) if ingestion_kcal else obj

            print(obj.all().query)

        return render(request, self.template_name, {
            'title': self.title,
            'form': form,
            'cuisines': obj.all(),
            'classifications': self.classifications,
        })

class CuisineAddView(generic.CreateView):
    """ レシピ登録ビュー """
    model = Cuisine
    template_name = 'cuisine/edit.dhtml'
    success_url = 'cuisine/edit.dhtml'
    fields = ['name', 'classification', 'ingestion_kcal', 'create_number_of_times']

    def __init__(self):
        self.title = 'レシピ詳細'
        self.classifications = ['主菜', '副菜', '主食', 'デザート', 'その他']
        self.foodstuff_classifications = ['野菜', '肉', '調味料']

class CuisineDetailView(generic.detail.DetailView):
    """ レシピ詳細ビュー """
    model = Cuisine
    template_name = 'cuisine/edit.dhtml'
    success_url = 'cuisine/edit.dhtml'
    # fields = ['name', 'classification', 'ingestion_kcal', 'create_number_of_times']

    def __init__(self):
        self.title = 'レシピ詳細'
        self.classifications = ['主菜', '副菜', '主食', 'デザート', 'その他']
        self.foodstuff_classifications = ['野菜', '肉', '調味料']

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_view(request, **kwargs)

    def render_view(self, request: HttpRequest, **kwargs):
        """ 描画処理 """
        return render(request, self.template_name, {
            'title': self.title,
            'id': kwargs.get('pk', ''),
            'cuisine': self.get_object(),
            'classifications': self.classifications,
            'foodstuff_classifications': self.foodstuff_classifications,
        })

    def get_object(self, queryset=None):
        target = super(CuisineDetailView, self).get_object(queryset)

        # 手順
        instructions = Instruction.objects.filter(cuisine=target).order_by('sort_order')
        target.instructions_set = instructions

        # 数量・食材
        quantities = Quantity.objects.filter(cuisine=target).prefetch_related('foodstuff')
        target.quantities_set = quantities

        logger = logging.getLogger('recipe')
        logger.info('レシピ【%s】が参照されました。', target.name)

        return target
