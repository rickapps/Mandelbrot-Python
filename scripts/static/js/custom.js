//      custom.js - Mandelbrot Set
//      Copyright (C) 2021  Rick Eichhorn: rickapps@live.com

//      This program is free software: you can redistribute it and/or modify
//      it under the terms of the GNU General Public License as published by
//      the Free Software Foundation, either version 3 of the License, or
//      (at your option) any later version.

//      This program is distributed in the hope that it will be useful,
//      but WITHOUT ANY WARRANTY; without even the implied warranty of
//      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//      GNU General Public License for more details.

//      You should have received a copy of the GNU General Public License
//      along with this program.  If not, see <https://www.gnu.org/licenses/>.

$(function() {
    // JQueryUI set up draggable properties
    $("#selection-box").draggable({ 
      containment: "#containment-wrapper", scroll: false,
      stop: function( event, ui ) {}
    });

    // The image scales to fit the screen, but the server works in
    // pixels of the full size image. Convert the selection box position
    // to image pixels. The server expects y measured from the bottom
    // of the image, negative going up.
    function setZoomFields() {
      var wrapper = $('#containment-wrapper');
      var box = $('#selection-box');
      var img = $('#containment-wrapper img')[0];
      var scale = img.naturalWidth / wrapper.width();
      var left = parseFloat(box.css('left'));
      var top = parseFloat(box.css('top'));
      $('#xtopLeft').val(left * scale);
      $('#ytopLeft').val(top * scale - img.naturalHeight);
      $('#xcenter').val((left + box.outerWidth()/2) * scale);
      $('#ycenter').val((top + box.outerHeight()/2) * scale - img.naturalHeight);
    }

    $("#selection-box").on({
      dragstop: function( event, ui ) {
        // Store the position as a percentage so the box stays put
        // over the same area if the image is resized (e.g. phone rotated)
        var wrapper = $('#containment-wrapper');
        $(this).css({
          left: (ui.position.left / wrapper.width() * 100) + '%',
          top: (ui.position.top / wrapper.height() * 100) + '%'
        });
      },
      mouseenter: function(){
        $("#selection-box h2").show();
      },
      mouseleave: function(){
        $("#selection-box h2").hide();
      }
    });

    $('#submit').on ({
      click: function(e) {
        setZoomFields();
        $('#containment-wrapper').off();
        $('#selection-box').off();
        $('#selection-box h2').hide();
        $('.spinner-grow').show();
      }
    });

    // The double click event does not
    // seem to bubble to the selection box
    // when used on a touch screen.
    // I have tried adding a double click
    // handler to the selection box, but
    // it still does not work on touch
    // screen. Everything works as expected
    // with the mouse.
    $('#containment-wrapper').on({
      dblclick: function() {
        $('#submit').click();
      }
    });
  
    $("#magnify a").click(function(){
      $('#containment-wrapper').off();
      $('#selection-box')
        .off()
        .removeAttr('style')
        .css('border', '0')
      $('#selection-box h2').hide();
      $('.spinner-grow').show();
    });

    // To be done on document ready.
    $("#selection-box h2").hide();
    $('.spinner-grow').hide();
  });
  