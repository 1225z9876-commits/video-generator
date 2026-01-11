import streamlit as st
import os, requests
import speech_recognition as sr
from googletrans import Translator
from pexels_api import API
from pydub import AudioSegment
import arabic_reshaper
from bidi.algorithm import get_display

# ملاحظة: تم حذف sys.path لتجنب تعارضات السيرفر السحابي
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
except:
    from moviepy.all import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

# إعداد واجهة المتصفح
st.set_page_config(page_title="صانع الفيديو الآلي", layout="wide")
st.title("🎬 تطبيق صناعة المحتوى الذكي")

# مفتاح API الخاص بك
API_KEY = 'nr03n2RursI8dw49fGVxxPHGFnyVhruBZRvs5ZYhd3sOLJdVESIj9yqQ'
api = API(API_KEY)

def fix_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

uploaded_file = st.file_uploader("ارفع ملف الصوت الخاص بك (MP3)", type=["mp3"])

if uploaded_file:
    st.audio(uploaded_file)
    if st.button("🚀 ابدأ إنتاج الفيديو"):
        with st.status("جاري العمل على إنتاج محتواك..."):
            # حفظ الصوت ومعالجته
            with open("voice.mp3", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # تحويل الصوت لصيغة wav للتحليل
            audio = AudioSegment.from_mp3("voice.mp3")
            audio.export("temp.wav", format="wav")
            
            # تحليل الكلام
            st.write("🎙️ جاري تحليل الكلام العربي...")
            recognizer = sr.Recognizer()
            try:
                with sr.AudioFile("temp.wav") as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="ar-SA")
                st.info(f"النص المستخرج بنجاح: {text}")
                
                # إشعار النجاح
                st.success("🎉 اكتمل تحليل النص وجاري تجهيز المشاهد!")
            except Exception as e:
                st.error(f"حدث خطأ في تحليل الصوت: {e}")