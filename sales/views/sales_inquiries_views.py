from datetime import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date, parse_duration, parse_datetime

from bm_hunting_settings.models import IdentityType
from bm_hunting_settings.serializers import CreateEntityCategorySerializer
from sales.helpers import SalesHelper
from sales.models import (
    Contacts,
    Entity,
    EntityCategories,
    EntityCategory,
    SalesInquiry,
    SalesIquiryPreference,
)
from sales.serializers.sales_inquiries_serializers import (
    CreateContactsSerializers,
    CreateEntityCategorySerializers,
    CreateEntityIdentitySerializers,
    CreateEntitySerializers,
    CreateSalesInquiryAreaSerializer,
    CreateSalesInquirySerializers,
    CreateSalesIquiryPreferenceSerializers,
    GetContactsSerializers,
    GetEntitySerializers,
    GetSalesInquirySerializers,
    SalesIquiryPreferenceSerializers,
    UpdateEntitySerializers,
    createSalesInquiryPriceListSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from django.db.models import Q

from utils.pdf import SalesInquiryPDF


class SalesInquiriesViewSet(viewsets.ModelViewSet):
    queryset = SalesInquiry.objects.filter().order_by("-created_date")
    serializer_class = GetSalesInquirySerializers
    permission_classes = [IsAuthenticated]

    from django.db.models import Q

    def list(self, request, *args, **kwargs):
        from utils.utitlities import format_any_date

        queryset = self.queryset.filter(
            Q(sales_confirmation_proposal__status=None)
            | Q(sales_confirmation_proposal__status__status="pending")
        )

        # Get query parameters
        preferred_date = request.query_params.get("preferred_date")
        season_id = request.query_params.get("season_id")

        # Check if both parameters are None or empty strings
        if not preferred_date and not season_id:
            # No filters applied if both are empty
            queryset = self.queryset.filter(
                Q(sales_confirmation_proposal__status=None)
                | Q(sales_confirmation_proposal__status__status="pending")
            )

        # Try to format the preferred date
        try:
            formatted_date = (
                format_any_date(str(preferred_date)) if preferred_date else None
            )

        except ValueError as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter by parsed date only if it is valid
        if formatted_date:
            queryset = queryset.filter(
                Q(sales_inquiry_preference_set__preferred_date__gte=formatted_date)
            ).order_by("sales_inquiry_preference_set__preferred_date")

        # Filter by season_id only if it is valid (not empty)
        if season_id:
            queryset = queryset.filter(Q(season__id=season_id)).order_by(
                "sales_inquiry_preference_set__preferred_date"
            )

        # Serializing the queryset
        serializer = self.serializer_class(queryset, many=True)
        response_data = []

        for data in serializer.data:
            #  def get_pdf(self, obj):
            pdf_file = SalesInquiryPDF.generate_pdf(data, return_type="base64")
            data["pdf"] = pdf_file["pdf"]
            response_data.append(data)

        return Response(response_data)

    # save the following tables
    # entity
    # contact
    # entity_category
    # sales_inquiry
    # area of hunting
    # species preference

    def create(self, request, *args, **kwargs):
        from utils.utitlities import format_any_date

        try:
            preferred_date_str = format_any_date(request.data.get("preferred_date"))
        except ValueError as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        categories, _ = EntityCategories.objects.get_or_create(
            name=request.data.get("categories")
        )
        no_companion = 0
        no_observers = 0
        companion = request.data.get("no_of_companions", 0)

        if companion:
            no_companion = companion

        if request.data.get("no_of_observers"):
            no_observers = request.data.get("no_of_observers")

        # if not categories.exists():
        #     return Response(
        #         {"error": "No valid categories provided"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        identity, _ = IdentityType.objects.get_or_create(name="passport_number")

        entity_data = {
            "user": request.user.id,
            "full_name": request.data.get("full_name"),
            "nationality": request.data.get("nationality"),
            "country": request.data.get("country"),
        }

        category_data = {
            "entity": None,
            "category": categories.id,
        }

        print(category_data)

        contact_data = {
            "entity": None,
            "contact_type": None,
            "contact": None,
        }
        entity_identity_data = {
            "entity": None,
            "identity_type": identity.id,
            "identity_number": request.data.get("identity_number"),
        }

        sales_inquiry_data = {
            "user": request.user.id,
            "season": request.data.get("season"),
            "entity": None,
        }
        sales_inquiry_areas_of_hunting_data = {
            "sales_inquiry": None,
            "area": request.data.get("area_id"),
        }

        seles_inquiry_preference_data = {
            "sales_inquiry": None,
            "no_of_hunters": request.data.get("no_of_hunters"),
            "no_of_companions": no_companion,
            "no_of_days": request.data.get("no_of_days"),
            "no_of_observers": no_observers,
            "preferred_date": preferred_date_str,
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
        }
        sales_inquiry_price_list_data = {
            "sales_inquiry": None,
            "price_list": request.data.get("price_list_id"),
        }
        sales_prefered_species_data = {"sales_inquiry": None, "species": None}
        # print(request.data)
        try:
            with transaction.atomic():
                entity_serializer = CreateEntitySerializers(data=entity_data)
                if not entity_serializer.is_valid():
                    return Response(
                        entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                saved_entity = entity_serializer.save()

                # CreateEntityIdentitySerializers
                entity_identity_data.update({"entity": saved_entity.id})
                entity_identity_serializer = CreateEntityIdentitySerializers(
                    data=entity_identity_data
                )
                if not entity_identity_serializer.is_valid():
                    #  we do delete the entity if the entity_identity is not valid
                    # i am deleting the entity first because it is not possible to create entity_identity without entity
                    Entity.objects.get(id=saved_entity.id).delete()
                    return Response(
                        entity_identity_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                entity_identity_serializer.save()

                # create entity_category
                category_data.update({"entity": saved_entity.id})
                entity_category_serializer = CreateEntityCategorySerializers(
                    data=category_data
                )
                if not entity_category_serializer.is_valid():
                    #  we do delete the entity if the entity_category is not valid
                    # i am deleting the entity first because it is not possible to create entity_category without entity
                    Entity.objects.get(id=saved_entity.id).delete()
                    return Response(
                        entity_category_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                saved_category_serializer = entity_category_serializer.save()
                try:
                    SalesHelper.save_contacts(
                        contacts=request.data.get("contacts"),
                        contact_request_data=contact_data,
                        saved_entity_serializer=saved_entity,
                        category_serializer=saved_category_serializer,
                    )
                except Exception as e:
                    return Response(
                        {
                            "message": "Error while saving contacts",
                            "error": str(e),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                sales_inquiry_data.update({"entity": saved_entity.id})
                sales_inquiry_serializer = CreateSalesInquirySerializers(
                    data=sales_inquiry_data
                )
                if not sales_inquiry_serializer.is_valid():
                    #  we do delete the entity if the sales_inquiry is not valid
                    # i am deleting the entity first because it is not possible to create sales_inquiry without entity
                    Entity.objects.get(id=saved_entity.id).delete()
                    EntityCategory.objects.get(id=saved_category_serializer.id).delete()
                    Contacts.objects.filter(entity__id=saved_entity.id).delete()
                    return Response(
                        sales_inquiry_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                saved_sales_inquiry = sales_inquiry_serializer.save()
                seles_inquiry_preference_data.update(
                    {"sales_inquiry": saved_sales_inquiry.id}
                )
                sales_inquiry_areas_of_hunting_data.update(
                    {"sales_inquiry": saved_sales_inquiry.id}
                )

                sales_inquiry_preference_serializer = (
                    CreateSalesIquiryPreferenceSerializers(
                        data=seles_inquiry_preference_data
                    )
                )
                if not sales_inquiry_preference_serializer.is_valid():
                    #  we do delete the entity if the sales_inquiry_preference is not valid
                    # i am deleting the entity first because it is not possible to create sales_inquiry_preference without sales_inquiry
                    # Entity.objects.get(id=saved_entity.id).delete()
                    saved_entity.delete()
                    saved_sales_inquiry.delete()
                    saved_category_serializer.delete()
                    # SalesInquiry.objects.get(id=saved_sales_inquiry.id).delete()
                    # EntityCategory.objects.get(id=saved_category_serializer.id).delete()
                    Contacts.objects.filter(entity__id=saved_entity.id).delete()
                    return Response(
                        sales_inquiry_preference_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                sales_inquiry_preference_serializer.save()
                # sales_prefered_species_data.update(
                #     {"sales_inquiry": saved_sales_inquiry.id}
                # )
                sales_inquiry_area_serializer = CreateSalesInquiryAreaSerializer(
                    data=sales_inquiry_areas_of_hunting_data
                )
                if not sales_inquiry_area_serializer.is_valid():
                    #  we do delete the entity if the sales_inquiry_area is not valid
                    # i am deleting the entity first because it is not possible to create sales_inquiry_area without sales_inquiry
                    saved_entity.delete()
                    saved_sales_inquiry.delete()
                    saved_category_serializer.delete()
                    return Response(
                        sales_inquiry_area_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                sales_inquiry_area_serializer.save()

                # sales inquiry price list
                sales_inquiry_price_list_data.update(
                    {"sales_inquiry": saved_sales_inquiry.id}
                )
                sales_inquiry_price_list_serializer = (
                    createSalesInquiryPriceListSerializer(
                        data=sales_inquiry_price_list_data
                    )
                )
                if not sales_inquiry_price_list_serializer.is_valid():
                    #  we do delete the entity if the sales_inquiry_price_list is not valid
                    # i am deleting the entity first because it is not possible to create sales_inquiry_price_list without sales_inquiry
                    saved_entity.delete()
                    saved_sales_inquiry.delete()
                    saved_category_serializer.delete()

                    return Response(
                        sales_inquiry_price_list_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                saved_price_list = sales_inquiry_price_list_serializer.save()

                try:
                    SalesHelper.savePreferredSpecies(
                        request=request,
                        sales_prefered_species_data=sales_prefered_species_data,
                        saved_sales_inquiry=saved_sales_inquiry,
                        save_entity_serializer=saved_entity,
                    )
                except Exception as e:
                    return Response(
                        {
                            "message": "Error while saving preferred species",
                            "error": str(e),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return Response(
                    {
                        "message": "Sales Inquiry created successfully",
                        "entity": entity_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return Response(
                {"message": "Error while creating entity"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SalesInquiriesClientBasicinfosViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = GetEntitySerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                ob = self.queryset.get(id=entity_id)
                serializer = self.get_serializer(ob)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Entity.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        #  entity data
        entity_data = {
            "user": request.user.id,
            "full_name": request.data.get("full_name"),
            "nick_name": request.data.get("nick_name"),
            "country": request.data.get("country"),
            "nationality": request.data.get("nationality"),
        }

        entity_serializer = CreateEntitySerializers(data=entity_data)

        if not entity_serializer.is_valid():
            return Response(
                entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        saved_entity = entity_serializer.save()
        # entity = entity_serializer.instance
        entity_category_data = {
            "entity": saved_entity.id,
            "category": request.data.get("category"),
        }

        # sales Inquiry data
        sales_inquiry_data = {
            "user": request.user.id,
            "entity": saved_entity.id,
            "remarks": request.data.get("remarks"),
        }

        entity_category_serializer = CreateEntityCategorySerializers(
            data=entity_category_data
        )

        seles_inquiry_serializer = GetSalesInquirySerializers(data=sales_inquiry_data)

        if not entity_category_serializer.is_valid():
            entity = Entity.objects.get(id=saved_entity.id)
            entity.delete()
            errors = [
                entity_category_serializer.errors,
                seles_inquiry_serializer.errors,
            ]

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if not seles_inquiry_serializer.is_valid():
            entity = Entity.objects.get(id=saved_entity.id)
            entity.delete()
            errors = [
                entity_category_serializer.errors,
                seles_inquiry_serializer.errors,
            ]

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        entity_category_serializer.save()
        saved_seles_inquiry = seles_inquiry_serializer.save()

        return Response(
            {
                "message": "Entity created successfully",
                "entity": entity_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class SearchSalesInquiriesViewSet(viewsets.ModelViewSet):
    queryset = SalesInquiry.objects.all()
    serializer_class = GetSalesInquirySerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all().order_by(
            "-sales_inquiry_preference_set__preferred_date"
        )
        query = request.query_params.get("query", None)
        if query:
            queryset = self.queryset.filter(
                Q(entity__full_name__icontains=query) | Q(code=query)
            ).order_by("-sales_inquiry_preference_set__preferred_date")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesClientContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = GetContactsSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                ob = self.queryset.get(entity=entity_id)
                serializer = self.get_serializer(ob)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Entity.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        client_contact_data = {
            "entity": request.data.get("entity_id"),
            "contact_type": request.data.get("contact_type"),
            "contact": request.data.get("contact"),
            "contactable": request.data.get("contactable"),
        }

        serializer = CreateContactsSerializers(data=client_contact_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                entity = Entity.objects.get(id=entity_id)
            except Entity.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            entity_data = {
                "full_name": request.data.get("full_name", entity.full_name),
                "email": request.data.get("email", entity.email),
                "phone_number": request.data.get("phone_number", entity.phone_number),
                "address": request.data.get("address", entity.address),
                "nationality": request.data.get("nationality", entity.nationality),
                "country": request.data.get("country", entity.nationality),
            }
            entity_serializer = UpdateEntitySerializers(
                entity, data=entity_data, partial=True
            )

            if entity_serializer.is_valid():
                self.perform_update(entity_serializer)
                if EntityCategory.objects.filter(entity=entity).exists():
                    c = EntityCategory.objects.filter(entity=entity).first()
                    categorySerializer = CreateEntityCategorySerializers(
                        c,
                        data={
                            "entity": entity.id,
                            "category": request.data.get("category"),
                        },
                        partial=True,
                    )
                else:
                    categorySerializer = CreateEntityCategorySerializers(
                        data={
                            "entity": entity.id,
                            "category": request.data.get("category"),
                        }
                    )
                if not categorySerializer.is_valid():
                    return Response(
                        categorySerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                categorySerializer.save()

                return Response(
                    {
                        "message": "Entity updated successfully",
                        "entity": entity_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    "message": "Please provide entity_id in query params to update entity"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                entity = Entity.objects.get(id=entity_id)
            except Entity.DoesNotExist:
                return Response(
                    {"message": "Entity does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            entity.delete()
            return Response(
                {"message": "Entity deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Please provide entity_id in query params to delete entity"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SalesIquiryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = SalesIquiryPreference.objects.all()
    serializer_class = SalesIquiryPreferenceSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sales_inquiry_id = request.query_params.get("sales_inquiry_id", None)
        if sales_inquiry_id:
            try:
                ob = self.queryset.get(sales_inquiry=sales_inquiry_id)
                serializer = self.get_serializer(ob)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SalesInquiry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        sales_inquiry, created = SalesInquiry.objects.get_or_create(
            entity=self.request.data.get("entity_id")
        )

        sales_inquiry_preference_data = {
            "sales_inquiry": sales_inquiry.id,
            "payment_method": request.data.get("payment_method_id"),
            "prev_experience": request.data.get("prev_experience"),
            "preffered_date": request.data.get("preffered_date"),
            "no_of_hunters": request.data.get("no_of_hunters"),
            "no_of_observers": request.data.get("no_of_observers"),
            "no_of_days": request.data.get("no_of_days"),
            "no_of_companions": request.data.get("no_of_companions"),
            "special_requests": request.data.get("special_requests"),
            "budget_estimation": request.data.get("budget_estimation"),
            "accommodation_type": request.data.get("accommodation_type"),
        }

        serializers = CreateSalesIquiryPreferenceSerializers(
            data=sales_inquiry_preference_data
        )

        if serializers.is_valid():
            serializers.save()
            return Response(
                {"message": "Sales Inquiry Preference created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
