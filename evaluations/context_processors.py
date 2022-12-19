from django.conf import settings
import os
import environ

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

def site_common_texts(request):
    data = {}
    data['GOOGLE_ANALYTICS_ID'] = env('GOOGLE_ANALYTICS_ID')
    return data