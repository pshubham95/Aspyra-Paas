var validNavigation = false;


function wireUpEvents() {
  /*
  * For a list of events that triggers onbeforeunload on IE
  * check http://msdn.microsoft.com/en-us/library/ms536907(VS.85).aspx
  */
  window.onbeforeunload = function() {
    if(!localStorage.getItem('background')){
      if (!validNavigation) {

        $.ajax({
            url: '/del_con',
            type: 'POST',
            async: false,
      processData: false,
      contentType: false,

            success: function(response) {
        console.log(response);
      },

      error: function(error) {
        console.log(error);

      }

    });

        }

    }
  }

  // Attach the event keypress to exclude the F5 refresh

  // Attach the event click for all links in the page
  $("a").bind("click", function() {
    validNavigation = true;
  });

  // Attach the event submit for all forms in the page
  $("form").bind("submit", function() {
    validNavigation = true;
  });



  // Attach the event click for all inputs in the page
  $("input[type=submit]").bind("click", function() {
    validNavigation = true;
  });

}

// Wire up the events as soon as the DOM tree is ready
$(document).ready(function() {
  wireUpEvents();
  $(document.body).on("keydown", this, function (event) {
      if (event.keyCode == 116) {
          alert('F5 pressed!');
      }
  });
});
