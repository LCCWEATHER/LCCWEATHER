function cambiarColor(color) {
  document.body.style.background = "#" + color;
}

var grads = [
  [{color:"00000c",position:0},{color:"00000c",position:0}],
  [{color:"020111",position:85},{color:"191621",position:100}],
  [{color:"020111",position:60},{color:"20202c",position:100}],
  [{color:"020111",position:10},{color:"3a3a52",position:100}],
  [{color:"20202c",position:0},{color:"515175",position:100}],
  [{color:"40405c",position:0},{color:"6f71aa",position:80},{color:"8a76ab",position:100}],
  [{color:"4a4969",position:0},{color:"7072ab",position:50},{color:"cd82a0",position:100}],
  [{color:"757abf",position:0},{color:"8583be",position:60},{color:"eab0d1",position:100}],
  [{color:"82addb",position:0},{color:"ebb2b1",position:100}],
  [{color:"94c5f8",position:1},{color:"a6e6ff",position:70},{color:"b1b5ea",position:100}],
  [{color:"b7eaff",position:0},{color:"94dfff",position:100}],
  [{color:"9be2fe",position:0},{color:"67d1fb",position:100}],
  [{color:"90dffe",position:0},{color:"38a3d1",position:100}],
  [{color:"57c1eb",position:0},{color:"246fa8",position:100}],
  [{color:"2d91c2",position:0},{color:"1e528e",position:100}],
  [{color:"2473ab",position:0},{color:"1e528e",position:70},{color:"5b7983",position:100}],
  [{color:"1e528e",position:0},{color:"265889",position:50},{color:"9da671",position:100}],
  [{color:"1e528e",position:0},{color:"728a7c",position:50},{color:"e9ce5d",position:100}],
  [{color:"154277",position:0},{color:"576e71",position:30},{color:"e1c45e",position:70},{color:"b26339",position:100}],
  [{color:"163C52",position:0},{color:"4F4F47",position:30},{color:"C5752D",position:60},{color:"B7490F",position:80},{color:"2F1107",position:100}],
  [{color:"071B26",position:0},{color:"071B26",position:30},{color:"8A3B12",position:80},{color:"240E03",position:100}],
  [{color:"010A10",position:30},{color:"59230B",position:80},{color:"2F1107",position:100}],
  [{color:"090401",position:50},{color:"4B1D06",position:100}],
  [{color:"00000c",position:80},{color:"150800",position:100}],
];

var meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
var dias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]

function toCSSGradient(data)
{
  var css = "linear-gradient(to bottom, "
  var len = data.length

  for (var i=0;i<len;i++)
  {
     var item = data[i]
     css+= " #" + item.color + " " + item.position + "%"
     if ( i<len-1 ) css += ","
  }
  return css + ")";
}

var horaActual = undefined;

function cambiarFondoSegunHora(hora) {
  if(horaActual != hora) {
    horaActual = hora

    document.body.style.background = toCSSGradient(grads[hora])
  }
}

function actualizarFondo() {
  var fecha = new Date()
  cambiarFondoSegunHora(fecha.getHours())
  var cosa = document.querySelector(".fecha")

  cosa.innerHTML = dias[fecha.getDay()] + " " + fecha.getDate() + " de " + meses[fecha.getMonth()] + " del " + fecha.getFullYear()

  cosa = document.querySelector(".hora")

  cosa.innerHTML = fecha.getHours() + ":" + fecha.getMinutes()
}

google.charts.load('current', {packages: ['corechart', 'line']})
google.charts.setOnLoadCallback(drawBasic)

function drawBasic() {

  var humedad = new google.visualization.DataTable()
  var temperatura = new google.visualization.DataTable()
  var presion = new google.visualization.DataTable()
  humedad.addColumn('timeofday','h')
  humedad.addColumn('number','b')
  temperatura.addColumn('timeofday','h')
  temperatura.addColumn('number','C°')
  presion.addColumn('timeofday', 'X')
  presion.addColumn('number', 'ayy')

  
  var ultimaActualizacion = Date.now() - 2 * 60 * 60 * 1000
  var graficaActual = 0;
  function actualizarGrafica() {
    cargarDatos(ultimaActualizacion).then(function(datos) {
      var nRows = datos['datos'].length
      console.log(datos)
      if(nRows) {
        if(presion.getNumberOfRows()) {
          presion.removeRows(0, nRows)
          humedad.removeRows(0, nRows)
          temperatura.removeRows(0, nRows)
        }
        agregarDatos(presion, humedad, temperatura, datos['datos'])
        actualizarMedidores(datos['datos'][0])
        chart.draw(datos[graficaActual], opciones[graficaActual])
      }
      
      chart.draw(tablas[graficaActual], opciones[graficaActual])
      graficaActual = (graficaActual + 1) % 3;

      setTimeout(actualizarGrafica, 5000)
    })
    ultimaActualizacion = Date.now()
  }

  var opcion1 = {
    animation:{
        duration: 1000,
        easing: 'out'
    },
    hAxis: {
      title: 'Hora',
      baselineColor: '#fff'
    },
    vAxis: {
      baselineColor: '#fff',
      title: 'temperatura'
    },
    backgroundColor: { fill:'transparent' },
  }
  var opcion2 = {
    animation:{
        duration: 1000,
        easing: 'out'
    },
    hAxis: {
      title: 'Hora',
      baselineColor: '#fff'
    },
    vAxis: {
      baselineColor: '#fff',
      title: 'Presión'
    },
    backgroundColor: { fill:'transparent' },
  }
  var opcion3 = {
    animation:{
        duration: 1000,
        easing: 'out'
      },
    hAxis: {
      title: 'Hora',
      baselineColor: '#fff'
    },
    vAxis: {
      baselineColor: '#fff',
      title: 'Humedad'
    },
    backgroundColor: { fill:'transparent' },
  }
  
  var chart = new google.visualization.LineChart(document.getElementById('grafica_temp'))
  var tablas = [temperatura, presion, humedad]
  var opciones = [opcion1, opcion2, opcion3]
  function siguienteGrafica() {
    chart.draw(datos[graficaActual], opciones[graficaActual])
  }
  //chart.draw(datos[0],opciones[0])
  //setInterval(siguienteGrafica, 3 * 1000)
  
  actualizarGrafica()

  
  return {
    chart,
    tablas
  }
}
var alturaMax = 123
function actualizar_termometro(cTemp) {
  var cTempPercent = cTemp * alturaMax / 45
  var cMargin = -cTempPercent+20;
  if (cTemp > -50) {
    if (cTemp >= 50) {
      $('.temperature').height(200);
      $('.temperature').css({
        'margin-top': '-180px'
      });
    }
    $('.temperature').height(cTempPercent);
    $('.temperature').css({
      'margin-top': cMargin + 'px'
    });
  } else {
    $('.temperature').height(0);
  }
}

function cargarDatos(tiempo) {
  var dominio = 'http://localhost:5000'
  return fetch(dominio + '/api/lecturas?d=' + tiempo)
    .then(function(respuesta) {
      return respuesta.json()
    })
}

function agregarDatos(presion, humedad, temperatura, datos) {
  datos.reverse().forEach(function(lectura) {
    var time = new Date(lectura.fecha)
    var timeofday = [time.getHours(), time.getMinutes(), time.getSeconds()]
    humedad.addRow([timeofday, lectura.humedad]);
    temperatura.addRow([timeofday, lectura.temperatura]);
    presion.addRow([timeofday, lectura.presion]);
  })
}

function actualizarMedidores(lectura) {
  var centigrados = lectura.temperatura - 273

  $('#valorTemperatura').text(centigrados + '°')
  $('#valorPresion').text(lectura.presion + ' hpa')
  $('#valorHumedad').text(lectura.humedad + '%')
  $('#valorMonoxido').text(lectura.monoxido + '%')
  $('#valorNitrogeno').text(lectura.nitrogeno + '%')
  actualizar_termometro(centigrados)
}

function cargarAlertas() {
  fetch('http://localhost:5000/api/alertas')
    .then(function(respuesta) {
      return respuesta.json()
    }).then(function(json) {
      var contenedor = $('#contenedorAlertas')
      contenedor.empty()
      json.alertas.forEach(function(alerta) {
        contenedor.append($('<li>').text(alerta.text))
      })

    })
}

actualizarFondo()
setInterval(actualizarFondo, 60 * 1000);
