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

    // Tried setting the fields on form submit, but position() values
    // don't seem to be accurate. Not sure why, perhaps not recognizing
    // parent div?.
    $("#selection-box").on({
      dragstop: function( event, ui ) {
        // ui contains position and offset. Position is relative to the containment-wrapper
        // We need the size of the selection-box so we can calculate cx,cy, and domain
        $('#xtopLeft').val(ui.position.left);
        $('#ytopLeft').val(ui.position.top);
        $('#xcenter').val(ui.position.left + $(this).outerWidth()/2);
        $('#ycenter').val(ui.position.top + $(this).outerHeight()/2);
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
        $('#containment-wrapper').off();
        $('#selection-box').off().show();
        $('#selection-box h2').hide();
        $('.spinner-grow').show();
      },
      mouseenter: function(){
        $("#selection-box").show();
      },
      mouseleave: function(){
        $("#selection-box").hide();
      }
    });

    $('#containment-wrapper').on({
      mouseenter: function(){
        $("#selection-box").show();
      },
      mouseleave: function(){
        $("#selection-box").hide();
      },
      dblclick(){
        $('#submit').click();
      }
    });
  
    $("#magnify a").click(function(){
      $('#containment-wrapper').off();
      $('#selection-box')
        .off()
        .removeAttr('style')
        .css('border', '0')
        .show();
      $('#selection-box h2').hide();
      $('.spinner-grow').show();
    });

    // To be done on document ready. Using css to get
    // values as position method does not seem to be accurate.
    var box = $('#selection-box');
    var left = parseInt(box.css('left'));
    var top = parseInt(box.css('top'));
    $('#xtopLeft').val(left);
    $('#ytopLeft').val(top);
    $('#xcenter').val(left + box.outerWidth()/2);
    $('#ycenter').val(top + box.outerHeight()/2);
    $("#selection-box").hide();
    $("#selection-box h2").hide();
    $('.spinner-grow').hide();
  });
  