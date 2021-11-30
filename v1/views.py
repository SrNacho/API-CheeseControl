from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pymongo import MongoClient
from rest_framework import status
import datetime
import os

from .serializers import LecheSerializer

DB_CFG = os.environ.get('db_cfg')
print(DB_CFG)
client = MongoClient(DB_CFG)
db = client['olimpiadas']
collection_user = db['leche']


class Leche(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LecheSerializer

    def get(self, request):
        results = [x for x in collection_user.find()]
        content = {'results': results}
        return Response(content)

    # FALTA VALIDAR EL POST TODOS LOS CAMPOS, COMO SI LO HICE CON EL UPDATE
    def post(self, request):
        #posted_fields = list(self.request.data.keys())
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        #accepted_fields = ['tambo', 'fecha', 'estado']
        message = []
        all_args_passed = False

        try:
            tambo, fecha, estado = list(self.request.data.values())
            all_args_passed = True
        except:
            general_status = status.HTTP_400_BAD_REQUEST
            message.append(
                "Argumentos insuficientes en la request. Se espera 'tambo', 'fecha', 'estado'")

        #SI LA VERIFICACION NO ANDA DESCOMENTAR LINEAS 45 46 47 30 Y 32
        # Verifica que todos los argumentos hayan sido pasados a la request
        # all_args_passed = all(
        #     item in posted_fields for item in accepted_fields)

        if all_args_passed:
            try:
                datetime.datetime.strptime(fecha, '%d-%m-%Y')  # nopep8 // valida la fecha en el formato DD-MM-YYYY
                if estado.isalnum():
                    try:
                        collection_user.insert_one(
                            {"_id": tambo, 'fecha': fecha, "estado": estado})
                        general_status = status.HTTP_200_OK
                    except:
                        general_status = status.HTTP_400_BAD_REQUEST
                else:
                    general_status = status.HTTP_400_BAD_REQUEST
                    message.append("Estado vacio o con caracteres invalidos")
            except:
                general_status = status.HTTP_400_BAD_REQUEST
                message.append(
                    "Formato de fecha equivocado. Formato aceptado: DD-MM-YYYY")
        if general_status == status.HTTP_200_OK:
            return Response({"status": status.HTTP_200_OK, "message": "OK"})
        else:
            return Response({"status": general_status, "message": message})

    def put(self, request):
        #posted_fields = list(self.request.data.keys())
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        #accepted_fields = ['tambo', 'fecha', 'estado']
        message = []
        all_args_passed = False

        try:
            tambo, fecha, estado = list(self.request.data.values())
            all_args_passed = True
        except:
            general_status = status.HTTP_400_BAD_REQUEST
            message.append(
                "Argumentos insuficientes en la request. Se espera 'tambo', 'fecha', 'estado'")


        #SI LA VERIFICACION NO ANDA DESCOMENTAR LINEAS 88 89 90 72 Y 74
        # Verifica que todos los argumentos hayan sido pasados a la request
        # all_args_passed = all(
        #     item in posted_fields for item in accepted_fields)

        if all_args_passed:
            try:
                datetime.datetime.strptime(fecha, '%d-%m-%Y')  # nopep8 // valida la fecha en el formato DD-MM-YYYY
                if estado.isalnum():
                    try:
                        collection_user.update_one(
                            {"_id": tambo}, {"$set": {'fecha': fecha, "estado": estado}})
                        general_status = status.HTTP_200_OK
                        message.append("OK")
                    except Exception as ex:
                        print(ex)
                        general_status = status.HTTP_400_BAD_REQUEST
                        message.append("Unknown error")
                else:
                    general_status = status.HTTP_400_BAD_REQUEST
                    message.append("Estado vacio o con caracteres invalidos")
            except:
                general_status = status.HTTP_400_BAD_REQUEST
                message.append(
                    "Formato de fecha equivocado. Formato aceptado: DD-MM-YYYY")

        if general_status == status.HTTP_200_OK:
            return Response({"status": general_status, "message": message})
        else:
            return Response({"status": general_status, "message": message})

    def delete(self, request):
        posted_fields = list(self.request.data.keys())
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        accepted_fields = ['tambo']
        message = []

        try:
            tambo = list(self.request.data.values())
        except:
            general_status = status.HTTP_400_BAD_REQUEST
            message.append(
                "Argumentos insuficientes en la request. Se espera 'tambo', 'fecha', 'estado'")
