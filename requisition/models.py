from django.db import models
from django.contrib.auth.models import User

from approval_chain.models import ApprovalChainLevels, ApprovalChainModule
from bm_hunting_settings.models import Currency

# approval_chain_modules(id,name,descriptions,active)
# approval_chains(id,approval_chain_module_id,user_id,approval_chain_level_id)
# approval_chain_roles(id, name, past)
# approval_chain_levels(id,approval_chain_module_id,can_change_source,position_id,approval_chain_role_id,level_id,status)
# requisitions(id,user_id,requested_by,approval_chain_module_id,level_id,type['GAME_REQ','GENERAL'],date,required_date,status,remarks,is_printed)
# requisition_item_sources(id,requisition_id,type['CASH','STORE','VENDOR'],payee,currency_id,account_id,mode_of_payment['CASH', 'TT', 'CREDIT'])
# requisition_items(id,requisition_id,remarks)
# requisition_item_items(id,item_id,currency_id,exchange_rate,unit_of_measurement_id,requisition_item_id,quantity,rate,descriptions)
# requisition_item_accounts(id,requisition_item_id,account_id,currency_id,exchange_rate,amount,descriptions)


class Requisition(models.Model):
    TYPE = (
        ("GAME_REQ", "Game Requisition"),
        ("GENERAL", "General Requisition"),
    )

    STATUS = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requested_by"
    )
    approval_chain_module = models.ForeignKey(
        ApprovalChainModule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="requisition_module",
    )
    level = models.ForeignKey(ApprovalChainLevels, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE)
    date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    status = models.CharField(max_length=255, choices=STATUS)
    remarks = models.TextField()
    is_printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisitions"
        db_table = "requisitions"

    def __str__(self):
        return self.type


class RemarksHistory(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisition Remarks History"
        db_table = "requisition_remarks_history"

    def __str__(self):
        return self.requisition.type


class RequestItemSource(models.Model):
    TYPE = (("CASH", "Cash"), ("STORE", "Store"), ("VENDOR", "Vendor"))
    MODEL_OF_PAYMENT = (
        ("CASH", "Cash"),
        ("TT", "TT"),
        ("CREDIT", "Credit"),
    )
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE)
    payee = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account = models.CharField(max_length=255)
    mode_of_payment = models.CharField(max_length=255, choices=MODEL_OF_PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisition Item Sources"
        db_table = "requisition_item_sources"

    def __str__(self):
        return self.type


class RequestItem(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisition Items"
        db_table = "requisition_items"

    def __str__(self):
        return self.requisition.type


class RequestItemItems(models.Model):
    item = models.ForeignKey(
        RequestItem, on_delete=models.CASCADE, related_name="item_items_set"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measurement = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisition Item Items"
        db_table = "requisition_item_items"

    def __str__(self):
        return self.item.requisition.type


class RequestItemAccount(models.Model):
    requisition_item = models.ForeignKey(RequestItem, on_delete=models.CASCADE)
    account = models.CharField(max_length=255)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Requisition Item Accounts"
        db_table = "requisition_item_accounts"

    def __str__(self):
        return self.requisition_item.item.requisition.type
