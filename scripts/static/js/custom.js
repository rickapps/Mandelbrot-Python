$(function() {
    // JQueryUI set up draggable properties
    $("#selection-box").draggable({ 
      containment: "#containment-wrapper", scroll: false,
      stop: function( event, ui ) {}
    });
    $("#selection-box").on( "dragstop", function( event, ui ) {
      // ui contains position and offset. Position is relative to the containment-wrapper
      // We need the size of the selection-box so we can calculate cx,cy, and domain
      $('#xtopLeft').val(ui.position.left);
      $('#ytopLeft').val(ui.position.top);
      $('#xcenter').val(ui.position.left + this.offsetWidth/2);
      $('#ycenter').val(ui.position.top + this.offsetHeight/2);
    });
    $("#containment-wrapper").mouseover(function(){$("#selection-box h2").show()});
    $("#containment-wrapper").mouseout(function(){$("#selection-box h2").hide()});
    $('#magnify').submit(function(){
      // Populate our form
      var box = $('#selection-box');
      var pos = box.position();
      var wid = box.width();
      var height = box.height();
    });
    var box = $('#selection-box');
    $('#xtopLeft').val(box.position().left);
    $('#ytopLeft').val(box.position().top);
    $('#xcenter').val(box.position().left + box.outerWidth()/2);
    $('#ycenter').val(box.position().top - box.outerHeight()/2);
  });
  