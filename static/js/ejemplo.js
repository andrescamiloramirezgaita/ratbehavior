document.addEventListener('DOMContentLoaded', function () {
    const appElement = document.getElementById('app_ejemplo');
    const videoUrl = appElement.getAttribute('data-video-url'); // URL del video
    const videoId = extractVideoId(videoUrl); // Extraer ID del video
  
    function extractVideoId(url) {
      const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
      const matches = url.match(regex);
      return matches ? matches[1] : null;
    }
  
    function loadYouTubeIframeAPI() {
      if (!window.YT) {
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        window.onYouTubeIframeAPIReady = initializePlayer;
      } else {
        initializePlayer();
      }
    }
  
    function initializePlayer() {
      new YT.Player('video-player', {
        height: '390',
        width: '640',
        videoId: videoId,
        playerVars: { autoplay: 1, controls: 1 },
      });
    }
  
    loadYouTubeIframeAPI();
  });
  