let mediaRecorder;
let audioChunks = [];

document.getElementById("newQuestion").onclick = async function() {
    let response = await fetch("/get_question");
    let data = await response.json();
    document.getElementById("question").innerText = data.question;
};

document.getElementById("startRecording").onclick = async function() {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        let audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        let formData = new FormData();
        formData.append("audio", audioBlob, "audio.webm");

        let response = await fetch("/process_audio", { method: "POST", body: formData });
        let result = await response.json();

        document.getElementById("feedback").innerText = "Feedback: " + result.feedback;
        document.getElementById("audioPlayback").src = URL.createObjectURL(audioBlob);
    };

    mediaRecorder.start();
    document.getElementById("startRecording").disabled = true;
    document.getElementById("stopRecording").disabled = false;
};

document.getElementById("stopRecording").onclick = function() {
    mediaRecorder.stop();
    document.getElementById("startRecording").disabled = false;
    document.getElementById("stopRecording").disabled = true;
};
