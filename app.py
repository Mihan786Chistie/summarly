from dotenv import load_dotenv
import google.generativeai as genai
import os
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_PRO_API_KEY"))

prompt = """You are a Youtube video summarizer. 
Given the transcript of a YouTube video, please summarize the main points and key takeaways in a concise and easy-to-understand format. The summary should include:

Introduction: Briefly describe the video's topic or main focus.
Key Points: List the most important information, ideas, or arguments presented in the video.
Conclusion: Summarize any final thoughts, conclusions, or calls to action from the video.

Make sure the summary is clear and accessible, providing a quick yet comprehensive overview of the video's content.

This is the transcrit text:
"""

