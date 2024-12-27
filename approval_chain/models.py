from django.db import models
from django.contrib.auth.models import User


class ApprovalChainModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Approval Chain Modules"
        db_table = "approval_chain_modules"

    def __str__(self):
        return self.name


class ApprovalChainRole(models.Model):
    PAST = (
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    )

    name = models.CharField(max_length=255, unique=True)
    past = models.CharField(choices=PAST, default="APPROVED", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Approval Chain Roles"
        db_table = "approval_chain_roles"

    def __str__(self):
        return self.name


class ApprovalChainLevels(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("VISITED", "Completed"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )
    approval_chain_module = models.ForeignKey(
        ApprovalChainModule, on_delete=models.CASCADE, related_name="levels"
    )
    can_change_source = models.BooleanField(default=False)
    position = models.CharField(max_length=255, null=True, blank=True)
    level_number = models.IntegerField(null=True, blank=True, default=1)
    approval_chain_role = models.ForeignKey(ApprovalChainRole, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255, choices=STATUS, null=True, blank=True, default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Approval Chain Levels"
        db_table = "approval_chain_levels"
        unique_together = ("approval_chain_module", "approval_chain_role")

    def __str__(self):
        return self.approval_chain_module.name + " - " + self.approval_chain_module.name


class ApprovalChain(models.Model):
    approval_chain_module = models.ForeignKey(
        ApprovalChainModule, on_delete=models.CASCADE, related_name="chains"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approval_chain_level = models.ForeignKey(
        ApprovalChainLevels, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Approval Chains"
        db_table = "approval_chains"

    def __str__(self):
        return (
            self.user.username
            + " - "
            + self.approval_chain_level.approval_chain_module.name
        )
