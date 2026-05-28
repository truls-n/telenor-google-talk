import cv2
import os

def crop_video():
    input_path = os.path.join('media', 'looker-agent.mp4')
    output_path = os.path.join('media', 'looker-agent-cropped.mp4')
    
    print(f"Opening input video: {input_path}")
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return False
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Original dimensions: {width}x{height} @ {fps} FPS. Total frames: {total_frames}")
    
    # We want a 564x720 vertical cropped region
    # Center crop:
    crop_w = 564
    crop_h = 720
    
    start_x = (width - crop_w) // 2
    end_x = start_x + crop_w
    
    print(f"Cropping region: X from {start_x} to {end_x}, Y from 0 to {crop_h}")
    
    # On macOS, using 'avc1' (H.264) or 'mp4v' (MPEG-4) works best with PowerPoint
    # Let's try 'mp4v' first, as it is widely supported by OpenCV out-of-the-box
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (crop_w, crop_h))
    
    if not out.isOpened():
        print("Error: Could not open output video writer.")
        cap.release()
        return False
        
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Crop the frame
        cropped = frame[0:crop_h, start_x:end_x]
        out.write(cropped)
        
        frame_count += 1
        if frame_count % 50 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
            
    cap.release()
    out.release()
    print(f"Video cropped successfully and saved to: {output_path} ({os.path.getsize(output_path)} bytes)")
    return True

if __name__ == "__main__":
    crop_video()
