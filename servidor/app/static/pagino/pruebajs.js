var alturaMax = 85

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
actualizar_termometro(20)
