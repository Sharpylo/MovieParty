console.log("Sanity check from movie.js.");

const movieId = JSON.parse(document.getElementById('movieId').textContent); // ID фильма, который просматривают участники
const videoElement = document.getElementById("movie"); // HTML элемент видео
const socket = new WebSocket(`ws://${window.location.host}/ws/movie/${movieId}/`);

// Прослушивание события изменения времени в видео
videoElement.ontimeupdate = function () {
    socket.send(JSON.stringify({
        action: "sync",
        time: videoElement.currentTime
    }));
};

// Слушать сообщения о подключении
socket.onopen = function () {
    // Отправить сигнал со стороны клиента для получения текущего времени
    socket.send(JSON.stringify({
        action: "play"
    }));
}

// Прослушивание сообщений из сокета
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.action === "sync") {
        videoElement.currentTime = data.time;
    } else if (data.action === "play") {
        videoElement.play();
    } else if (data.action === "pause") {
        videoElement.pause();
    } else if (data.action === "seek") {
        videoElement.currentTime = data.time;
    }
};

videoElement.addEventListener("seeked", function () {
    socket.send(JSON.stringify({
        action: "seek",
        time: videoElement.currentTime
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