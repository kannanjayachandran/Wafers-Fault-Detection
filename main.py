from wsgiref import simple_server
from flask_cors import CORS, cross_origin
from flask import Flask, request, render_template, Response
import json
import os
from Prediction_validation import PredictionValidation
from Training_Model import TrainModel
from Training_Validation_Insertion import Train_Validation
from Prediction_model import Prediction

