import jwt
from datetime import datetime, timedelta
from django.conf import settings
from functools import wraps
from django.http import JsonResponse
from .models import User

# Generate JWT token
def generate_token(user_id, is_admin):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

# Admin authorization decorator
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized - No valid token provided'}, status=401)
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if not payload.get('is_admin'):
                return JsonResponse({'error': 'Forbidden - Admin access required'}, status=403)
            
            # Add user to request for views that need user info
            user_id = payload.get('user_id')
            request.user = User.objects.get(id=user_id)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)
            
        return view_func(request, *args, **kwargs)
    return wrapper 