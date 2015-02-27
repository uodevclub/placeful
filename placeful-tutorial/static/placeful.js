position = {coords:{latitude: "", longitude: ""} };
    function getLocation() {
      console.log('a');
      if(getCookie('latitude') && getCookie('longitude')){
        position.coords.latitude = getCookie('latitude');
        position.coords.longitude = getCookie('longitude');
        updatePosition(position)
      }else{
        if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(updatePosition);
          } else { 
              alert("Geolocation is not supported by this browser.");
          }
      }
    }

    function updatePosition(position) {
      console.log('b');
      loadMessages(position);
      setCookie('latitude', position.coords.latitude, .5);
      setCookie('longitude', position.coords.longitude, .5);

      $(function(){
        $("#latitude").val(position.coords.latitude);
        $("#longitude").val(position.coords.longitude);
      });
    }

    function loadMessages(position){
      console.log('c');
      $.ajax( "/messages/"+ position.coords.latitude + "/" + position.coords.longitude, {
        success: function(data){
          $('#messages').html(data);
        },
        error: function(){
          alert("A Derp was encountered when attempting to load the messages");
        }
      });
    }

    $(function(){
      $('#reset').click(function(event){
        deleteCookie('latitude');
        deleteCookie('longitude');
      })
      $('.msg-header').pin();
    });
    getLocation();