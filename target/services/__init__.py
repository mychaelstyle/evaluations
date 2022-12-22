from django.http import Http404
from django.forms import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from ..models import Target, Anonymous

AUTH_TARGETS_SESSION = 'authenticated_targets'

def is_authenticated(request, uuid:str) -> bool:
    """指定のターゲットが認証済みか確認

    Args:
        request (_type_): Requestオブジェクト
        target_uuid (_type_): ターゲットのUUID

    Returns:
        _type_: _description_
    """
    authed_targets = request.session.get(AUTH_TARGETS_SESSION,[])
    if str(uuid) in authed_targets:
        return True
    return False

def authenticate(request, uuid:str, passcode:str) -> Target:
    """指定のUUIDの目標の認証

    Args:
        request (_type_): _description_
        uuid (str): _description_
        passcode (str): _description_

    Raises:
        Http404: _description_
        ValidationError: _description_
        ValidationError: _description_
        ValidationError: _description_

    Returns:
        Target: _description_
    """
    target = Target.objects.prefetch_related('items','items__item').filter(uuid=uuid).first()
    if target is None:
        raise Http404('Not found!')
    if target.passcode is None or len(target.passcode)==0:
        # 目標設定にパスコードが設定されていない場合
        if passcode is None or len(passcode)==0:
            # パスコードも入力がないの正解でパス
            pass
        else:
            # パスコードが入力されていたらエラー
            raise ValidationError(_("passcode_is_invalid"),"passcode_is_invalid")
    elif len(target.passcode)>0:
        # 目標設定にパスコードが設定されている場合
        if passcode is None or len(passcode)==0:
            # パスコードが入力されていないならエラー
            raise ValidationError(_("passcode_is_required"),"passcode_is_required")
        elif not check_password(passcode,target.passcode):
            # 設定されたパスコードが一致しないならエラー
            raise ValidationError(_("passcode_is_invalid"),"passcode_is_invalid")

    authed_targets = request.session.get(AUTH_TARGETS_SESSION,[])
    authed_targets.append(uuid)
    request.session[AUTH_TARGETS_SESSION] = authed_targets
    # 目標設定のcreator_idを確認して関連付け
    creator_id = get_anonymous(request)
    if target.creator_id is None:
        target.creator_id = creator_id
        target.save()
    elif str(target.creator_id) != creator_id:
        relate_anonymous(target.creator_id, creator_id)
    return target

def remove_auth(request, uuid):
    """認証済みの目標をセッションから削除

    Args:
        request (_type_): _description_
        uuid (_type_): _description_
    """
    authed_targets = request.session.get(AUTH_TARGETS_SESSION,[])
    authed_news = []
    for authed_uuid in authed_targets:
        if uuid != authed_uuid:
            authed_news.append(authed_uuid)
    request.session[AUTH_TARGETS_SESSION] = authed_news

def get_anonymous(request):
    """匿名ユーザーのUUIDを取得

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    anonymous_uuid = request.COOKIES.get('euuid',None)
    if anonymous_uuid is None:
        anonymous = Anonymous()
        anonymous.save()
        return str(anonymous.uuid)
    else:
        anonymous = Anonymous.objects.filter(Q(uuid=anonymous_uuid) | Q(related=anonymous_uuid)).order_by("id").first()
        if anonymous is not None:
            return str(anonymous.uuid)
        else:
            anonymous = Anonymous()
            anonymous.save()
            return str(anonymous.uuid)

def relate_anonymous(s_uuid, d_uuid):
    anonymous = Anonymous.objects.filter(uuid=d_uuid).order_by("id").first()
    if anonymous is not None:
        anonymous.related = s_uuid
        anonymous.save()
        return str(anonymous.uuid)
    else:
        return None