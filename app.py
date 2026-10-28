from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return "ISMAILMEDIA API is running!"

@app.route('/api/download', methods=['GET'])
def get_video_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                    filesize = f.get('filesize', 0) or f.get('filesize_approx', 0)
                    size_mb = round(filesize / (1024 * 1024), 1) if filesize else 0
                    
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution', 'Audio'),
                        'url': f.get('url'),
                        'filesize_mb': size_mb
                    })
            
            formats.reverse()

            return jsonify({
                'title': info.get('title'),
                'source': info.get('extractor_key'),
                'formats': formats[:10]
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
