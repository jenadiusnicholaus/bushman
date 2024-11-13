from django.contrib import admin
from .models import (
    SalesConfirmationProposal,
    SalesConfirmationProposalPackage,
    SalesConfirmationProposalItinerary,
    SalesConfirmationProposalAdditionalService,
    SalesConfirmationProposalClientPreference,
    Installment,
    SalesConfirmationProposalStatus,
    GameActivity,
    EntityContractPermit,
    GameKilledActivity,
)

admin.site.register(SalesConfirmationProposal)
admin.site.register(SalesConfirmationProposalPackage)
admin.site.register(SalesConfirmationProposalItinerary)
admin.site.register(SalesConfirmationProposalAdditionalService)
admin.site.register(SalesConfirmationProposalClientPreference)
admin.site.register(Installment)
admin.site.register(SalesConfirmationProposalStatus)
admin.site.register(GameActivity)
admin.site.register(EntityContractPermit)
admin.site.register(GameKilledActivity)
