$(function() {
    // JQueryUI set up draggable properties
    $("#selection-box").draggable({ 
      containment: "#containment-wrapper", scroll: false,
      stop: function( event, ui ) {}
    });

    // Tried setting the fields on form submit, but position() values
    // don't seem to be accurate. Not sure why, perhaps not recognizing
    // parent div?.
    $("#selection-box").on( "dragstop", function( event, ui ) {
      // ui contains position and offset. Position is relative to the containment-wrapper
      // We need the size of the selection-box so we can calculate cx,cy, and domain
      $('#xtopLeft').val(ui.position.left);
      $('#ytopLeft').val(ui.position.top);
      $('#xcenter').val(ui.position.left + $(this).outerWidth()/2);
      $('#ycenter').val(ui.position.top + $(this).outerHeight()/2);
    });

    $("#containment-wrapper").mouseover(function(){$("#selection-box h2").show()});
    $("#containment-wrapper").mouseout(function(){$("#selection-box h2").hide()});

    // To be done on document ready. Using css to get
    // values as position method does not seem to be accurate.
    var box = $('#selection-box');
    var left = parseInt(box.css('left'));
    var top = parseInt(box.css('top'));
    $('#xtopLeft').val(left);
    $('#ytopLeft').val(top);
    $('#xcenter').val(left + box.outerWidth()/2);
    $('#ycenter').val(top + box.outerHeight()/2);
  });
  