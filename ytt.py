import random
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

def VideoTranscription():
    st.title('Youtube Transcribtion Tool.')
    st.write("Put your YouTube video URL in the box below.")
    textInput = st.text_input('', '')
    transcribe_button = st.button('Transcribe!')

    if transcribe_button:
        # Put the URL into a list for consistency
        video_urls = [textInput]
        
        # Extract video ID for each URL in the list
        video_ids = [url.split('v=')[-1] for url in video_urls if 'v=' in url]
        
        if not video_ids:
            st.write("Invalid YouTube URL.")
            return
        
        video_id = video_ids[0]  # Using the first video ID for transcription

        # Get transcript
        try:
            transcribe = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['ar', 'en'])
        except Exception as e:
            st.write(f"Error retrieving transcript: {e}")
            return

        # Format the transcript
        formatter = TextFormatter()
        Format_txt = formatter.format_transcript(transcribe)

        # Generate and save a random file number
        fileNumber = random.randint(1, 1000)
        savedNumber = str(fileNumber)
        
        # Save the transcript to a file
        file_path = f'format_{savedNumber}.txt'
        with open(file_path, 'w', encoding='UTF-8') as text_file:
            text_file.write(Format_txt)

        # Save the file number for tracking
        with open('file_tracker.txt', 'a', encoding='UTF-8') as tracker_file:
            tracker_file.write(f'fileNumber: {savedNumber}, fileName: format_{savedNumber}.txt\n')

        # Display the saved file information on the page
        #st.write(f"Transcript saved as format_{savedNumber}.txt with file number: {savedNumber}")

        # Read and display the file content on the page
        with open(file_path, 'r', encoding='UTF-8') as text_file:
            file_content = text_file.read()
            st.write("**Transcript Content:**")
            
            # Display the transcript in a text area with a hidden label
            st.text_area("Transcript (for accessibility)", value=file_content, height=300, key="transcript", label_visibility='hidden')

        # Copy Transcript functionality
        st_copy_to_clipboard(file_content)
    else:
        st.write('Click the button to start transcription.')

# Call the function in your Streamlit app
VideoTranscription()