#CREATE DATABASE lyriquest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
/*
USE lyriquest_db;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profile_picture VARCHAR(255)
);
CREATE TABLE music_track (
    track_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    audio_file VARCHAR(255) NOT NULL,
    artwork VARCHAR(255),
    lyrics TEXT
);
CREATE TABLE emotion (
    emotion_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE music_track_emotion (
    track_id INT,
    emotion_id INT,
    PRIMARY KEY (track_id, emotion_id),
    FOREIGN KEY (track_id) REFERENCES music_track(track_id),
    FOREIGN KEY (emotion_id) REFERENCES emotion(emotion_id)
);
CREATE TABLE playlist (
    playlist_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    playlist_name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE playlist_track (
    playlist_id INT,
    track_id INT,
    PRIMARY KEY (playlist_id, track_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
    FOREIGN KEY (track_id) REFERENCES music_track(track_id)
);
*/
INSERT INTO users (username, email, password)
VALUES ('testuser', 'test@example.com', '123456');
INSERT INTO music_track (title, artist, audio_file, lyrics)
VALUES ('My Song', 'My Artist', 'music/audio/mysong.mp3', 'This is my song lyrics...');
INSERT INTO emotion (name)
VALUES ('Радость');
INSERT INTO emotion (name)
VALUES ('Грусть');

INSERT INTO music_track_emotion (track_id, emotion_id)
VALUES (1, 1); -- Трек 1 (My Song) связан с эмоцией 1 (Радость)
INSERT INTO playlist (user_id, playlist_name)
VALUES (1, 'My Favorites');
INSERT INTO playlist_track (playlist_id, track_id)
VALUES (1, 1);