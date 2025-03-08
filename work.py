#Work
#Backend part of the assignment
#DJANGO BACKEND

from rest_framework import viewsets
from .models import SustainabilityAction
from .serializers import SustainabilityActionSerializer
import json
import os
from django.conf import settings

class SustainabilityActionViewSet(viewsets.ModelViewSet):
    queryset = SustainabilityAction.objects.all()
    serializer_class = SustainabilityActionSerializer

    def perform_create(self, serializer):                            #creating meathod to save to json 
        instance = serializer.save()
        self.save_to_json()

    def perform_update(self, serializer):                           #updating meathod to save to json
        instance = serializer.save()
        self.save_to_json()

    def perform_destroy(self, instance):                             #destroying meathod
        instance.delete()
        self.save_to_json()

    def save_to_json(self):                                         #here we save the objects in "SustainabilityActionViewSet" to json
        actions = SustainabilityAction.objects.all()
        data = SustainabilityActionSerializer(actions, many=True).data
        json_file_path = os.path.join(settings.BASE_DIR, 'actions.json')
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)



#Front end part of the assignment
#PYTHON FRONT END

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:8000/api/actions/'   #base URL of the API

def get_actions():                       #retrieving all  sustainability actions from API
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("Actions:")
        actions = response.json()
        for action in actions:
            print(f"ID: {action['id']}, Action: {action['action']}, Date: {action['date']}, Points: {action['points']}")
    else:
        print(f"Error: {response.status_code}")

def add_action(action, date, points):       #adding a new sustainability action to the API
    data = {'action': action, 'date': date, 'points': points}
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        print("Action added successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def update_action(action_id, action, date, points):   #updating an existing sustainability action in the API
    data = {'action': action, 'date': date, 'points': points}
    response = requests.put(f"{BASE_URL}{action_id}/", json=data)
    if response.status_code == 200:
        print("Action updated successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def delete_action(action_id):    #deleting from API
    response = requests.delete(f"{BASE_URL}{action_id}/")
    if response.status_code == 204:
        print("Action deleted successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")
