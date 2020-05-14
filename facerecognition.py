import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

def similarFaces():
	# Detect the faces in an image that contains multiple faces
	# Each detected face gets assigned a new ID
	multi_face_image_url = "http://www.historyplace.com/kennedy/president-family-portrait-closeup.jpg"
	multi_image_name = os.path.basename(multi_face_image_url)
	detected_faces2 = face_client.face.detect_with_url(url=multi_face_image_url)
	# Search through faces detected in group image for the single face from first image.
	# First, create a list of the face IDs found in the second image.
	second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
	# Next, find similar face IDs like the one detected in the first image.
	similar_faces = face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
	if not similar_faces[0]:
		print('No similar faces found in', multi_image_name, '.')
