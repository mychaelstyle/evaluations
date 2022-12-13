from django.http.response import JsonResponse
from django.middleware.csrf import get_token
from django.db.models import QuerySet, Model
from django.db.models.fields.related_descriptors import create_reverse_many_to_one_manager
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
import inspect

class CommonJsonResponse:
    """全体で使うJSONレスポンスのボディデータ構造を作成する

    Returns:
        _type_: _description_
    """
    RESPONSE_RESULT_OK = "OK"
    RESPONSE_RESULT_NG = "NG"
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.body = {}
        self.data = {}
        self.pageinfo = None
        self.messages = []
        self.field_errors = {}

    def add_message(self,msg):
        """レスポンスのmessagesにメッセージを追加する

        Args:
            msg (str): 追加するメッセージ文字列
        """
        self.messages.append(msg)

    def add_fielderror(self,name,msg):
        """入力フォームに対するメッセージを追加する

        Args:
            name (str): フィールド名
            msg (str): メッセージ
        """
        if name not in self.field_errors:
            self.field_errors[name] = []
        self.field_errors[name].append(msg)

    def set_fielderrors(self, errors):
        """入力フォームに対するメッセージを辞書形式で設定する

        Args:
            errors (dict): {入力フォーム名:[],}のdict
        """
        self.field_errors = errors

    def set_data(self,data, perpage:int=20, page:int=1):
        """dataフィールドで返すdictを設定する

        Args:
            data (dict): dataフィールドで返すdict
        """
        if isinstance(data,QuerySet):
            pagenator = Paginator(data,perpage)
            if page > pagenator.num_pages:
                page = pagenator.num_pages
            page_obj = pagenator.get_page(page)
            self.pageinfo = {
                "per_page" : perpage,
                "count" : pagenator.count,
                "num_pages" : pagenator.num_pages,
                "page" : page
            }
            d = []
            for row in page_obj:
                rd = self.model_to_dict(row)
                d.append(rd)
            self.data = d
        elif isinstance(data,Model):
            self.data = model_to_dict(data)
        else:
            self.data = data

    def model_to_dict(self, model):
        ret = {}
        for m in inspect.getmembers(model):
            if m[0].startswith("_"):
                continue
            if isinstance(m[1],int):
                ret[m[0]] = m[1]
            elif isinstance(m[1],str):
                ret[m[0]] = m[1]
            elif isinstance(m[1],datetime.datetime):
                ret[m[0]] = m[1]
            elif isinstance(m[1],datetime.date):
                ret[m[0]] = m[1]
            elif isinstance(m[1],Model):
                ret[m[0]] = self.model_to_dict(m[1])
        return ret

    def is_error(self):
        if len(self.messages) > 0 or len(self.field_errors) > 0:
            return True
        return False
        
    def get(self):
        """JSONResponseを作成して取得する

        Returns:
            django.http.response.JsonResponse: JSONレスポンス
        """
        self.body['messages'] = self.messages
        self.body['field_errors'] = self.field_errors
        if len(self.messages) > 0 or len(self.field_errors) > 0:
            self.body['result'] = self.RESPONSE_RESULT_NG
        else:
            self.body['result'] = self.RESPONSE_RESULT_OK
            if self.pageinfo is not None:
                self.body['pageinfo'] = self.pageinfo
        self.body['csrf_token'] = get_token(self.request)
        self.body['data'] = self.data
        return JsonResponse(self.body)
