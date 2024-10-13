from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bm_hunting_settings.serializers import CreateEntityCategorySerializer
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
    CreateEntitySerializers,
    CreateSalesIquiryPreferenceSerializers,
    GetContactsSerializers,
    GetEntitySerializers,
    GetSalesInquirySerializers,
    SalesIquiryPreferenceSerializers,
    UpdateEntitySerializers,
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


# Create your views here.


class SalesInquiriesViewSet(viewsets.ModelViewSet):
    queryset = SalesInquiry.objects.all()
    serializer_class = CreateSalesIquiryPreferenceSerializers
    permission_classes = [IsAuthenticated]


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

        # sales Inquiry data

        # CreateEntityCategorySerializer

        # entity_serializer = CreateEntitySerializers(data=entity_data)

        # if not entity_serializer.is_valid():
        #     return Response(
        #         entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        #     )

        # # sales Inquiry data
        # sales_inquiry_data = {
        #     "user": request.user.id,
        #     "entity": None,
        #     "remarks": request.data.get("remarks"),
        # }

        # # entity categoory
        # entity_category_data = {
        #     "entity": None,
        #     "category": request.data.get("category"),
        # }

        # # CreateSalesIquiryPreferenceSerializers
        # # sales inquiry prefence
        # sales_inquiry_preference_data = {
        #     "sales_inquiry": None,
        #     " payment_method": request.data.get("payment_method_id"),
        #     "prev_experience": request.data.get("prev_experience"),
        #     "preffered_date": request.data.get("preffered_date"),
        #     "no_of_hunters": request.data.get("no_of_hunters"),
        #     "no_of_observers": request.data.get("no_of_observers"),
        #     "no_of_days": request.data.get("no_of_days"),
        #     "no_of_companions": request.data.get("no_of_companions"),
        #     "special_requests": request.data.get("special_requests"),
        #     "budget_estimation": request.data.get("budget_estimation"),
        #     "accommodation_type": request.data.get("accommodation_type"),
        # }

        # # GetSalesInquirySerializers

        # with transaction.atomic():
        #     saved_entity = entity_serializer.save()
        #     sales_inquiry_data["entity"] = saved_entity.id
        #     entity_category_data["entity"] = saved_entity.id

        #     seles_inquiry_serializer = CreateEntityCategorySerializers(
        #         data=sales_inquiry_data
        #     )
        #     entity_category_serializer = CreateEntityCategorySerializers(
        #         data=entity_category_data
        #     )
        #     if (
        #         not seles_inquiry_serializer.is_valid()
        #         or entity_category_serializer.is_valid()
        #     ):
        #         enity = Entity.objects.get(id=saved_entity.id)
        #         enity.delete()
        #         return Response(
        #             seles_inquiry_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        #         )
        #     entity_category_serializer.save()
        #     saved_seles_inquiry = seles_inquiry_serializer.save()

        #     sales_inquiry_preference_data["sales_inquiry"] = saved_seles_inquiry.id

        #     sales_inquiry_preference_serializer = (
        #         CreateSalesIquiryPreferenceSerializers(
        #             data=sales_inquiry_preference_data
        #         )
        #     )
        #     if not sales_inquiry_preference_serializer.is_valid():
        #         enity = Entity.objects.get(id=saved_entity.id)
        #         salesInquiry = SalesInquiry.objects.get(id=saved_seles_inquiry.id)

        #         enity.delete()
        #         salesInquiry.delete()

        #     sales_inquiry_preference_serializer.save()
        #     return Response(
        #         {
        #             "message": "Sales Inquiry created successfully",
        #         },
        #         status=status.HTTP_201_CREATED,
        #     )

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
