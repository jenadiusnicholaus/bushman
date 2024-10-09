from django.shortcuts import render
from rest_framework import viewsets

from hunter.models import Client
from hunter.serializers.clients_docs_sz import (
    CreateClientsDocsSerializer,
    GetClientsDocsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from sales.models import Document


class ClientDocsView(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = GetClientsDocsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        doc_id = self.request.query_params.get("doc_id", None)
        if doc_id:
            try:
                doc_bject = Document.objects.get(id=doc_id)
            except Document.DoesNotExist:
                return Response(
                    {"message": "Document does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(doc_bject)
            return Response(serializer.data)
        queryset = self.queryset.filter(client__user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        doc_forWho = request.data.get("forWho")
        clinet = Client.objects.get(user=request.user)
        if request.data.get("document_type") == "Me":
            doc_forWho = clinet.id

        data = {
            "document_type": request.data.get("document_type"),
            "client": clinet.id,
            "document": request.data.get("document"),
            "uploaded_at": timezone.now(),
            "forWho": doc_forWho,
        }
        serializer = CreateClientsDocsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Document uploaded successfully",
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        doc_forWho = request.data.get("forWho")
        clinet = Client.objects.get(user=request.user)
        if request.data.get("document_type") == "Me":
            doc_forWho = clinet.id
        doc_id = self.request.query_params.get("doc_id", None)

        if not doc_id:
            return Response(
                {"message": "Document id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        doc = Document.objects.get(id=doc_id)
        data = {
            "document_type": request.data.get("document_type", doc.document_type),
            "client": clinet.id,
            "document": request.data.get("document", doc.document),
            "forWho": doc_forWho,
            "updated_at": timezone.now(),
        }

        serializer = CreateClientsDocsSerializer(doc, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Document updated successfully",
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        doc_id = self.request.query_params.get("doc_id", None)
        if not doc_id:
            return Response(
                {"message": "Document id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:

            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            return Response(
                {"message": "Document does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if doc.client.user != request.user:
            return Response(
                {"message": "You are not authorized to delete this document"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        doc.delete()
        return Response(
            {
                "message": "Document deleted successfully",
            },
            status=status.HTTP_200_OK,
        )
