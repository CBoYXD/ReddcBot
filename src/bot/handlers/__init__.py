from .admins import admin_router
from .user.messages import user_router

routers_list = [admin_router, user_router]
