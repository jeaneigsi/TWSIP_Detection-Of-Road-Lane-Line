import time
from keras.models import load_model
from moviepy.editor import VideoFileClip
import tempfile
import os
import streamlit as st
from application import Lanes, road_lines
from streamlit_option_menu import option_menu

st.cache_data.clear()

# Barre latérale
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Principal",
        options=["Simuler"],
    )
    st.markdown(""" 
                <style>
                .st-emotion-cache-6qob1r{
                    background: #F5A21F!important;
                    color: #ffffff!important;              
                }
                </style>""", unsafe_allow_html=True)
if selected == "Simuler":
    # Titre et sous-titre
    st.title('Détection de voies par apprentissage automatique :parrot:')
    st.subheader('Ceci est une application web simple pour détecter les voies dans une vidéo à l\'aide d\'un modèle d\'apprentissage automatique.', divider='blue')

    # Instruction pour uploader une vidéo
    st.write('Pour commencer, téléchargez un fichier vidéo et cliquez sur le bouton ci-dessous pour démarrer le processus de détection de voies.')

    uploaded_file = st.file_uploader("Choisir une vidéo...", type="mp4")
    st.subheader("Voici quelques exemples de vidéos pour tester le modèle de détection de voies.")

     # Ajouter la première vidéo
    st.write('Exemple 1:')
    video_file1 = open('project_video.mp4', 'rb')
    video_bytes1 = video_file1.read()
    st.video(video_bytes1)
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        st.markdown('Vidéo téléchargée avec succès!')

        if st.button('Commencer la détection de voies'):
            # Nettoyer le fichier result.mp4
            if os.path.exists('result.mp4'):
                os.remove('result.mp4')
            st.write('Détection de voies en cours...')
            
            # Convertir le format brut en objet de clip vidéo
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Charger la vidéo à partir du fichier temporaire
            video_bytes = VideoFileClip(temp_file_path)
            
            # Charger le modèle Keras
            model = load_model('full_CNN_model.h5')
            
            # Créer l'objet voies
            lanes = Lanes()
            
            # Vidéo de sortie
            vid_output = 'result.mp4'

            # Barre de progression
            progress_text = "Opération en cours. Veuillez patienter. Cela peut prendre un certain temps..."
            my_bar = st.progress(0, text=progress_text)
        
            # Clip vidéo
            vid_clip = video_bytes.fl_image(road_lines)
            vid_clip.write_videofile(vid_output, audio=False)
            os.remove(temp_file_path)

            # Afficher la vidéo
            vid_file = open('result.mp4', 'rb')
            vid_bytes = vid_file.read()
            st.markdown('Détection de voies terminée!')
            st.video(vid_bytes)

    else:
        st.markdown('**:blue[Veuillez télécharger un fichier vidéo]**.')
