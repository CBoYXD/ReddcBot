from .dialogs.core import admin_dialog
from .messages import admin_router

admin_router.include_router(admin_dialog)
