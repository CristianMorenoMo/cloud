import sqlite3 as sql
import os
from pydub import AudioSegment
import yagmail


def convert_audio(input_path, out_path, file):
    format = file.split('.')[-1]
    name_file = file.split('.')[0]
    given_audio = AudioSegment.from_file(input_path + file, format=format)
    given_audio.export(out_path + name_file + '.mp3', format="mp3")
    print(f'completado:{name_file}')

path = os.path.abspath(os.curdir)
path_input = path + '/static/uploads/dialog_song/'
path_output = path + '/static/uploads/dialog_song_convert/'

print(path)
sqlconnection = sql.connect(path + '/database/proyecto_01.db')
cursor = sqlconnection.cursor()

query='''
select id_proposal,
       dialogo_sound,
       email
from proposal
where state_voice = 'in process';
'''
query_update = '''
    UPDATE proposal
    SET state_voice = 'convert', dialogo_sound_convert ="{name_file}", formato="mp3"
    WHERE id_proposal = CAST("{id}" as INT);
    '''

cursor.execute(query)
records = cursor.fetchall()
if not records:
    print('no existen audios para convertir')
else:
    id_proposal = []
    name_file = []
    email_users=[]
    columnNames=[column[0] for column in cursor.description]
    for record in records:
        id_proposal.append(record[0])
        name_file.append(record[1])
        email_users.append(record[2])

    name_file_search = name_file[:30]
    arr = os.listdir(path + '/static/uploads/dialog_song')

    if all([i in arr for i in name_file_search]):
        i=0
        for row in name_file_search:
            name_file= row.split('.')[0] + '.mp3'
            convert_audio(path_input, path_output, row)
            query_update_f = query_update.format(name_file =name_file,
                                                 id =id_proposal[i])
            print(query_update_f)
            cursor.execute(query_update_f)
            sqlconnection.commit()
            print('update file')
            email = 'semestrecloud2022@gmail.com'
            password = 'Semestre2022cloud'
            yag = yagmail.SMTP(email,password)
            yag.send(email_users[i],
                     'Audio convertido',
                     ['Audio convertido'])
            print('email enviado')
            i = i+1

