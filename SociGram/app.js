let posts = [];
let userAudioStream;
let audioActive = true;
let remoteAudioStream;
let peerConnection;

async function startMedia() {
  try {
    userAudioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const userAudio = document.getElementById('userAudio');
    userAudio.srcObject = userAudioStream;
  } catch (error) {
    console.error('Error accessing the microphone:', error);
  }
}

function toggleAudio() {
  const toggleButton = document.getElementById('toggleAudio');
  if (audioActive) {
    userAudioStream.getTracks().forEach((track) => track.stop());
    toggleButton.textContent = 'Start Audio';
    audioActive = false;
  } else {
    startMedia();
    toggleButton.textContent = 'Stop Audio';
    audioActive = true;
  }
}

function startCall() {
  const remoteAudio = document.getElementById('remoteAudio');
  remoteAudioStream = new MediaStream();
  remoteAudio.srcObject = remoteAudioStream;

  // Configure ICE servers - replace with your own TURN/STUN server configuration
  const iceServers = [
    { urls: 'stun:stun.l.google.com:19302' },
    // Add your own TURN server here if necessary
  ];

  // Create a peer connection
  peerConnection = new RTCPeerConnection({ iceServers });

  // Add the user's audio stream to the peer connection
  userAudioStream.getTracks().forEach((track) => peerConnection.addTrack(track, userAudioStream));

  // Set up event handlers for the peer connection - not shown in this example

  // Create an offer to initiate the call - not shown in this example
}

startMedia();

function navigateToProfile() {
    // Redirect to the profile page
    window.location.href = 'profile.html';
  }
  

function toggleCamera() {
  const toggleButton = document.getElementById('toggleCamera');
  if (cameraActive) {
    userVideoStream.getTracks().forEach((track) => track.stop());
    toggleButton.textContent = 'Start Camera';
    cameraActive = false;
  } else {
    startMedia();
    toggleButton.textContent = 'Stop Camera';
    cameraActive = true;
  }
}

startMedia();

function postMessage() {
  const postContent = document.getElementById('postContent').value;
  if (postContent) {
    posts.push(postContent);
    displayPosts();
    document.getElementById('postContent').value = '';
  }
}

function displayPosts() {
  const postList = document.getElementById('postList');
  postList.innerHTML = '';

  posts.forEach((post, index) => {
    const postElement = document.createElement('div');
    postElement.className = 'alert alert-primary';
    postElement.textContent = post;

    const deleteButton = document.createElement('button');
    deleteButton.className = 'btn btn-danger btn-sm';
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = () => deletePost(index);

    postElement.appendChild(deleteButton);
    postList.appendChild(postElement);
  });
}

function deletePost(index) {
  posts.splice(index, 1);
  displayPosts();
}

startMedia();
