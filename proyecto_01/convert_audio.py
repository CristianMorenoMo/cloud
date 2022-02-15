import sqlite3 as sql
import os
from pydub import AudioSegment


path = os.path.abspath(os.curdir)
path_input = path + '/uploads/dialog_song/'
path_output = path + '/uploads/dialog_song_convert/'

print(path)
sqlconnection = sql.connect(path + '/database/proyecto_01.db')
cursor = sqlconnection.cursor()

query='''
select id_proposal,
       dialogo_sound
from proposal
-- where state_voice = 'in process';
'''
cursor.execute(query)
records = cursor.fetchall()
id_proposal = []
name_file = []
columnNames=[column[0] for column in cursor.description]
for record in records:
    id_proposal.append(record[0])
    name_file.append(record[1])

name_file_search = name_file[:30]
arr = os.listdir(path + '/uploads/dialog_song')
##name_file_search in arr

def convert_audio(input_path,out_path,file):
    format = file.split('.')[-1]
    name_file = file.split('.')[0]
    given_audio = AudioSegment.from_file(input_path + file, format=format)
    given_audio.export(out_path + name_file+'.mp3', format="mp3")

for file in name_file_search:
    convert_audio(path_input, path_output, file)

query_update=f'''
UPDATE proposal
SET state_voice = 'convert'
WHERE id_proposal in {id_proposal};
'''
print(query_update)