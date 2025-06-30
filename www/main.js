$(document).ready(function () {
    $('.text').textillate({
        loop:true,
        sync:true,
        in:{
            effect:"bounceIn",
        },
        out:{
            effect:"bounceOut",
        }
    })
    //siri config
      var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude:"1",
    speed:"0.30",
    autostart:true,
  });

  //siri message animaton
  $('.siri-message').textillate({
        loop:true,
        sync:true,
        in:{
            effect:"fadeInUp",
            sync:true
        },
        out:{
            effect:"fadeOutUp",
            sync:true
        }
    })

    // mic button click event
    $('#Micbtn').on('click', function() {
        eel.playAssistantSound(); // Play the assistant sound
        $('#oval').attr('hidden',true);
        $('#SiriWave').attr('hidden',false);
        eel.allCommands()()

    });

    function doc_keyUp(e) {
    const key = e.key.toLowerCase();  // Normalize just in case

    if (key === 'j' && e.metaKey) {
        console.log("✅ Command + J pressed on macOS");
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands(); // No () unless allCommands returns another function
    }
}

document.addEventListener('keyup', doc_keyUp, false);



});