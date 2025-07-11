$(document).ready(function () {

    eel.init()();

    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" }
    });

    // siri config
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true,
    });

    // siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true }
    });

    // Mic button click event (fixed ID case and call)
    $('#MicBtn').on('click', function () {
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands();  // ← fixed: no double parentheses
    });

    function doc_keyUp(e) {
        const key = e.key.toLowerCase();
        if (key === 'j' && e.metaKey) {
            console.log("✅ Command + J pressed on macOS");
            eel.playAssistantSound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands();
        }
    }




    document.addEventListener('keyup', doc_keyUp, false);

    // Play assistant function
    function PlayAssistant(message) {
        if (message.trim() !== "") {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    $("#chatbox").keypress(function (e) {
        if (e.which == 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

});
