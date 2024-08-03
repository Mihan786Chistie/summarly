from dotenv import load_dotenv
import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# Configure the generative AI API key
genai.configure(api_key=os.getenv("GEMINI_PRO_API_KEY"))

app = Flask(__name__)

# Prompt template for generating the summary
prompt = """You are a Youtube video summarizer. 
Given the transcript of a YouTube video, summarize the content in a clear and detailed manner. Your summary should include the following:

Introduction: Provide a brief overview of the video's main topic or focus, including any relevant context.
Key Points: Identify and elaborate on the most important information, ideas, or arguments presented in the video. Each point should be clearly explained, making it easy for the reader to understand.
Conclusion: Conclude with a summary of the video's final thoughts, conclusions, or calls to action, highlighting the overall message or purpose.
Ensure that the summary is thorough yet concise, capturing the essence of the video in an accessible format.

This is the transcript text:
"""

@app.get("/summary")
def summary_api():
    url = request.args.get("url", '')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        # Decode the URL parameter
        decoded_url = urllib.parse.unquote(url)
        print("Decoded Url: ",decoded_url)
        video_id = decoded_url.split("%")[1]
        transcript = get_transcript(video_id)
        summary = generate_summary(prompt, transcript)
        return jsonify({"summary": summary})
    except (IndexError, VideoUnavailable, NoTranscriptFound) as e:
        # Handle specific errors related to YouTube video ID extraction and transcript retrieval
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle all other unexpected errors
        return jsonify({"error": str(e)}), 500

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([line['text'] for line in transcript_list])
        return transcript
    except NoTranscriptFound as e:
        # Handle the case where the transcript is not available
        raise NoTranscriptFound(f"Transcript not found for video ID: {video_id}")
    except VideoUnavailable as e:
        # Handle the case where the video is unavailable
        raise VideoUnavailable(f"Video unavailable for video ID: {video_id}")
    except Exception as e:
        # Handle all other errors
        raise Exception("Error fetching transcript")

def generate_summary(prompt, transcript):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt + transcript)
        return response.text
    except Exception as e:
        # Handle errors related to the generative AI model
        raise Exception("Error generating summary")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
