from django.contrib import admin

# Register your models here.

from approval_chain.models import (
    ApprovalChain,
    ApprovalChainLevels,
    ApprovalChainModule,
    ApprovalChainRole,
)

admin.site.register(ApprovalChain)
admin.site.register(ApprovalChainLevels)
admin.site.register(ApprovalChainModule)
admin.site.register(ApprovalChainRole)
