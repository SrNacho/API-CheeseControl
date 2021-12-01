from django.shortcuts import render
from pymongo import MongoClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import datetime
import os
import shortuuid

DB_CFG = os.environ.get('db_cfg')

client = MongoClient(DB_CFG)
db = client['olimpiadas']
collection_leche = db['leche']
collection_curado = db['curado']


class Leche(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        results = [x for x in collection_leche.find()]
        if results:
            return Response({'status': status.HTTP_200_OK, 'results': results})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': ["Base de datos vacia"]})

    def post(self, request):
        posted_fields = list(self.request.data.keys())
        posted_values = list(self.request.data.values())
        accepted_fields = ['tambo', 'fecha', 'estado']
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        message = []

        # Verifica que todos los argumentos hayan sido pasados a la request
        all_args_passed_check = True if all(
            item in posted_fields for item in accepted_fields) else message.append(
                "Argumentos insuficientes en la request. Se espera 'tambo', 'fecha', 'estado'")

        if all_args_passed_check:
            try:
                tambo, fecha, estado = posted_values
                datetime.datetime.strptime(fecha, '%d-%m-%Y')  # nopep8 // valida la fecha en el formato DD-MM-YYYY
                if estado.isalnum():
                    try:
                        collection_leche.insert_one(
                            {"_id": tambo, 'fecha': fecha, "estado": estado})
                        general_status = status.HTTP_200_OK
                    except:
                        general_status = status.HTTP_400_BAD_REQUEST
                        message.append("ID del TAMBO ya existente")
                else:
                    general_status = status.HTTP_400_BAD_REQUEST
                    message.append("Estado vacio o con caracteres invalidos")
            except:
                general_status = status.HTTP_400_BAD_REQUEST
                message.append(
                    "Formato de fecha equivocado. Formato aceptado: DD-MM-YYYY")
        if general_status == status.HTTP_200_OK:
            return Response({"status": status.HTTP_200_OK, "message": "OK", "result": {"_id": tambo, 'fecha': fecha, "estado": estado}})
        else:
            return Response({"status": general_status, "message": message})

    def put(self, request):
        posted_fields = list(self.request.data.keys())
        posted_values = list(self.request.data.values())
        accepted_fields = ['tambo', 'fecha', 'estado']
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        message = []

        # Verifica que todos los argumentos hayan sido pasados a la request
        all_args_passed_check = True if all(
            item in posted_fields for item in accepted_fields) else message.append(
                "Argumentos insuficientes en la request. Se espera 'tambo', 'fecha', 'estado'")

        if all_args_passed_check:
            try:
                tambo, fecha, estado = posted_values
                datetime.datetime.strptime(fecha, '%d-%m-%Y')  # nopep8 // valida la fecha en el formato DD-MM-YYYY
                if estado.isalnum():
                    try:
                        collection_leche.update_one(
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
            return Response({"status": general_status, "message": message, "result": {"_id": tambo, 'fecha': fecha, "estado": estado}})
        else:
            return Response({"status": general_status, "message": message})

    def delete(self, request):
        posted_fields = list(self.request.data.keys())
        id = list(self.request.data.values())[0]
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        accepted_fields = ['tambo']
        message = []

        all_args_passed = True if all(
            item in posted_fields for item in accepted_fields) else message.append("Argumentos esperados: 'tambo'")

        exists = [x for x in collection_leche.find({'_id': id})]
        if all_args_passed and exists:
            collection_leche.delete_one({'_id': id})
            general_status = status.HTTP_200_OK
        else:
            general_status = status.HTTP_400_BAD_REQUEST
            message.append("El registro no existe")

        if general_status == status.HTTP_200_OK:
            return Response({"status": general_status, "message": message})
        else:
            return Response({"status": general_status, "message": message})


class Curado(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        results = [x for x in collection_curado.find()]
        print()
        if results:
            return Response({"status": status.HTTP_200_OK, "results": results})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, "message": ["Base de datos vacia"]})

    def post(self, request):
        posted_fields = list(self.request.data.keys())
        posted_values = list(self.request.data.values())
        accepted_fields = ['humedad', 'temperatura', 'co2']
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        message = []

        try:
            max_id = collection_curado.find_one(sort=[("_id", -1)])['_id']
        except:
            max_id = 0
        # Verifica que todos los argumentos hayan sido pasados a la request
        all_args_passed_check = True if all(
            item in posted_fields for item in accepted_fields) else message.append(
                "Argumentos insuficientes en la request. Se espera 'humedad', 'temperatura', 'co2'")

        if all_args_passed_check:
            try:
                print(posted_values)
                humedad, temperatura, co2 = posted_values
                try:
                    int(humedad)
                    try:
                        int(temperatura)
                        try:
                            int(co2)
                            general_status = status.HTTP_200_OK
                            collection_curado.insert_one(
                                {'_id': max_id+1, 'humedad': humedad, 'temperatura': temperatura, 'co2': co2})
                        except:
                            general_status: status.HTTP_400_BAD_REQUEST
                            message.append("CO2 debe ser numerico")
                    except:
                        general_status: status.HTTP_400_BAD_REQUEST
                        message.append("TEMPERATURA debe ser numerico")
                except:
                    general_status: status.HTTP_400_BAD_REQUEST
                    message.append("HUMEDAD debe ser numerico")
            except Exception as e:
                print(e)
                general_status = status.HTTP_400_BAD_REQUEST
                message.append(
                    "Formato de fecha equivocado. Formato aceptado: DD-MM-YYYY")
        if general_status == status.HTTP_200_OK:
            return Response({"status": status.HTTP_200_OK, "message": "OK", "result": {'_id': max_id+1, 'humedad': humedad, 'temperatura': temperatura, 'co2': co2}})
        else:
            return Response({"status": general_status, "message": message})

    def put(self, request):
        posted_fields = list(self.request.data.keys())
        posted_values = list(self.request.data.values())
        accepted_fields = ['id', 'humedad', 'temperatura', 'co2']
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        message = []

        # Verifica que todos los argumentos hayan sido pasados a la request
        all_args_passed_check = True if all(
            item in posted_fields for item in accepted_fields) else message.append(
                "Argumentos insuficientes en la request. Se espera 'id', humedad', 'temperatura', 'co2'")

        if all_args_passed_check:
            try:
                print(posted_values)
                id, humedad, temperatura, co2 = posted_values
                try:
                    int(id)
                    exists = [x for x in collection_curado.find({'_id': id})]
                    if exists:
                        try:
                            int(humedad)
                            try:
                                int(temperatura)
                                try:
                                    int(co2)
                                    try:
                                        general_status = status.HTTP_200_OK
                                        collection_curado.update_one(
                                            {'_id': id}, {'$set': {'humedad': humedad, 'temperatura': temperatura, 'co2': co2}})
                                    except:
                                        general_status: status.HTTP_400_BAD_REQUEST
                                        message.append("No existe el registro")
                                except:
                                    general_status: status.HTTP_400_BAD_REQUEST
                                    message.append("CO2 debe ser numerico")
                            except:
                                general_status: status.HTTP_400_BAD_REQUEST
                                message.append("TEMPERATURA debe ser numerico")
                        except:
                            general_status: status.HTTP_400_BAD_REQUEST
                            message.append("HUMEDAD debe ser numerico")
                    else:
                        general_status: status.HTTP_400_BAD_REQUEST
                        message.append(
                            "No existe el registro con ID {}".format(id))
                except:
                    general_status: status.HTTP_400_BAD_REQUEST
                    message.append("ID debe ser numerico")
            except Exception as e:
                print(e)
                general_status = status.HTTP_400_BAD_REQUEST
                message.append(
                    "Formato de fecha equivocado. Formato aceptado: DD-MM-YYYY")
        if general_status == status.HTTP_200_OK:
            return Response({"status": status.HTTP_200_OK, "message": "OK", 'result': {'_id': id, 'humedad': humedad, 'temperatura': temperatura, 'co2': co2}})
        else:
            return Response({"status": general_status, "message": message})

    def delete(self, request):
        posted_fields = list(self.request.data.keys())
        id = list(self.request.data.values())[0]
        general_status = status.HTTP_400_BAD_REQUEST  # nopep8 // Status general, puede ser 200 o 400
        accepted_fields = ['id']
        message = []

        all_args_passed = True if all(
            item in posted_fields for item in accepted_fields) else message.append("Argumentos esperados: 'id'")

        exists = [x for x in collection_curado.find({'_id': id})]
        if all_args_passed and exists:
            collection_curado.delete_one({'_id': id})
            general_status = status.HTTP_200_OK
        else:
            general_status = status.HTTP_400_BAD_REQUEST
            message.append("El registro no existe")

        if general_status == status.HTTP_200_OK:
            return Response({"status": general_status, "message": message})
        else:
            return Response({"status": general_status, "message": message})
