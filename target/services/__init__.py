from django.http import Http404
from django.forms import ValidationError
from django.utils.translation import gettext as _

from django.contrib.auth.hashers import check_password

from ..models import Target

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