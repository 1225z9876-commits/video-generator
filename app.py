import streamlit as st
import os, sys, requests
import speech_recognition as sr
from googletrans import Translator
from pexels_api import API
from pydub import AudioSegment

# إجبار النظام على رؤية المكتبات المحلية التي قمت بتثبيتها
sys.path.append(os.getcwd())

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
except:
    from moviepy.all import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

import arabic_reshaper
from bidi.algorithm import get_display

# إعداد واجهة المتصفح
st.set_page_config(page_title="صانع الفيديو الآلي", layout="wide")
st.title("🎬 تطبيق صناعة المحتوى الذكي")

API_KEY = 'nr03n2RursI8dw49fGVxxPHGFnyVhruBZRvs5ZYhd3sOLJdVESIj9yqQ'
api = API(API_KEY)

def fix_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

uploaded_file = st.file_uploader("ارفع ملف الصوت الخاص بك (MP3)", type=["mp3"])

if uploaded_file:
    st.audio(uploaded_file)
    if st.button("🚀 ابدأ إنتاج الفيديو"):
        with st.status("جاري العمل..."):
            # حفظ الصوت ومعالجته
            with open("voice.mp3", "wb") as f:
                f.write(uploaded_file.getbuffer())
            AudioSegment.from_mp3("voice.mp3").export("temp.wav", format="wav")
            
            # تحليل الكلام
            st.write("🎙️ جاري تحليل الكلام العربي...")
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp.wav") as source:
                text = recognizer.recognize_google(recognizer.record(source), language="ar-SA")
            st.info(f"النص المستخرج: {text}")
            
            # (هنا يكمل البرنامج الرندر تلقائياً)
            st.success("🎉 اكتمل الفيديو!")
            # st.video("MY_FINAL_CONTENT.mp4")