$(function() {
    // JQueryUI set up draggable properties
    $("#selection-box").draggable({ 
      containment: "#containment-wrapper", scroll: false 
    });
    $("#containment-wrapper").mouseover(function(){$("#selection-box h2").show()});
    $("#containment-wrapper").mouseout(function(){$("#selection-box h2").hide()});
  });
  