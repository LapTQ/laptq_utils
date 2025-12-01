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
    <style>
        body { font-family: sans-serif; display: flex; max-width: 1200px; margin: 0 auto; }
        #browser { width: 300px; padding: 20px; border-right: 1px solid #ccc; height: 100vh; overflow-y: auto; }
        #player-container { flex-grow: 1; padding: 20px; }
        #file-list { list-style: none; padding: 0; }
        #file-list li { margin-bottom: 5px; cursor: pointer; padding: 5px; border-radius: 3px; }
        #file-list li:hover { background-color: #eee; }
        .dir { font-weight: bold; color: #1e88e5; } 
        .file { color: #388e3c; } 
        video, img { width: 100%; height: auto; background-color: black; display: none; }
        input[type="text"] { width: 100%; padding: 8px; margin-bottom: 5px; border: 1px solid #ccc; box-sizing: border-box; }
        #path-controls { display: flex; margin-bottom: 10px; }
        #path-controls button { margin-left: 10px; }
        #path-input { flex-grow: 1; margin-left: 0 !important; }
        .action-button { padding: 8px 15px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 4px; }
        #play-image-folder-btn { background-color: #e51e88; margin-left: 10px; display: none; } /* Hidden by default */
        #status-message { color: orange; font-weight: bold; margin-top: 10px; }
        #image-controls { margin-top: 10px; padding: 10px; border: 1px dashed #ccc; display: none; }
        #image-controls input[type="number"] { width: 60px; margin-right: 10px; padding: 5px; }
        #image-controls label { margin-right: 15px; }
        #image-slider-container { display: flex; align-items: center; margin-top: 10px; }
        #image-slider { flex-grow: 1; margin: 0 15px; }
        #frame-info { min-width: 100px; text-align: right; }
    </style>
</head>
<body>

    <div id="browser">
        <h2>📁 File Browser</h2>
        <div id="path-controls">
            <input type="text" id="path-input" placeholder="Enter path (e.g., folder/video.mp4)" value="">
            <button onclick="resolvePathAndAct()" class="action-button">Resolve</button>
            <button id="play-image-folder-btn" onclick="manualPlayImageFolder()" class="action-button">Play Image Folder</button>
        </div>
        <hr>
        <p>Current Path: <span id="current-path">/</span></p>
        <p id="status-message"></p>
        <ul id="file-list"></ul>
    </div>

    <div id="player-container">
        <h2>▶️ Media Player</h2>
        
        <video id="video-player" controls autoplay></video>
        
        <img id="image-player" src="" alt="Image Sequence Player">

        <div id="image-controls">
            <p id="image-info-text"></p>
            <label for="fps-input">FPS:</label>
            <input type="number" id="fps-input" value="10" min="1" max="60">
            <button id="start-sequence-btn" onclick="toggleImagePlayback()" class="action-button">Play</button>
            <div id="image-slider-container">
                <span id="frame-info-start">0</span>
                <input type="range" id="image-slider" min="0" max="0" value="0">
                <span id="frame-info">Frame 0 / 0</span>
            </div>
        </div>

        <p id="video-info">Select a media file or browse to a folder.</p>
    </div>

    <script>
        const INITIAL_PATH = "{INITIAL_BROWSER_PATH}";
        const videoPlayer = document.getElementById('video-player');
        const imagePlayer = document.getElementById('image-player');
        const fileList = document.getElementById('file-list');
        const pathInput = document.getElementById('path-input');
        const currentPathSpan = document.getElementById('current-path');
        const videoInfo = document.getElementById('video-info');
        const statusMessage = document.getElementById('status-message');
        const imageControls = document.getElementById('image-controls');
        const fpsInput = document.getElementById('fps-input');
        const imageSlider = document.getElementById('image-slider');
        const frameInfo = document.getElementById('frame-info');
        const imageInfoText = document.getElementById('image-info-text');
        const playImageFolderBtn = document.getElementById('play-image-folder-btn');
        const startSequenceBtn = document.getElementById('start-sequence-btn');
        // REMOVED: const pauseSequenceBtn = document.getElementById('pause-sequence-btn'); 

        let currentBrowserPath = INITIAL_PATH;
        let imageSequenceTimer = null; 
        let imageFiles = []; 
        let currentImageFrame = 0;
        let isPlaying = false; 

        /** Stops any existing image playback timer */
        function stopImagePlaybackTimer() {
            if (imageSequenceTimer) {
                clearInterval(imageSequenceTimer);
                imageSequenceTimer = null;
            }
            isPlaying = false;
        }

        /** Utility to switch player visibility and reset controls */
        function switchPlayer(type) {
            stopImagePlaybackTimer(); // Ensure playback is stopped

            videoPlayer.style.display = 'none';
            imagePlayer.style.display = 'none';
            imageControls.style.display = 'none';
            
            // Reset image sequence button text
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
            }
        }
        
        /** Fetches file list for a given path and updates the UI (remains the same) */
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
                currentPathSpan.textContent = path || '/';

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
        
        /** Sets the video player source to start streaming (remains the same) */
        function playVideo(videoRelativePath) {
            switchPlayer('video');
            const videoSourceUrl = `/video/${encodeURIComponent(videoRelativePath)}`;
            
            videoPlayer.src = videoSourceUrl;
            videoPlayer.load();
            videoPlayer.play();
            
            pathInput.value = videoRelativePath;
            videoInfo.textContent = `Streaming Video: ${videoRelativePath}`;
        }
        
        /** Prepares the image player by fetching file list, but doesn't start playback (modified to reset state) */
        async function prepareImagePlayback(folderRelativePath) {
             switchPlayer('image'); // This calls stopImagePlaybackTimer()
             videoInfo.textContent = `Image Sequence Ready: ${folderRelativePath}`;
             pathInput.value = folderRelativePath; 
             imageInfoText.textContent = `Folder: ${folderRelativePath}`;
             
             // Reset playback state for new folder
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
                updateFrameInfo();
                
                displayCurrentImage();

            } catch (error) {
                console.error("Image sequence load error:", error);
                alert("Could not load image sequence from the server.");
                switchPlayer('none');
            }
        }

        /** Displays the current image in the sequence (remains the same) */
        function displayCurrentImage() {
            if (imageFiles.length === 0) return;
            const imageRelativePath = imageFiles[currentImageFrame];
            const imageSourceUrl = `/image/${encodeURIComponent(imageRelativePath)}`;
            imagePlayer.src = imageSourceUrl;
            updateFrameInfo();
            imageSlider.value = currentImageFrame; 
        }

        /** Updates the frame count display (remains the same) */
        function updateFrameInfo() {
            frameInfo.textContent = `Frame ${currentImageFrame + 1} / ${imageFiles.length}`;
        }
        
        /** Starts or resumes playback, or pauses if already playing. */
        function toggleImagePlayback() {
            if (imageFiles.length === 0) {
                alert("No image files loaded. Please select an image folder first.");
                return;
            }
            
            if (isPlaying) {
                // If currently playing, treat this button as a pause/stop
                stopImagePlaybackTimer();
                startSequenceBtn.textContent = 'Resume';
                return;
            }

            const fps = parseFloat(fpsInput.value);
            if (isNaN(fps) || fps <= 0) {
                alert("Please enter a valid FPS (Frames Per Second).");
                return;
            }
            
            // Start or Resume Playback
            stopImagePlaybackTimer(); // Clear any residual timer
            const intervalMs = 1000 / fps;

            imageSequenceTimer = setInterval(() => {
                currentImageFrame = (currentImageFrame + 1) % imageFiles.length;
                displayCurrentImage();
            }, intervalMs);
            
            isPlaying = true;
            startSequenceBtn.textContent = 'Pause';
        }

        /** Handler for the 'Resolve Path' button (remains the same) */
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
        
        /** Handler for the new "Play Image Folder" button (remains the same) */
        function manualPlayImageFolder() {
            const path = pathInput.value.trim();
            if (!path) {
                alert("Please enter or select a folder path.");
                return;
            }
            prepareImagePlayback(path);
        }

        // --- Event Listeners for Image Controls ---
        imageSlider.addEventListener('input', (event) => {
            currentImageFrame = parseInt(event.target.value);
            displayCurrentImage();
            // Stop automatic playback when user interacts with the slider
            if (isPlaying) {
                // The new logic to pause (stopImagePlaybackTimer and update button text)
                stopImagePlaybackTimer();
                startSequenceBtn.textContent = 'Resume';
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