document.addEventListener('DOMContentLoaded', function () {
  const appElement = document.getElementById('app_evaluacion');
  const idevaluacion = appElement.getAttribute('data-idevaluacion');
  const videoIds = JSON.parse(appElement.getAttribute('data-video-ids')); // Get the list of video IDs from the backend
  const videoIdsLista = JSON.parse(appElement.getAttribute('data-video-ids-lista')); // Get the list of video IDs from the backend
  const nombrefase = appElement.getAttribute('data-nombrefase');  
  const videoSeccion = JSON.parse(appElement.getAttribute('seccion-video'));// Get the list of video sections from the backend
  const videoNumber=JSON.parse(appElement.getAttribute('list-video'));// Get the list of video number from the backend
  const videoNumberUltimo=JSON.parse(appElement.getAttribute('ultimo-video-codigo'));
  const videoSeccionUltimo=JSON.parse(appElement.getAttribute('ultimo-video-seccion'));
  const videoIdUltimo=JSON.parse(appElement.getAttribute('ultimo-video-id'));
  
  //console.log('\n\n>>>>>>>>>> DEBUG: idevaluacion:', idevaluacion);
  console.log('videoIds:', videoIds);
  console.log('videoIdsLista:', videoIdsLista);
  console.log('nombrefase:', nombrefase);
  console.log('videoSeccion:', videoSeccion);
  console.log('videoNumber:', videoNumber);
  console.log('videoNumberUltimo:', videoNumberUltimo);
  console.log('videoSeccionUltimo:', videoSeccionUltimo);
  console.log('videoIdUltimo:', videoIdUltimo);

  const mensajeDiv = document.getElementById('mensaje');
  mensajeDiv.innerText = "Hola, el video seleccionado tiene ID: " + videoSeccionUltimo;

  let randomVideoId, idvideo, seccionvideo, numerovideo;

  
  if (videoSeccionUltimo==3 || videoSeccionUltimo == 0){
    // Filtrar solo los videos que tengan sección igual a 1
    const indicesSeccion1 = videoSeccion
    .map((seccion, index) => seccion == 1 ? index : null)
    .filter(index => index !== null);

    // Obtener un índice aleatorio de los videos con sección 1
    randomIndex= indicesSeccion1[Math.floor(Math.random() * indicesSeccion1.length)];
    randomVideoId = videoIds[randomIndex]; // URL del video
    idvideo = videoIdsLista[randomIndex];  // ID del video
    seccionvideo = videoSeccion[randomIndex]; // Sección del video
    numerovideo = videoNumber[randomIndex]; // Número del video
  }

  if (videoSeccionUltimo==1 || videoSeccionUltimo==2){
    // Calcular la siguiente sección
    
    if(videoSeccionUltimo==1){
      seccionvideo = 2;
    } else {
      seccionvideo = 3;
      }
  //mensajeDiv.innerText = "Hola, el video seleccionado tiene ID: " + idvideo + " y pertenece a la sección: " + seccionvideo+" y del video: "+numerovideo+" el randomvideo: "+randomVideoId;

    numerovideo = videoNumberUltimo;
  //mensajeDiv.innerText = "Hola, el video seleccionado tiene ID: " + idvideo + " y pertenece a la sección: " + seccionvideo+" y del video: "+numerovideo+" el randomvideo: "+randomVideoId;

    // Buscar el índice del video con la misma numeración y la sección siguiente
    const index = videoSeccion.findIndex((seccion, i) => 
      seccion == seccionvideo && videoNumber[i] == numerovideo
    );

    // Asignar los datos correspondientes
    if (index !== -1) {
      idvideo = videoIdsLista[index];
      randomVideoId = videoIds[index]; // URL del video
    } else {
      console.warn("No se encontró un video con la sección " + seccionvideo + " y número " + numerovideo);
    }
  }
  //Esta línea es super útil para validar el video que estas visualizando
  //ensajeDiv.innerText = "Hola, el video seleccionado tiene ID: " + idvideo + " y pertenece a la sección: " + seccionvideo+" y del video: "+numerovideo+"el código del ultimo video es: "+videoIdUltimo+" y pertenece a la sección: "+videoSeccionUltimo+" y del video: "+videoNumberUltimo;

  const app_evaluacion = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
      return {
        player: null,
        videoId: this.extractVideoId(randomVideoId), // Use the randomly selected video ID
        idvideo: idvideo,
        videoDuration: 0,        
        idevaluacion: idevaluacion,
        isButtonEnabled: false,
        timeLeft: 15 * 60, // 15 minutos en segundos,
        matriz_datos: [],
        nombrefase: nombrefase,
        progressBarSegments: [],
        contadorPalanqueo: 0,
        contadorLevantamiento: 0,
        contadorAcercamiento: 0,
        resultadosVideo: [],
      }
    },
    computed: {
      formattedTime() {
          const minutes = Math.floor(this.timeLeft / 60);
          const seconds = this.timeLeft % 60;          
          return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
      }
  },
    mounted() {
      this.loadYouTubeIframeAPI();              
    },
    methods: {
      extractVideoId(url) {
        const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const matches = url.match(regex);
        return matches ? matches[1] : null;
    },
      loadYouTubeIframeAPI() {
        // Cargar dinámicamente la API de YouTube IFrame si aún no está cargada
        if (!window.YT) {
          const tag = document.createElement('script');
          tag.src = 'https://www.youtube.com/iframe_api';
          const firstScriptTag = document.getElementsByTagName('script')[0];
          firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

          window.onYouTubeIframeAPIReady = this.initializePlayer;
        } else {
          this.initializePlayer();
        }
      },
      initializePlayer() {
        this.player = new window.YT.Player('video-player', {
          height: '390',
          width: '640',
          videoId: this.videoId,
          playerVars: { 'autoplay': 0, 'controls': 0 },
          events: {
            onReady: this.onPlayerReady,
            onStateChange: this.onPlayerStateChange,
          },
        });
        this.getResultadosVideo();
      },
      checkVideoTime() {
        // const video = this.$refs.video;
        if (this.player.getCurrentTime() >= 1 * 60) { // 15 minutos en segundos
          this.isButtonEnabled = true;          
        }        
      },
      
      onPlayerReady(event) {
        //Duración del video en minutos
        this.videoDuration = Math.ceil(event.target.getDuration() / 60);                
        this.timeLeft = event.target.getDuration()-1;
        //matriz con los datos de las acciones(Palanqueo, Levantamiento, Acercamiento,Entrega Pellet,Consumo Pellet)
        this.matriz_datos = Array.from({ length: this.videoDuration }, (_, index) => {
          const startSecond = index * 60;
          const endSecond = (index + 1) * 60 - 1;
          return [this.idvideo, `${startSecond} - ${endSecond}`, 0, 0, 0]; // Asignar rango de segundos a la primera columna
        });
        this.initializeProgressBar();
      },

      onPlayerStateChange(event) {
        if (event.data === window.YT.PlayerState.PLAYING) {
          this.currentTime = event.target.getCurrentTime();   
          this.startCountdown();               
        }
        if (event.data === window.YT.PlayerState.PAUSED) {
          this.pauseCountdown();
        }
            if (event.data === window.YT.PlayerState.ENDED) {
              console.log("El video ha terminado. Llamando a finalizar...");
              this.finalizar(); // Llama a la función para guardar y redirigir
        }

      },

      accion(conducta) {
        //Esto solo está aplicando para la fase de habituación.  Se debe ajustar para las demás fases
        if (conducta === 'Palanqueo') {
          this.updateDataMatrix(2);
          this.contadorPalanqueo += 1;
        } else if (conducta === 'Levantamiento') {
          this.updateDataMatrix(3);
          this.contadorLevantamiento += 1;
        } else if (conducta === 'Acercamiento') {
          this.updateDataMatrix(4);
          this.contadorAcercamiento += 1;
         } //else if (conducta === 'Entrega Pellet') {
        //   this.updateDataMatrix(5);
        // } else if (conducta === 'Consumo Pellet') {
        //   this.updateDataMatrix(6);
        // }
      },

      //Obtiene los datos de la fila de la matriz correspondiente al minuto
      getRowIndexBySecond(second) {
        // Asume que cada fila en matriz_datos representa un minuto del video
        const rowIndex = Math.floor(second / 60);
        return rowIndex;
      },

      //Actualiza la matriz de datos con la acción correspondiente
      updateDataMatrix(action) {
        const rowIndex = this.getRowIndexBySecond(this.player.getCurrentTime());
        this.matriz_datos[rowIndex][action] += 1;
      },

      updateProgressBar() {        
        const currentTime = this.player.getCurrentTime();
        const minutes = Math.floor(currentTime / 60);       
        
        this.progressBarSegments[minutes].color = this.checkIfCorrect(minutes) ? 'green' : 'red';                           
        
      },
      checkIfCorrect(minute) {
        var palanqueos = 0;
        var levantamientos = 0;
        var acercamientos = 0;
        fin = (minute * 60) + 59;
        inicio = minute * 60;
        console.log('Fin:', fin);
        for (let i = 0; i < this.resultadosVideo.length; i++) {          
          if (this.resultadosVideo[i].nombre == 'Palanqueo' && this.resultadosVideo[i].fin == fin) {
            
            palanqueos = this.resultadosVideo[i].cantidad
          }
          if (this.resultadosVideo[i].nombre == 'Levantamiento' && this.resultadosVideo[i].fin == fin) {
            
            levantamientos = this.resultadosVideo[i].cantidad
          }
          if (this.resultadosVideo[i].nombre == 'Acercamiento' && this.resultadosVideo[i].fin == fin) {
            
            acercamientos = this.resultadosVideo[i].cantidad
          }
        }
        

        if (palanqueos == this.contadorPalanqueo && levantamientos == this.contadorLevantamiento && acercamientos == this.contadorAcercamiento) {
          this.contadorPalanqueo = 0;
          this.contadorLevantamiento = 0;
          this.contadorAcercamiento = 0;
          return true;
        } 
        this.contadorPalanqueo = 0;
        this.contadorLevantamiento = 0;
        this.contadorAcercamiento = 0; 
        return false;
        
        
      },
      finalizar() {
        this.player.pauseVideo();
        console.log(this.matriz_datos);
        // Enviar los datos al backend                
        fetch('/evaluacion/guardar_datos', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            matriz_datos: this.matriz_datos,
            idvideo: this.idvideo,
            idevaluacion: this.idevaluacion,
            nombrefase: this.nombrefase
          })
        })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            // Redireccionar a otra página
            window.location.href = '/evaluacion/resultado/' + this.idevaluacion;
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      },
      getResultadosVideo() {
        fetch('/evaluacion/videosconductasview/'+this.idvideo, {
         method: 'GET',
          headers: {            
             'X-Requested-With': 'XMLHttpRequest'
          } 
      })
          .then(response => response.json())
          .then(data => {
            this.resultadosVideo = data['videos_conductas_view'];
            console.log('Success retornar resultados:', this.resultadosVideo);            
          })
          .catch((error) => {
            console.error('Error al obtener resultados:', error);
          });
      },
      startCountdown() {
        this.timer = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
            } else {
                clearInterval(this.timer);
            }           
            if ((Math.ceil(this.player.getCurrentTime() % 60))  == 59) {
                this.updateProgressBar(); 
                console.log('Actualizar barra de progreso');    
            }
        }, 1000);        
    },
    pauseCountdown() {
      if (this.timer) {
          clearInterval(this.timer);
          this.timer = null;
      }
    },
    initializeProgressBar() {
      const totalMinutes = Math.ceil(this.videoDuration)-1;
      console.log('Total minutos:', totalMinutes);
      this.progressBarSegments = Array.from({ length: totalMinutes }, () => ({ color: 'gray' }));            
    },
   // Se determina el color de cada boton -- Andres Ramirez
    getButtonClass(conducta) {
      switch (conducta) {
        case 'Palanqueo':
          return 'btn-palanqueo';
        case 'Levantamiento':
          return 'btn-levantamiento';
        case 'Acercamiento':
          return 'btn-acercamiento';
        default:
          return 'btn-default';
      }
    }
    }

  });

  app_evaluacion.mount('#app_evaluacion');
});