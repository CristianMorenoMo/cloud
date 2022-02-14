from pydub import AudioSegment
import os
path_audio = os.path.abspath(os.curdir) + '/uploads/dialog_song_convert/'
path_audio_convert  = os.path.abspath(os.curdir) + '/uploads/dialog_song_convert/'


1. consultar en la base de datos de propust todos los adios que aun no han sido convertidos
2. traer todos los nombres y  buscarlos en el path
3. pasar cada unos de los audios en la funcion
4. validar que los audios fueron convertidos
5. hacer un update de los audios que fueron convertidso en la tabla proposal.



arr = os.listdir(path_audio)
format= arr[0].split('.')[-1]
name = arr[0].split('.')[0]

def convert_audio(input_path,out_path,format_input):
    given_audio = AudioSegment.from_file(path_audio + arr[0], format=format)
    given_audio.export(path_audio_convert + arr[0], format="mp3")

