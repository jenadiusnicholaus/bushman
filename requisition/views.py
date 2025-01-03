from rest_framework import viewsets

from approval_chain.models import ApprovalChainLevels, ApprovalChainModule
from approval_chain.serializers import GetApprovalChainLevelsSerializer
from .models import RequestItem, Requisition, RequisitionApprovalStatus
from .serializers import (
    CreateRemarksHistorySerializer,
    CreateRequestItemAccountsSerializer,
    CreateRequestItemItemsSerializer,
    CreateRequestItemSerializer,
    CreateRequestItemSourceSerializer,
    CreateRequisitionApprovalStatusSerializer,
    CreateRequisitionSerializer,
    GetRequestItemSerializer,
    GetRequisitionSerializer,
    UpdateRequisitionApprovalStatusSerializer,
    UpdateRequisitionSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class RequisitionVewSet(viewsets.ModelViewSet):
    serializer_class = GetRequisitionSerializer
    queryset = Requisition.objects.filter().order_by("-created_at")
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # we need to save this
        # CreateRequisitionSerializer

        stattus = "PENDING"
        level_number = 1
        level_id = request.data.get("level_id")
        _db_level_id = None

        if level_id is None:
            try:
                alevel = ApprovalChainLevels.objects.get(level_number=level_number)
                level_id = alevel.id
            except ApprovalChainLevels.DoesNotExist:
                pass

        requistion_data = {
            "user": request.user.id,
            "requested_by": request.user.id,
            "approval_chain_module": request.data.get("approval_chain_module_id"),
            "level": level_id,
            "type": request.data.get("type"),
            "date": request.data.get("date"),
            "required_date": request.data.get("required_date"),
            "status": stattus,
            "remarks": request.data.get("remarks"),
        }

        # get number of  approval chain present for approval_chain_module_id,
        #  and check the level number provided if number provided is the highest level number present in the approval chain,
        # then save requuistion approved else make it pending and send notification to the next approver.
        #  then create the requisition, else return error message

        approval_chain_module_id = request.data.get("approval_chain_module_id")
        try:
            approval_chain_module = ApprovalChainModule.objects.get(
                id=approval_chain_module_id
            )
        except ApprovalChainModule.DoesNotExist:
            return Response(
                {"message": "Approval chain module not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            approval_chain_level = ApprovalChainLevels.objects.get(
                approval_chain_module=approval_chain_module, id=level_id
            )
        except ApprovalChainLevels.DoesNotExist:
            return Response(
                {"message": "Approval chain not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # The level numbers are sequential, such as 1, 2, 3, 4, etc.
        # A higher number indicates that the requisition has been approved.
        # We need to determine the position of the number in the list of levels from [approval_chain_module] using the given level_id.
        # If the level_id is at the last position, we will mark the requisition as approved; otherwise, we will set it to pending and notify the next approver.
        # Then, we will create the requisition; if not, we will return an error message.

        levels = approval_chain_module.levels.all()
        if len(levels) == 0:
            return Response(
                {"message": "Approval chain not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        provided_level_position = approval_chain_level.level_number

        # if the provode numer is greater than or equal all the available level number in the approval chain, then status is Aprrove coz it is the highest level number
        # get the highest level number in the approval chain
        _max = levels.aggregate(Max("level_number"))["level_number__max"]
        if provided_level_position >= _max:
            stattus = "APPROVED"
        else:
            stattus = "PENDING"

        requistion_data["status"] = stattus

        level_status_data = {
            "requisition": None,
            "level": level_id,
            "status": stattus,
            "user": request.user.id,
        }

        with transaction.atomic():
            r_serializer = CreateRequisitionSerializer(data=requistion_data)

            if not r_serializer.is_valid():
                return Response(r_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            saved_requisition = r_serializer.save()

            level_status_data["requisition"] = saved_requisition.id
            level_status_sz = CreateRequisitionApprovalStatusSerializer(
                data=level_status_data
            )
            if not level_status_sz.is_valid():
                return Response(
                    level_status_sz.errors, status=status.HTTP_400_BAD_REQUEST
                )

            level_status_sz.save()

            return Response(
                {
                    "message": "Requisition created successfully",
                    "data": {
                        "requisition": saved_requisition.id,
                        "level_status": level_status_sz.data,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

    def put(self, request, *args, **kwargs):
        # update the requisition
        requisition_id = request.data.get("requisition_id")
        level_id = request.data.get("level_id")
        remarks = request.data.get("remarks")
        _status = request.data.get("status")
        try:
            requisition = Requisition.objects.get(id=requisition_id)
        except Requisition.DoesNotExist:
            return Response(
                {"message": "Requisition not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            approval_chain_module = ApprovalChainModule.objects.get(
                id=requisition.approval_chain_module.id
            )
        except ApprovalChainModule.DoesNotExist:
            return Response(
                {"message": "Approval chain module not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            approval_chain_level = ApprovalChainLevels.objects.get(
                approval_chain_module=approval_chain_module, id=level_id
            )
        except ApprovalChainLevels.DoesNotExist:
            return Response(
                {"message": "Approval chain not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        levels = approval_chain_module.levels.all()
        if len(levels) == 0:
            return Response(
                {"message": "Approval chain not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # check is already aproved or Rejected
        if requisition.status == "APPROVED":
            return Response(
                {"message": "Requisition already approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if requisition.status == "REJECTED":
            return Response(
                {
                    "message": "Requisition already rejected",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        main_status = None
        if _status == "APPROVED" or _status == "REJECTED":
            main_status = _status
        else:
            main_status = "PENDING"

        requistion_data = {
            "status": main_status,
            "level": approval_chain_level.id,
        }
        requisition_level_status_data = {
            "requisition": requisition.id,
            "status": _status,
            "level": approval_chain_level.id,
            "user": request.user.id,
        }

        status_level, _ = RequisitionApprovalStatus.objects.get_or_create(
            requisition=requisition, level=approval_chain_level, user=request.user
        )

        with transaction.atomic():

            update_sz = UpdateRequisitionSerializer(
                instance=requisition, data=requistion_data, partial=True
            )
            if not update_sz.is_valid():
                return Response(update_sz.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_requisition = update_sz.save()

            requisition_level_status_sz = UpdateRequisitionApprovalStatusSerializer(
                instance=status_level, data=requisition_level_status_data, partial=True
            )
            if not requisition_level_status_sz.is_valid():
                return Response(
                    requisition_level_status_sz.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            requisition_level_status_sz.save()

            remarks = CreateRemarksHistorySerializer(
                data={
                    "requisition": requisition.id,
                    "user": request.user.id,
                    "remarks": remarks,
                }
            )
            if not remarks.is_valid():
                return Response(remarks.errors, status=status.HTTP_400_BAD_REQUEST)
            remarks.save()

            levels = approval_chain_module.levels.all()
            if len(levels) == 0:
                return Response(
                    {"message": "Approval chain not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            provided_level_position = approval_chain_level.level_number

            # if the provode numer is greater than or equal all the available level number in the approval chain, then status is Aprrove coz it is the highest level number
            # get the highest level number in the approval chain
            _max = levels.aggregate(Max("level_number"))["level_number__max"]
            if provided_level_position >= _max:
                return Response(
                    {"message": f"Reuistion {_status} successfully"},
                    status=status.HTTP_200_OK,
                )
            else:

                return Response(
                    {"message": "Requisition updated successfully"},
                    status=status.HTTP_200_OK,
                )


class RequisitionItemViewSet(viewsets.ModelViewSet):
    serializer_class = GetRequestItemSerializer
    queryset = RequestItem.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request, *args, **kwargs):
        requisition_id = self.request.query_params.get("requisition_id")
        if requisition_id is not None:
            queryset = self.get_queryset().filter(requisition__id=requisition_id)

        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # create item items for the requisition
        # CreateRequestItemSourceSerializer
        # CreateRequestItemSerializer
        # CreateRequestItemItemsSerializer
        # CreateRequestItemAccountsSerializer

        source_data = {
            "requisition": request.data.get("requisition_id"),
            "type": request.data.get("source_type"),
            "payee": request.data.get("payee"),
            "currency": request.data.get("currency_id"),
            "account": request.data.get("account_id"),
            "mode_of_payment": request.data.get("mode_of_payment_id"),
        }

        item = {
            "name": request.data.get("item_name"),
            "requisition": request.data.get("requisition_id"),
            "remarks": request.data.get("remarks"),
        }

        # requestItemAccount = {
        #     "item": None,
        #     "account": request.data.get("account_id"),
        #     "currency": request.data.get("currency_id"),
        #     "amount": request.data.get("amount"),
        # }

        with transaction.atomic():
            serializer = CreateRequestItemSourceSerializer(data=source_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            saved_source = serializer.save()

            item_sz = CreateRequestItemSerializer(data=item)
            if not item_sz.is_valid():
                saved_source.delete()
                return Response(item_sz.errors, status=status.HTTP_400_BAD_REQUEST)

            saved_item = item_sz.save()

            item_ites = request.data.get("items")
            for item in item_ites:
                item_items_data = {
                    "item": saved_item.id,
                    "name": item.get("name"),
                    "currency": item.get("currency_id"),
                    "exchange_rate": item.get("exchange_rate"),
                    "unit_of_measurement": item.get("unit_of_measurement_id"),
                    "quantity": item.get("quantity"),
                    "rate": item.get("rate"),
                    "descriptions": item.get("descriptions"),
                }
                item_items_sz = CreateRequestItemItemsSerializer(data=item_items_data)
                if not item_items_sz.is_valid():
                    saved_item.delete()
                    saved_source.delete()

                    return Response(
                        item_items_sz.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                item_items_sz.save()

            account_data = {
                "requisition_item": saved_item.id,
                "account": request.data.get("account_id"),
                "currency": request.data.get("currency_id"),
                "amount": request.data.get("amount"),
            }
            account_sz = CreateRequestItemAccountsSerializer(data=account_data)
            if not account_sz.is_valid():
                saved_item.delete()
                saved_source.delete()

                return Response(account_sz.errors, status=status.HTTP_400_BAD_REQUEST)
            account_sz.save()

            return Response(
                {
                    "message": "Requisition item created successfully",
                    "data": {
                        "requisition": request.data.get("requisition_id"),
                        "item": saved_item.id,
                        "requisition_source": saved_source.id,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
