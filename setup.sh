#!/bin/sh

printf "Adding yt-dlp repository...\n\n"
sudo add-apt-repository ppa:tomtomtom/yt-dlp
printf "Updating packages....\n\n"
sudo apt update && sudo apt upgrade
printf "Installig ffmepg && yt-dlp...\n\n"
sudo apt install ffmpeg yt-dlp 
