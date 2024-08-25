from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # Get the path to the desktop
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),
                'noplaylist': True  # Ensure only one video is downloaded
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info = ydl.extract_info(url, download=False)
                filename = f"{info['title']}.mp4"
                
            return send_file(os.path.join(desktop_path, filename), as_attachment=True, download_name=filename)

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
