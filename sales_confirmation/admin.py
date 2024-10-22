from django.contrib import admin
from .models import (
    SalesConfirmationProposal,
    SalesConfirmationProposalPackage,
    SalesConfirmationProposalItinerary,
    SalesConfirmationProposalAdditionalService,
    SalesConfirmationProposalClientPreference,
)

admin.site.register(SalesConfirmationProposal)
admin.site.register(SalesConfirmationProposalPackage)
admin.site.register(SalesConfirmationProposalItinerary)
admin.site.register(SalesConfirmationProposalAdditionalService)
admin.site.register(SalesConfirmationProposalClientPreference)
