console.log("Sanity check from movie.js.");

const movieId = JSON.parse(document.getElementById('movieId').textContent); // ID фильма, который просматривают участники
const videoElement = document.getElementById("movie"); // HTML элемент видео
const socket = new WebSocket(`ws://${window.location.host}/ws/movie/${movieId}/`);

let userInteracted = false;

// Прослушивание события изменения времени в видео
videoElement.ontimeupdate = function () {
    socket.send(JSON.stringify({
        action: "sync",
        time: videoElement.currentTime
    }));
};

videoElement.addEventListener("seeked", function (event) {
    socket.send(JSON.stringify({
        action: "seek",
        time: event.target.currentTime
    }));
});

videoElement.addEventListener("pause", function () {
    socket.send(JSON.stringify({
        action: "pause"
    }));
});

videoElement.addEventListener("play", function () {
    socket.send(JSON.stringify({
        action: "play"
    }));
});

document.addEventListener("click", function () {
    userInteracted = true;
});

// Слушать сообщения о подключении
socket.onopen = function () {
    if (!document.getElementById('userId')) {
        return;
    }
    // Отправить сигнал со стороны клиента для получения текущего времени
    socket.send(JSON.stringify({
        action: "request_time"
    }));
}

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.action === "sync") {
        videoElement.currentTime = data.time;
    } else if (data.action === "play") {
        if (userInteracted) {
            videoElement.play();
        }
    } else if (data.action === "pause") {
        videoElement.pause();
    } else if (data.action === "seek") {
        videoElement.currentTime = data.time;
    } else if (data.action === "time") { // действие времени
        videoElement.currentTime = data.time;
    } else if (data.action === "get_current_time") {
        videoElement.currentTime = data.time;
        videoElement.play(); // проверить с какого момента запускается
    }
};
