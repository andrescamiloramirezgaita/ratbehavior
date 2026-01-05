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
  
  const conductaIndices = {
    'Palanqueo': 2,
    'Levantamiento': 3,
    'Acercamiento': 4,
    'Comedero': 5,
    'Aproximación': 6,
    'Tocar Palanca': 7,
    'Palanqueo Reforzado': 8,
    'Palanqueo No Reforzado': 9
  };
  
  //console.log('\n\n>>>>>>>>>> DEBUG: idevaluacion:', idevaluacion);
  //console.log('videoIds:', videoIds);
  //console.log('videoIdsLista:', videoIdsLista);
  //console.log('nombrefase:', nombrefase);
  //console.log('videoSeccion:', videoSeccion);
  //console.log('videoNumber:', videoNumber);
  //console.log('videoNumberUltimo:', videoNumberUltimo);
  //console.log('videoSeccionUltimo:', videoSeccionUltimo);
  //console.log('videoIdUltimo:', videoIdUltimo);

  const mensajeDiv = document.getElementById('mensaje');
  //mensajeDiv.innerText = "Hola, el video seleccionado tiene ID: " + videoSeccionUltimo;

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
        contadorComedero: 0, // Nuevo
        contadorAproximacion: 0, // Nuevo
        contadorTocarPalanca: 0, // Nuevo
        contadorPalanqueoReforzado: 0, // Nuevo
        contadorPalanqueoNoReforzado: 0, // Nuevo
        resultadosVideo: [],
        progressTimer: null, // New property to store the progress bar timer
        lastMinute: -1, // Nueva variable para rastrear el último minuto evaluado
        botonActivo: null, // Guardará el nombre del botón activo
        contadores: {
        'Palanqueo': 0,
        'Levantamiento': 0,
        'Acercamiento': 0,
        'Comedero': 0,
        'Aproximación': 0,
        'Tocar Palanca': 0,
        'Palanqueo Reforzado': 0,
        'Palanqueo No Reforzado': 0
        }
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
        
        // Inicializar un temporizador de finalización
        this.completionTimer = setInterval(() => {
            this.checkVideoCompletion();
        }, 1000); // Se verifica cada segundo
        
        //matriz con los datos de las acciones(Palanqueo, Levantamiento, Acercamiento,Entrega Pellet,Consumo Pellet)
        this.matriz_datos = Array.from({ length: this.videoDuration }, (_, index) => {
          const startSecond = index * 60;
          const endSecond = (index + 1) * 60 - 1;
          return [this.idvideo, `${startSecond} - ${endSecond}`, 0,0,0,0,0,0,0,0]; // Asignar rango de segundos a la primera columna
        });
        this.initializeProgressBar();
      },

      checkVideoCompletion() {
        const currentTime = this.player.getCurrentTime();
        const duration = this.player.getDuration();

        // Verificación 1: Si el video ha terminado (evento ENDED)
        /*if (this.player && this.player.getPlayerState() === window.YT.PlayerState.ENDED) {
            console.log("El evento ENDED se ha disparado. Finalizando...");
            clearInterval(this.completionTimer);
            this.finalizar();
            return;
        }
       */
       //  Verificación 2: Si el tiempo actual es muy cercano a la duración total del video
        if (duration > 0 && currentTime >= duration - 0.5) {
            console.log("El tiempo ha llegado al final. Finalizando...");
            clearInterval(this.completionTimer);
            this.finalizar();
            this.finalizar();
            this.finalizar();
        //    this.isButtonEnabled = true;
            return;
        }
        

        // Verificación 3: Nueva condición para finalizar a los 5 minutos y 4 segundos
        /*const cincoMinutosCuatroSegundos = (5 * 60)+2;
        if (currentTime >= cincoMinutosCuatroSegundos) {
            console.log("Se ha superado el tiempo de 5 minutos y 4 segundos. Finalizando...");
            clearInterval(this.completionTimer);
            this.isButtonEnabled = true;
            //this.finalizar();
        }*/
      },

/*      toggleButtons(shouldDisable) {
        const botonesConducta = document.querySelectorAll('.buttons .button:not(.btn-finalizar)');
        botonesConducta.forEach(boton => {
          boton.disabled = shouldDisable;
        });
      },
*/
      /*
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
*/
    onPlayerStateChange(event) {
        // Habilitar/deshabilitar botones y controlar el contador
        if (event.data === window.YT.PlayerState.PLAYING) {
            //this.toggleButtons(false);
            this.startCountdown();
            // Start a new timer to update the progress bar every second
            this.progressTimer = setInterval(() => {
              this.updateProgressBar();
            }, 1000);
        } else {
            //this.toggleButtons(true);
            this.pauseCountdown();

            // Clear the progress bar timer when the video is not playing 
            if (this.progressTimer) {
            clearInterval(this.progressTimer);
            this.progressTimer = null;
          }
        }
    },
     accion(conducta) {
            const index = conductaIndices[conducta];
            this.botonActivo = conducta; // Para cambiar el estado
            if (index !== undefined) {
              this.updateDataMatrix(index);
            }

            switch (conducta) {
                case 'Palanqueo':
                    this.contadorPalanqueo += 1;
                    break;
                case 'Levantamiento':
                    this.contadorLevantamiento += 1;
                    break;
                case 'Acercamiento':
                    this.contadorAcercamiento += 1;
                    break;
                case 'Comedero':
                    this.contadorComedero += 1;
                    break;
                case 'Aproximación':
                    this.contadorAproximacion += 1;
                    break;
                case 'Tocar Palanca':
                    this.contadorTocarPalanca += 1;
                    break;
                case 'Palanqueo Reforzado':
                    this.contadorPalanqueoReforzado += 1;
                    break;
                case 'Palanqueo No Reforzado':
                    this.contadorPalanqueoNoReforzado += 1;
                    break;
            }
            // Ahora actualiza el contador en el objeto
            if (this.contadores[conducta] !== undefined) {
              this.contadores[conducta]++;
            }
       },

/*
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
*/

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

        // Actualizar solo cuando el minuto cambia
        if (minutes > this.lastMinute && this.lastMinute >= 0) {
            const correct = this.checkIfCorrect(this.lastMinute);
            this.progressBarSegments[this.lastMinute].color = correct ? 'green' : 'red';
            this.resetCounters();
        }
        this.lastMinute = minutes;
    },

      // Nueva función para reiniciar los contadores
      resetCounters() {
        // Reiniciar contadores para el siguiente minuto
        this.contadorPalanqueo = 0;
        this.contadorLevantamiento = 0;
        this.contadorAcercamiento = 0;
        this.contadorAproximacion = 0;
        this.contadorComedero=0;
        this.contadorTocarPalanca=0;
        this.contadorPalanqueoReforzado=0;
        this.contadorPalanqueoNoReforzado=0;
      },

      checkIfCorrect(minute) {
        const fin = (minute * 60) + 59;
        
        // Crear un objeto para almacenar las cantidades esperadas y obtenidas en este minuto
        const expected = {};
        const obtained = {};

        // Rellenar los valores esperados de la API
        for (const resultado of this.resultadosVideo) {
          if (resultado.fin === fin) {
            expected[resultado.nombre] = resultado.cantidad;
          }
        }
        
        // Rellenar los valores obtenidos de los contadores
        obtained['Palanqueo'] = this.contadorPalanqueo;
        obtained['Levantamiento'] = this.contadorLevantamiento;
        obtained['Acercamiento'] = this.contadorAcercamiento;
        obtained['Aproximación'] = this.contadorAproximacion;
        obtained['Comedero'] = this.contadorComedero;
        obtained['Tocar Palanca'] = this.contadorTocarPalanca;
        obtained['Palanqueo Reforzado'] = this.contadorPalanqueoReforzado;
        obtained['Palanqueo No Reforzado'] = this.contadorPalanqueoNoReforzado;

        // Comparar los objetos para ver si son iguales
        let correct = true;
        for (const nombre of Object.keys(expected)) {
          if (expected[nombre] !== (obtained[nombre] || 0)) {
            correct = false;
            break;
          }
        }
        return correct;
      },
   /*   checkIfCorrect(minute) {
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
   */
      finalizar() {
//        alert('Contenido de matriz_datos:\n' + this.matriz_datos);
        //this.player.pauseVideo();
        // Crea el objeto de datos que se va a enviar
        const datosParaEnviar = {
          matriz_datos: this.matriz_datos,
          idvideo: this.idvideo,
          idevaluacion: this.idevaluacion,
          nombrefase: this.nombrefase
        };

        // Agrega esta línea para ver los datos en la consola
        //console.log('Datos que se van a enviar:', datosParaEnviar);

        //alert('Contenido de id video:\n' + this.idvideo);
        //alert('Contenido de id video:\n' + this.idevaluacion);
        //alert('Contenido de id video:\n' + this.nombrefase);
        //console.log(this.matriz_datos);
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
          //alert('evaluacion/resultado:\n' + datosParaEnviar);
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
            //if ((Math.ceil(this.player.getCurrentTime() % 60))  == 59) {
            //    this.updateProgressBar(); 
            //    console.log('Actualizar barra de progreso');    
            //}
        }, 1000);        
    },
    pauseCountdown() {
      if (this.timer) {
          clearInterval(this.timer);
          this.timer = null;
      }
    },
    initializeProgressBar() {
        const totalMinutes = Math.floor(this.videoDuration); // O 5 si quieres una barra fija
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
        case 'Comedero':
            return 'btn-comedero';
        case 'Aproximación':
            return 'btn-aproximacion';
        case 'Tocar Palanca':
            return 'btn-tocar-palanca';
        case 'Tocar Palanca':
            return 'btn-tocar-palanca';
        case 'Palanqueo Reforzado': // Nuevo caso
            return 'btn-palanqueo-reforzado';
        case 'Palanqueo No Reforzado': // Nuevo caso
            return 'btn-palanqueo-no-reforzado';
        default:
            return 'btn-default';
      }
    }
  },

  });

  app_evaluacion.mount('#app_evaluacion');
});