import PySimpleGUI as sg
from pathlib import Path
import os
import threading

threads = []

def download_song(window, target_folder, url):
    command = f'yt-dlp --extract-audio --audio-format mp3 -P "{target_folder}" -o "%(title)s.%(ext)s" "{url}" --ignore-errors'
    try:
        print("[i] Downloading...")
        window['status'].update(f'Downloading: {url}')
        window['download'].update(button_color="black")
        print(f"[i] used command: {command}")
        os.system(command)
    except Exception as error:
        print('[!] An error has been occoured')
        print(f'[x] Error: {str(error)}')
        window['status'].update('Error at Download')
        return

    window['status'].update('')
    threads.pop(0)
    if(threads):
        threads[0].start()
    else:
        window['download'].update(button_color=sg.theme_background_color())

def get_songs(window, values):
    urls = values['urls'].split('\n')
    target_folder = values['folder']

    if(not target_folder):
        print("[!] folder not provided!")
        return

    if(not urls):
        print("[!] No urls provided!")
        return

    
    print(f"[i] aim folder: {target_folder}")
    for url in urls:
        parsed_url = url.strip()
        print(f"[i] actual url: {parsed_url}")
            
        if(not url):
            print("[!] no url!")
            continue

        threads.append(threading.Thread(target=download_song, args=(window, target_folder, url,)))
    
    if(threads):
        threads[0].start()

downloads_folder = str(Path.joinpath(Path.home(), 'Downloads'))
layout = [[sg.Text("Target Folder: ")],
          [sg.InputText(key='folder', default_text=downloads_folder)],
          [sg.Text("urls: ")],
          [sg.Multiline(size=(65,20), key='urls', autoscroll=True)],
          [sg.Button('Download', key="download", disabled_button_color='gray')],
          [sg.Text("", key='status')],
          ]
actions = {'download':get_songs}
window = sg.Window('Download youtube songs', layout)

while True:
    try:

        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        
        action = actions.get(event)
        if(not action):
            print("[!] No Valid action found")
            continue
    
        print(f'[*] Recieved event: {event}')
        print(f'[*] Calling function: {action.__name__}')
        if(not threads):
            action(window, values)

    except KeyboardInterrupt:
        print("[!] Keyboard Interrupt")
        print("[x] Closing program!!")
        break

window.close()
