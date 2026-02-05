# air-piano
Gesture-Controlled Music

An AI-powered virtual piano that allows users to play music by hovering their fingers in the air. Using MediaPipe Hand Tracking, the system detects finger positions and triggers high-quality audio samples in real-time.

**How it Works**
Hand Landmark Detection: Uses MediaPipe to track 21 hand points.
Virtual Zones: The screen is divided into vertical "key zones."
Collision Detection: When the "Index Finger Tip" (Landmark 8) enters a zone, a specific sound file is triggered via pygame.mixer.

**Controls**
Play: Move your index finger over a virtual key.
Volume: (If you added this) Distance between thumb and index finger.
Quit: Press 'q' on your keyboard.

note: Lighting conditions and CPU speed may affect latency.
Sound Engine: use pygame.mixer.init() and pygame.mixer.Sound(). It is much faster for real-time triggers than other libraries.
Python version: 3.10.. to support mediapipe
