
#! Face Detection : Face Image -> Face Detector (using dlib) -> Detected landmarks(68 points which read face using Shape Predictor[sp]) -> ResNet(Convert into 128D embedding using facerec which is store in DB)
#! Face Recognition :  Face Image -> ResNet(feature extraction) -> 128D embedding(face description) -> SVM Classifier -> Student ID

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

@st.cache_resource #! to prevent reloading of models on every interaction, it will load only once and cache the result for future use
def load_dlib_models():
    face_detector = dlib.get_frontal_face_detector() 
    shape_predictor = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    face_rec_model = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return face_detector, shape_predictor, face_rec_model

def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
        faces = detector(image_np, 1) #! detect faces in the image, (1)no. of times to processing(invert,magnified...) the image for better detection but it consume high CPU
        if len(faces) == 0:
            return None
        
        encoding = []
        for face in faces:
            shape = sp(image_np, face) #! get the 68 landmarks of the detected 
            face_descriptor = facerec.compute_face_descriptor(image_np, shape,1) #! return embedding of the face 128D
            encoding.append(np.array(face_descriptor)) #! pass in numpy for easy calculating 
        return encoding
    except Exception as e:
        print(e)


@st.cache_resource 
def get_trained_model(): 
    # SVM Classifier used to identify the student based on the face embedding, it take 2 parameters X(all student embeddings) and Y(all student_id)
    x=[] 
    y=[] 
    student_db = get_all_students() #! get all students from DB  

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding') #! embedding stored in DB as string, we need to convert it back to numpy array
        if embedding is not None:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))
    
    if len(x) == 0:
        return None

    clf = SVC(kernel='linear', probability=True,class_weight='balanced') 
    try:
        clf.fit(x,y) 
    except ValueError as e:
        pass
    return {"clf":clf,"x":x,"y":y}

def train_classifier(): #! we clear cache when new student register or update their face data for better accuracy
    st.cache_resource.clear()  #st.cache_resource.clear(get_trained_model)
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np): #! class picture in numpy array format
    
    encodings = get_face_embeddings(class_image_np)
    detected_students = {} 
    model_data = get_trained_model()
    if not model_data:
       #return detected_students, [], None  
       return detected_students, [], len(encodings) # original but error using this 
    
   
    clf = model_data['clf']
    x_train=model_data['x']
    y_train=model_data['y']
    
    all_students = sorted(list(set(y_train))) 

    for encoding in encodings:
        if len(all_students) >=2:
            predicted_id = int(clf.predict([encoding])[0]) #! predict return array of predicted labels,
        else:
            predicted_id = int(all_students[0])
        
        student_embedding = x_train[y_train.index(predicted_id)] #! get the embedding of the predicted student from training data
        best_match_score = np.linalg.norm(student_embedding - encoding) #! calculate the distance between the predicted student embedding and the detected face embedding, lower score means better match

        resemblance_threshold = 0.6 
        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)
