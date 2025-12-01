# pip install fastapi uvicorn pydantic
# pip install Pillow imageio

# usage:
# uvicorn video_player:app --reload --host 0.0.0.0 --port 9000
# (Port forwarding) ssh -L 9000:localhost:9000 user@remote_host

import os
from pathlib import Path
from typing import Optional, List, Union, Tuple

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel

# --- Configuration ---
# Set the root directory for video browsing. 
# !!! IMPORTANT: CHANGE THIS TO YOUR DESIRED DIRECTORY !!!
VIDEO_ROOT_DIR = "/"

INITIAL_BROWSER_PATH = os.path.expanduser("~")  # Start browsing from the user's home directory

app = FastAPI(title="Video Streamer")

# --- Schemas ---
class FileItem(BaseModel):
    name: str
    path: str
    is_dir: bool
    # is_image_folder field is removed/ignored as it's not used in browse/resolve

# --- Path Utility Class ---

class PathAction(BaseModel):
    """Data structure for the frontend to know how to proceed."""
    # Action now only includes 'play', 'browse', or 'error'
    action: str  # 'play', 'browse', or 'error'
    path_to_use: Optional[str] = None # The path for the action
    browse_path: Optional[str] = None # The path for the file browser update
    error_detail: Optional[str] = None

# --- Helpers ---

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.webm', '.ogg')

# Keeping the helper for the image sequence check, but only used by the new /image_folder_files endpoint.
def is_image_folder(path: Path) -> bool:
    """Checks if a directory primarily contains image files."""
    if not path.is_dir():
        return False
        
    file_count = 0
    image_count = 0
    
    for item in sorted(os.listdir(path))[:100]:
        full_path = path / item
        if full_path.is_file():
            file_count += 1
            if item.lower().endswith(IMAGE_EXTENSIONS):
                image_count += 1
    
    return file_count >= 2 and (image_count / file_count) > 0.8

def get_absolute_path(relative_path: str) -> Path:
    # ... (get_absolute_path remains the same) ...
    """
    Safely converts a relative path to an absolute path within the root directory,
    resolving soft links securely.
    """
    root_path = Path(VIDEO_ROOT_DIR).resolve()
    full_path = root_path.joinpath(relative_path.lstrip('/'))
    try:
        resolved_path = full_path.resolve(strict=True) 
    except FileNotFoundError:
        try:
            full_path.resolve(strict=False).relative_to(root_path)
            return full_path
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid path or outside root directory.")

    try:
        resolved_path.relative_to(root_path)
    except ValueError:
        raise HTTPException(status_code=400, detail="Forbidden: Symlink points outside of the root directory.")
    return resolved_path

def resolve_path_action(relative_path: str) -> PathAction:
    """
    Checks the path existence and type, and determines the correct action.
    - Simplified to only handle video files or browsing directories.
    """
    if not relative_path:
        return PathAction(action='browse', path_to_use='')

    try:
        abs_path = get_absolute_path(relative_path)
    except HTTPException:
        return PathAction(action='error', error_detail="Path is outside the allowed root directory.")

    # Action 1: If it's a video file, play the video and browse its parent.
    if abs_path.is_file() and str(abs_path).lower().endswith(VIDEO_EXTENSIONS):
        try:
            parent_path = str(abs_path.parent.relative_to(VIDEO_ROOT_DIR)).replace('\\', '/')
        except ValueError:
             parent_path = ''
             
        return PathAction(
            action='play', 
            path_to_use=relative_path,
            browse_path=parent_path
        )
    
    # Action 2: If it's a directory, or any other file type, browse it.
    if abs_path.is_dir():
        return PathAction(action='browse', path_to_use=relative_path)

    # Action 3: Path does not exist. Find the closest existing parent.
    current = Path(relative_path)
    while current != Path('.'): 
        parent_path_str = str(current.parent).replace('\\', '/')
        try:
            abs_parent = get_absolute_path(parent_path_str)
            if abs_parent.is_dir():
                return PathAction(
                    action='browse', 
                    path_to_use=parent_path_str, 
                    error_detail=f"Path '{relative_path}' not found or is not a video file. Browsing closest existing parent: '{parent_path_str}'."
                )
        except HTTPException:
            return PathAction(action='browse', path_to_use='') 

        current = current.parent
        
    return PathAction(action='browse', path_to_use='')


# --- Endpoints ---

@app.post("/resolve_path", response_model=PathAction)
async def resolve_path(path_data: dict):
    """API to resolve the user-inputted path before playback/browsing."""
    path = path_data.get('path', '')
    return resolve_path_action(path)


@app.get("/", response_class=HTMLResponse)
async def serve_player():
    """Serves the main HTML video player page."""
    return HTML_CONTENT

@app.get("/browse", response_model=List[FileItem])
async def browse_files(path: Optional[str] = ""):
    """Lists files and directories in a given path (no image folder detection)."""
    try:
        current_dir = get_absolute_path(path)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    if not current_dir.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found.")

    items: List[FileItem] = []
    
    if current_dir.resolve() != Path(VIDEO_ROOT_DIR).resolve():
        parent_path = str(Path(path).parent).replace('\\', '/')
        items.append(FileItem(name=".. (Up Directory)", path=parent_path, is_dir=True))

    for item in sorted(os.listdir(current_dir)):
        full_path = current_dir / item
        
        relative_path_for_frontend = str(full_path.relative_to(VIDEO_ROOT_DIR)).replace('\\', '/')
        
        if item.startswith('.'):
            continue

        if full_path.is_dir():
            # Directories are always returned as is_dir=True
            items.append(FileItem(
                name=item, 
                path=relative_path_for_frontend, 
                is_dir=True 
            ))
        elif full_path.is_file() and item.lower().endswith(VIDEO_EXTENSIONS):
            # Only video files are explicitly listed as non-directories
            items.append(FileItem(name=item, path=relative_path_for_frontend, is_dir=False))

    # --- ADD SORTING LOGIC HERE ---
    items.sort(key=lambda item: (not item.is_dir, item.name.lower()))
    
    return items

@app.get("/image_folder_files/{folder_path:path}", response_model=List[str])
async def get_image_folder_files(folder_path: str):
    """Returns a sorted list of relative paths to images within a folder."""
    try:
        abs_path = get_absolute_path(folder_path)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    if not abs_path.is_dir():
        # Do not check is_image_folder here, let the frontend decide if it wants to play
        # any folder as a sequence, but still verify it's a directory.
        raise HTTPException(status_code=404, detail="Folder not found.")

    image_files: List[str] = []
    
    for item in sorted(os.listdir(abs_path)):
        if item.lower().endswith(IMAGE_EXTENSIONS):
            full_image_path = abs_path / item
            relative_image_path = str(full_image_path.relative_to(VIDEO_ROOT_DIR)).replace('\\', '/')
            image_files.append(relative_image_path)
            
    if not image_files:
        raise HTTPException(status_code=404, detail="No image files found in the folder.")
        
    return image_files


@app.get("/image/{image_path:path}")
async def stream_image(image_path: str):
    # ... (Image streaming logic remains the same) ...
    """Streams a single image file."""
    try:
        file_path = get_absolute_path(image_path)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Image file not found.")

    mime_type = "image/jpeg"
    if image_path.lower().endswith(('.png')):
        mime_type = "image/png"
    elif image_path.lower().endswith(('.gif')):
        mime_type = "image/gif"

    def file_iterator(file):
        with open(file, "rb") as f:
            while True:
                data = f.read(1024 * 1024)
                if not data:
                    break
                yield data

    return StreamingResponse(
        file_iterator(file_path),
        headers={"Content-Type": mime_type}
    )


# --- Video Streaming Endpoint (Remains the same) ---

@app.get("/video/{video_path:path}")
async def stream_video(video_path: str, request: Request):
    # ... (Video streaming logic remains the same) ...
    """
    Streams a video file, respecting HTTP Range headers for seeking/traversal.
    """
    try:
        file_path = get_absolute_path(video_path)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Video file not found.")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    def file_iterator(file, chunk_size, start, end):
        with open(file, "rb") as f:
            f.seek(start)
            while f.tell() < end:
                read_size = min(chunk_size, end - f.tell())
                data = f.read(read_size)
                if not data:
                    break
                yield data

    if range_header:
        byte1, byte2 = range_header.split("=")[1].split("-")
        start = int(byte1)
        end = int(byte2) if byte2 else file_size - 1
        end = min(end, file_size - 1)
        content_length = end - start + 1
        
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": "video/mp4"
        }

        return StreamingResponse(
            file_iterator(file_path, 1024 * 1024, start, end + 1),
            status_code=206,
            headers=headers
        )

    headers = {
        "Content-Length": str(file_size),
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4"
    }
    
    def full_file_iterator(file, chunk_size):
        with open(file, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    return StreamingResponse(
        full_file_iterator(file_path, 1024 * 1024),
        headers=headers
    )

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Video/Image Streamer</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <style>
        /* 🎨 Material Design Colors */
        :root {
            --md-primary-color: #3F51B5; /* Indigo 500 */
            --md-accent-color: #FF4081; /* Pink A200 */
            --md-text-color-dark: #212121; /* Grey 900 */
            --md-text-color-light: #757575; /* Grey 600 */
            --md-surface-color: #FFFFFF;
            --md-divider-color: #E0E0E0; /* Grey 300 */
            --md-shadow-1dp: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        }

        /* Global Fullscreen Layout */
        body { 
            font-family: 'Roboto', sans-serif; 
            display: flex; 
            margin: 0; 
            width: 100vw; 
            height: 100vh; 
            overflow: hidden; 
            background-color: #f5f5f5; 
            color: var(--md-text-color-dark);
        }

        /* File Browser Pane (Component with Elevation) */
        #browser { 
            width: 300px; 
            padding: 20px; 
            box-sizing: border-box; 
            min-width: 250px; 
            background-color: var(--md-surface-color);
            box-shadow: var(--md-shadow-1dp); 
            z-index: 10; 
            display: flex;
            flex-direction: column;
            height: 100vh; 
            overflow-y: hidden; 
        }

        /* Player Container (Takes remaining space) */
        #player-container { 
            flex-grow: 1; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
            overflow-y: auto; 
            background-color: #f5f5f5; 
        }
        
        /* Typography */
        h2 {
            font-weight: 500; 
            color: var(--md-primary-color);
            margin-top: 10px; /* Adjusted margin since info text is now above */
            margin-bottom: 15px;
        }

        /* Path Controls Container (Vertical Stack) */
        #path-controls { 
            display: block; 
            margin-bottom: 10px; 
            flex-shrink: 0; 
        }
        
        /* Container for the buttons (Horizontal Flex) */
        #path-buttons {
            display: flex; 
            justify-content: flex-end; 
            margin-top: 10px; 
        }

        /* Input Field (Material Underline Style) */
        input[type="text"] { 
            width: 100%; 
            padding: 8px 0; 
            margin-bottom: 5px; 
            border: none;
            border-bottom: 2px solid var(--md-divider-color); 
            box-sizing: border-box; 
            transition: border-bottom-color 0.2s;
            font-size: 16px;
            background: transparent;
        }
        input[type="text"]:focus {
            outline: none;
            border-bottom-color: var(--md-primary-color); 
        }

        /* 🖼️ Action Button (Raised Button Style) */
        .action-button { 
            padding: 8px 15px; 
            cursor: pointer; 
            background-color: var(--md-primary-color);
            color: white; 
            border: none; 
            border-radius: 4px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); 
            transition: background-color 0.2s, box-shadow 0.2s;
            text-transform: uppercase;
            font-weight: 500;
            margin-left: 10px;
        }
        .action-button:hover {
            background-color: #3949AB; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.25); 
        }
        .action-button:active {
            box-shadow: 0 1px 3px rgba(0,0,0,0.3); 
        }
        
        /* Accent Button (for 'Play Image Folder') */
        #play-image-folder-btn { 
            background-color: var(--md-accent-color); 
            margin-left: 10px; 
            display: none; 
        }
        #play-image-folder-btn:hover { background-color: #F73378; }
        
        /* Scrolling Container */
        #file-list-container {
            flex-grow: 1; 
            overflow-y: auto; 
            padding-right: 5px; 
        }

        #status-message { 
            color: var(--md-accent-color); 
            font-weight: 500; 
            margin-top: 10px; 
            flex-shrink: 0;
        }
        
        /* File List */
        #file-list { 
            list-style: none; 
            padding: 0; 
            margin-top: 0;
        }
        #file-list li { 
            margin-bottom: 2px; 
            cursor: pointer; 
            padding: 8px 5px; 
            border-radius: 4px; 
            transition: background-color 0.1s;
        }
        #file-list li:hover { background-color: #eeeeee; } 
        .dir { font-weight: 500; color: var(--md-primary-color); } 
        .file { color: var(--md-text-color-dark); } 
        
        /* Media Player Elements */
        video, img { 
            width: 100%; 
            max-height: 100%; 
            flex-shrink: 1; 
            background-color: #333333; 
            display: none;
            object-fit: contain; 
            box-shadow: 0 3px 6px rgba(0,0,0,0.16); 
        }

        /* Image Controls (Contained Card) */
        #image-controls { 
            margin-top: 15px; 
            padding: 15px; 
            border: none; 
            background-color: var(--md-surface-color);
            box-shadow: var(--md-shadow-1dp); 
            border-radius: 4px;
            display: none; 
            flex-shrink: 0; 
        }
        
        /* Input Field (Material Underline Style) for FPS input */
        #image-controls input[type="number"] { 
            width: 60px; 
            margin-right: 10px; 
            padding: 5px 0; 
            border: none;
            border-bottom: 2px solid var(--md-divider-color); 
            border-radius: 0; 
            transition: border-bottom-color 0.2s;
            text-align: center;
        }
        #image-controls input[type="number"]:focus {
            outline: none;
            border-bottom-color: var(--md-primary-color);
        }

        #image-controls label { margin-right: 15px; color: var(--md-text-color-light); }
        
        /* Progress Bar / Slider Container */
        #image-slider-container { 
            display: flex; 
            align-items: center; 
            margin-top: 20px; 
            padding: 10px 0;
            background-color: transparent; 
            border-radius: 4px; 
        }
        
        /* Image Slider Styling */
        #image-slider { 
            flex-grow: 1; 
            margin: 0 15px; 
            -webkit-appearance: none;
            appearance: none;
            height: 8px; 
            background: var(--md-divider-color); 
            border-radius: 4px;
            cursor: pointer;
        }

        /* Custom styles for the thumb (the movable circle) - Webkit (Chrome/Safari) */
        #image-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            background: var(--md-primary-color); 
            border-radius: 50%;
            border: 1px solid var(--md-surface-color);
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
            margin-top: -5px; 
        }

        /* Styles for the filled track (Webkit) using a CSS variable */
        #image-slider::-webkit-slider-runnable-track {
            background: linear-gradient(to right, 
                var(--md-primary-color) 0%, 
                var(--md-primary-color) var(--slider-progress, 0%), 
                var(--md-divider-color) var(--slider-progress, 0%), 
                var(--md-divider-color) 100%
            );
            height: 8px;
            border-radius: 4px;
        }

        /* Custom styles for the thumb (the movable circle) - Mozilla (Firefox) */
        #image-slider::-moz-range-thumb {
            width: 18px;
            height: 18px;
            background: var(--md-primary-color); 
            border-radius: 50%;
            border: none;
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
        }

        /* Styles for the filled track (Firefox) */
        #image-slider::-moz-range-progress {
            background: var(--md-primary-color);
            height: 8px;
            border-radius: 4px 0 0 4px;
        }
        
        /* Container for the frame index input and total */
        #frame-jump-control {
            display: flex;
            align-items: center;
            margin-right: 10px;
        }
        
        /* Styling for the frame jump input field */
        #frame-index-input {
            width: 40px; 
            padding: 5px; 
            border: 1px solid var(--md-divider-color);
            border-radius: 4px;
            text-align: right;
            font-size: 0.9em;
            color: var(--md-text-color-dark); 
            margin-right: 5px;
        }
        #frame-index-input:focus {
            outline: none;
            border-color: var(--md-divider-color); 
            box-shadow: none;
        }

        /* Style for the frame info text */
        #frame-info-start {
            display: none; 
        }
        #frame-total-info {
            color: var(--md-text-color-light);
            font-size: 0.9em;
            min-width: 20px; 
            text-align: center;
        }
        
        #video-info {
            flex-shrink: 0; 
            color: var(--md-text-color-light);
            /* Removed margin-top, now only margin-bottom should be used */
            margin-bottom: 5px;
            margin-top: 0;
        }
        
        hr {
            border: none;
            border-top: 1px solid var(--md-divider-color);
            margin: 10px 0;
            flex-shrink: 0;
        }
    </style>
</head>
<body>

    <div id="browser">
        <h2>File Browser</h2>
        <div id="path-controls">
            <input type="text" id="path-input" placeholder="Enter path (e.g., folder/video.mp4)" value="">
            
            <div id="path-buttons">
                <button onclick="resolvePathAndAct()" class="action-button">Resolve</button>
                <button id="play-image-folder-btn" onclick="manualPlayImageFolder()" class="action-button">Play Image Folder</button>
            </div>

        </div>
        <hr>
        
        <div id="file-list-container">
            <p id="status-message"></p>
            <ul id="file-list"></ul>
        </div>
    </div>

    <div id="player-container">
        <p id="video-info">Select a media file or browse to a folder.</p>
        
        <h2>Media Player</h2>
        
        <video id="video-player" controls autoplay></video>
        
        <img id="image-player" src="" alt="Image Sequence Player">

        <div id="image-controls">
            <label for="fps-input">FPS:</label>
            <input type="number" id="fps-input" value="10" min="1" max="60">
            <button id="start-sequence-btn" onclick="toggleImagePlayback()" class="action-button">Play</button>
            <div id="image-slider-container">
                <span id="frame-info-start">0</span>
                <input type="range" id="image-slider" min="0" max="0" value="0">
                
                <div id="frame-jump-control">
                    <input type="number" id="frame-index-input" value="1" min="1" max="1">
                    <span id="frame-total-info">/ 0</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const INITIAL_PATH = "{INITIAL_BROWSER_PATH}";
        const videoPlayer = document.getElementById('video-player');
        const imagePlayer = document.getElementById('image-player');
        const fileList = document.getElementById('file-list');
        const pathInput = document.getElementById('path-input');
        const videoInfo = document.getElementById('video-info');
        const statusMessage = document.getElementById('status-message');
        const imageControls = document.getElementById('image-controls');
        const fpsInput = document.getElementById('fps-input');
        const imageSlider = document.getElementById('image-slider');
        
        const frameIndexInput = document.getElementById('frame-index-input');
        const frameTotalInfo = document.getElementById('frame-total-info');
        
        const playImageFolderBtn = document.getElementById('play-image-folder-btn');
        const startSequenceBtn = document.getElementById('start-sequence-btn');

        let currentBrowserPath = INITIAL_PATH;
        let imageFiles = []; 
        let currentImageFrame = 0;
        let isPlaying = false; 
        let frameInterval = null; 
        let isWaitingForLoad = false; 

        /** Stops any existing image playback timer (both interval and timeout) */
        function stopImagePlaybackTimer() {
            if (frameInterval) {
                clearTimeout(frameInterval);
                frameInterval = null;
            }
            imagePlayer.onload = null;
            imagePlayer.onerror = null;
            
            isPlaying = false;
            isWaitingForLoad = false;
        }

        /** Utility to switch player visibility and reset controls */
        function switchPlayer(type) {
            stopImagePlaybackTimer(); 

            videoPlayer.style.display = 'none';
            imagePlayer.style.display = 'none';
            imageControls.style.display = 'none';
            
            startSequenceBtn.textContent = 'Play';

            if (type === 'video') {
                videoPlayer.style.display = 'block';
                imagePlayer.src = '';
            } else if (type === 'image') {
                imagePlayer.style.display = 'block';
                imageControls.style.display = 'block';
                videoPlayer.src = '';
                videoPlayer.load();
            } else {
                videoPlayer.src = '';
                imagePlayer.src = '';
                videoPlayer.load();
                videoInfo.textContent = 'Select a media file or browse to a folder.';
            }
        }
        
        /** Fetches file list for a given path and updates the UI */
        async function fetchFiles(path) {
            statusMessage.textContent = ''; 
            playImageFolderBtn.style.display = 'none'; 

            try {
                const response = await fetch(`/browse?path=${encodeURIComponent(path)}`);
                if (!response.ok) {
                    const error = await response.json();
                    alert(`Error browsing path: ${error.detail}`);
                    return;
                }
                const files = await response.json();
                
                currentBrowserPath = path;
                pathInput.value = path || '/'; 

                if (path !== '' && pathInput.value === path) {
                    playImageFolderBtn.style.display = 'inline-block';
                }

                fileList.innerHTML = ''; 
                
                files.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item.name;
                    li.classList.add(item.is_dir ? 'dir' : 'file');
                    li.setAttribute('data-path', item.path);

                    li.onclick = () => {
                        pathInput.value = item.path; 
                        if (item.is_dir) {
                            fetchFiles(item.path); 
                            playImageFolderBtn.style.display = 'inline-block';
                        } else {
                            playVideo(item.path); 
                            playImageFolderBtn.style.display = 'none';
                        }
                    };
                    fileList.appendChild(li);
                });
            } catch (error) {
                console.error("Fetch error:", error);
                alert("Could not connect to the file server.");
            }
        }
        
        /** Sets the video player source to start streaming */
        function playVideo(videoRelativePath) {
            switchPlayer('video');
            const videoSourceUrl = `/video/${encodeURIComponent(videoRelativePath)}`;
            
            videoPlayer.src = videoSourceUrl;
            videoPlayer.load();
            videoPlayer.play();
            
            pathInput.value = videoRelativePath;
            // MODIFIED: Simplified text content
            videoInfo.textContent = `Playing: ${videoRelativePath}`;
        }
        
        /** Prepares the image player by fetching file list */
        async function prepareImagePlayback(folderRelativePath) {
             switchPlayer('image'); 
             // MODIFIED: Simplified text content
             videoInfo.textContent = `Playing: ${folderRelativePath}`;
             pathInput.value = folderRelativePath; 
             
             currentImageFrame = 0;
             startSequenceBtn.textContent = 'Play';

             try {
                const response = await fetch(`/image_folder_files/${encodeURIComponent(folderRelativePath)}`);
                if (!response.ok) {
                    const error = await response.json();
                    alert(`Error loading image sequence: ${error.detail}`);
                    switchPlayer('none');
                    return;
                }
                imageFiles = await response.json();
                
                imageSlider.max = imageFiles.length - 1;
                imageSlider.value = currentImageFrame;
                
                frameIndexInput.min = 1;
                frameIndexInput.max = imageFiles.length;

                updateFrameInfo(); 
                
                displayCurrentImage(); 

            } catch (error) {
                console.error("Image sequence load error:", error);
                alert("Could not load image sequence from the server.");
                switchPlayer('none');
            }
        }

        /** * Displays the current image. 
         * If playing, it sets up the load/timing logic for the next frame.
         */
        function displayCurrentImage() {
            if (imageFiles.length === 0) return;

            const imageRelativePath = imageFiles[currentImageFrame];
            const imageSourceUrl = `/image/${encodeURIComponent(imageRelativePath)}`;
            
            updateFrameInfo();
            imageSlider.value = currentImageFrame; 
            
            // Calculate progress percentage and set CSS variable for Webkit filled track
            const progress = imageFiles.length > 1 ? (currentImageFrame / (imageFiles.length - 1)) * 100 : 0;
            imageSlider.style.setProperty('--slider-progress', `${progress}%`);

            if (isPlaying) {
                isWaitingForLoad = true;
                
                const fps = parseFloat(fpsInput.value);
                const intervalMs = 1000 / fps;

                const nextFrame = () => {
                    isWaitingForLoad = false; 

                    if (isPlaying) {
                        currentImageFrame = (currentImageFrame + 1) % imageFiles.length;
                        displayCurrentImage();
                    }
                };

                imagePlayer.onload = () => {
                    const timeElapsed = performance.now() - startTime;
                    const delay = Math.max(0, intervalMs - timeElapsed);

                    frameInterval = setTimeout(nextFrame, delay);
                };
                
                imagePlayer.onerror = (e) => {
                    console.error("Error loading image frame:", imageRelativePath, e);
                    const timeElapsed = performance.now() - startTime;
                    const delay = Math.max(0, intervalMs - timeElapsed);

                    frameInterval = setTimeout(nextFrame, delay);
                };
                
                const startTime = performance.now();
                imagePlayer.src = imageSourceUrl;

            } else {
                imagePlayer.src = imageSourceUrl;
            }
        }


        /** Updates the frame count display */
        function updateFrameInfo() {
            const frameNumber = currentImageFrame + 1; 
    
            frameIndexInput.value = frameNumber;
            frameTotalInfo.textContent = `/ ${imageFiles.length}`;
        }
        
        /** Starts or resumes playback, or pauses if already playing. */
        function toggleImagePlayback() {
            if (imageFiles.length === 0) {
                alert("No image files loaded. Please select an image folder first.");
                return;
            }
            
            if (isPlaying) {
                // PAUSE
                stopImagePlaybackTimer();
                startSequenceBtn.textContent = 'Resume';
                return;
            }

            const fps = parseFloat(fpsInput.value);
            if (isNaN(fps) || fps <= 0) {
                alert("Please enter a valid FPS (Frames Per Second).");
                return;
            }
            
            // START or RESUME Playback
            stopImagePlaybackTimer(); 
            
            isPlaying = true;
            startSequenceBtn.textContent = 'Pause';
            
            displayCurrentImage(); 
        }

        /** Handler for the 'Resolve Path' button */
        async function resolvePathAndAct() {
            const path = pathInput.value.trim();
            if (!path) {
                fetchFiles(currentBrowserPath);
                return;
            }
            
            try {
                const response = await fetch('/resolve_path', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: path })
                });

                if (!response.ok) {
                    const error = await response.json();
                    alert(`Error resolving path: ${error.detail}`);
                    return;
                }
                
                const result = await response.json();
                
                statusMessage.textContent = result.error_detail || '';

                if (result.action === 'play') {
                    playVideo(result.path_to_use);
                    fetchFiles(result.browse_path);
                } else if (result.action === 'browse') {
                    fetchFiles(result.path_to_use);
                    
                    const resolvedPath = result.path_to_use;
                    if (!resolvedPath.toLowerCase().match(/(\.mp4|\.webm|\.ogg)$/)) {
                         playImageFolderBtn.style.display = 'inline-block';
                    }
                    if (result.error_detail) {
                       pathInput.value = ''; 
                    }
                } else if (result.action === 'error') {
                    alert(result.error_detail);
                }

            } catch (error) {
                console.error("Path resolution error:", error);
                alert("Could not resolve path with the server.");
            }
        }
        
        /** Handler for the new "Play Image Folder" button */
        function manualPlayImageFolder() {
            const path = pathInput.value.trim();
            if (!path) {
                alert("Please enter or select a folder path.");
                return;
            }
            prepareImagePlayback(path);
        }

        // --- Event Listeners for Image Controls ---
        
        // 1. SLIDER CHANGE LISTENER
        imageSlider.addEventListener('input', (event) => {
            currentImageFrame = parseInt(event.target.value);
            if (isPlaying) {
                stopImagePlaybackTimer();
                startSequenceBtn.textContent = 'Resume';
            }
            displayCurrentImage(); 
        });

        // 2. INPUT FIELD CHANGE LISTENER 
        frameIndexInput.addEventListener('change', (event) => {
            let desiredFrame = parseInt(event.target.value);
            
            if (isNaN(desiredFrame)) {
                frameIndexInput.value = currentImageFrame + 1;
                return;
            }
            
            desiredFrame = Math.max(1, Math.min(desiredFrame, imageFiles.length));
            
            currentImageFrame = desiredFrame - 1;
            
            if (isPlaying) {
                stopImagePlaybackTimer();
                startSequenceBtn.textContent = 'Resume';
            }
            
            imageSlider.value = currentImageFrame;
            displayCurrentImage();
        });

        // 3. FPS CHANGE LISTENER
        fpsInput.addEventListener('change', () => {
            if (isPlaying) {
                toggleImagePlayback(); 
                toggleImagePlayback(); 
            }
        });


        // --- Initial Load ---
        switchPlayer('none');
        fetchFiles(currentBrowserPath); 

    </script>
</body>
</html>
"""

HTML_CONTENT = HTML_CONTENT.replace("{INITIAL_BROWSER_PATH}", INITIAL_BROWSER_PATH)