from sales.serializers.sales_inquiries_serializers import (
    CreateContactsSerializers,
    CreateSalesInquirySpeciesSerializer,
    GetSalesInquirySpeciesSerializer,
    SalesIquiryPreferenceSerializers,
)
from sales.models import (
    ContactType,
    Contacts,
    Entity,
    EntityCategory,
    SalesInquiry,
    SalesIquiryPreference,
)
from rest_framework import status
from rest_framework.response import Response


class SalesHelper:
    def __init__(self):
        pass

    @staticmethod
    def save_contacts(
        contacts,
        contact_request_data,
        saved_entity_serializer,
        category_serializer,
    ):
        # Loop through each contact

        for contact in contacts:
            # Prepare contact data for serialization
            contact_request_data.update(
                {  # Use update for clarity
                    "entity": saved_entity_serializer.id,
                    "category": category_serializer.id,
                }
            )

            try:
                c_type_obj, created = ContactType.objects.get_or_create(
                    name=contact.get("contact_type")
                )
            except ContactType.DoesNotExist:
                raise Exception("Contact type does not exist")

            contact_request_data.update(
                {  # Use update for clarity
                    "contact_type": c_type_obj.id,
                    "contact": contact.get("contact"),  # Access contact directly
                }
            )

            # Create contact serializer with request data
            contact_serializer = CreateContactsSerializers(data=contact_request_data)
            if not contact_serializer.is_valid():
                # If the contact is not valid, delete the entity and its categories
                Entity.objects.filter(id=saved_entity_serializer.id).delete()
                EntityCategory.objects.filter(
                    entity_id=saved_entity_serializer.id
                ).delete()
                #

                raise Exception(contact_serializer.errors)

            contact_serializer.save()

    @staticmethod
    def savePreferredSpecies(
        request,
        sales_prefered_species_data,
        saved_sales_inquiry,
        save_entity_serializer,
    ):
        preferred_species = request.data.get("preferred_species")
        
        if preferred_species:
            for species in preferred_species:
                # Prepare the data for the serializer
                sales_prefered_species_data["sales_inquiry"] = saved_sales_inquiry.id
                sales_prefered_species_data["species"] = species.get("species_id")
                sales_prefered_species_data["quantity"] = species.get("quantity")

                # Create the serializer instance
                sales_preferred_species_serializer = (
                    CreateSalesInquirySpeciesSerializer(
                        data=sales_prefered_species_data
                    )
                )

                # Validate the serializer
                if not sales_preferred_species_serializer.is_valid():
                    # Delete the sales inquiry entity if the serializer is not valid
                    Entity.objects.filter(id=save_entity_serializer.id).delete()
                    SalesInquiry.objects.filter(
                        entity__id=save_entity_serializer.id
                    ).delete()
                    Contacts.objects.filter(
                        entity__id=save_entity_serializer.id
                    ).delete()
                    EntityCategory.objects.filter(
                        entity__id=save_entity_serializer.id
                    ).delete()
                    SalesIquiryPreference.objects.filter(
                        sales_inquiry__id=saved_sales_inquiry.id
                    ).delete()

                    raise ValueError(sales_preferred_species_serializer.errors)

                # Save the valid instance
                sales_preferred_species_serializer.save()
