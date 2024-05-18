function get_webcam_frame() {
    // Access the webcam using OpenCV.js
    const video = document.createElement('video');
    video.width = 640; // Adjust width as needed
    video.height = 480; // Adjust height as needed
  
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.play();
      })
      .catch(error => {
        console.error("Error accessing webcam:", error);
        alert("Error: Could not access webcam."); // Display an alert for the user
      });
  
    return new Promise((resolve, reject) => {
      video.onloadedmetadata = () => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
  
        const draw = () => {
          context.drawImage(video, 0, 0);
  
          // Process the frame (extract face and convert to encoding)
          const face_encoding = process_frame(context); // Replace with your logic
  
          if (face_encoding) { // If a face is detected and encoded
            resolve(face_encoding); // Resolve the promise with the encoding
            video.pause(); // Pause the video after capturing a frame (optional)
          }
  
          requestAnimationFrame(draw);
        };
  
        draw();
      };
    });
  }
  
  function process_frame(context) {
    // Implement face detection logic using OpenCV.js
    const face_locations = detect_faces(context); // Replace with your logic
  
    if (face_locations.length > 0) {
      // Assuming only one face detected, extract the facial region
      const [top, right, bottom, left] = face_locations[0];
      const face_image = context.getImageData(left, top, right - left, bottom - top);
  
      // Convert face image to format suitable for facial recognition (e.g., RGB)
      const rgb_face_image = convert_to_rgb(face_image);  // Replace with your logic
  
      // Extract facial encoding using your chosen library (e.g., face_recognition)
      const encoding = extract_encoding(rgb_face_image);  // Replace with your logic
  
      return encoding;
    } else {
      return null; // No face detected
    }
  }
  