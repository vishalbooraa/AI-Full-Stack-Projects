import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_face_recognition_model():
    detector=dlib.get_frontal_face_detector()
    sp=dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    
    facerec=dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detector,sp,facerec

def get_face_embeddings(image_np):
    detector,sp,facerec=load_face_recognition_model()
    faces=detector(image_np,1)
    embeddings=[]
    for face in faces:
        shape=sp(image_np,face) # 68 landmarks
        face_descriptor=facerec.compute_face_descriptor(image_np,shape,1) # 128D embeddings
        embeddings.append(np.array(face_descriptor))
    return embeddings


@st.cache_resource
def get_trained_model():
    X=[]
    Y=[]

    student_db=get_all_students()
    if not student_db:
        return None
    for student in student_db:
        if student["face_embedding"]:
            X.append(np.array(student["face_embedding"]))
            Y.append(student["student_id"])
    if not X:
        return None
    model=SVC(kernel="linear",probability=True,class_weight="balanced")
    try:
        model.fit(X,Y)
    except:
        return None
    return {"model":model,"X":X,"Y":Y}

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    if model_data:
        st.success("Face recognition model trained successfully!")

def predict_attendance(class_image_np):
    encodings=get_face_embeddings(class_image_np)
    detected_students={}
    model_data=get_trained_model()
    if not model_data:
        st.warning("No trained model available. Please train the model first.")
        return detected_students,[],len(encodings)
    model=model_data["model"]
    X_train=model_data["X"]
    Y_train=model_data["Y"]

    all_students=sorted(list(set(Y_train)))

    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id=model.predict([encoding])[0]
        else:
            predicted_id=int(all_students[0])
        
        student_embeddings=X_train[Y_train.index(predicted_id)]
        distance=np.linalg.norm(student_embeddings-encoding)
        if distance<0.6:
            detected_students[predicted_id]=True
    return detected_students,all_students,len(encodings)