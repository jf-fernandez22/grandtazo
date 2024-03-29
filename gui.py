
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import pandas as pd
from fp.fp import FreeProxy
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import unicodedata

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Define the function to remove accents
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_standings():
    # ~ output_text.insert(tk.END, "Running get_positions function...\n")
    url = 'https://fbref.com/en/comps/905/Copa-de-la-Liga-Profesional-Stats'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find_all('table')

    data = []
    i = 0
    for row in table[0].find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        data.append(row_data)
    for row in table[1].find_all('tr'):
        i = i + 1
        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        if i > 1:
            data.append(row_data)

    df = pd.DataFrame(data[1:], columns=data[0])

    df['Pts'] = pd.to_numeric(df['Pts'])
    df = df.drop(['Rk'], axis = 1).sort_values(by=['Pts'], ascending = False).reset_index(drop=True)
    df['Squad'] = df['Squad'].apply(remove_accents)
    df['Squad'] = df['Squad'].str.replace(' ', '')
    df['GF'] = pd.to_numeric(df['GF'])
    df['GA'] = pd.to_numeric(df['GA'])
    df['PO'] = round((df['GF'] - df['GF'].min()) / (df['GF'].max() - df['GF'].min()), 2)
    df['PD'] = round((df['GA'] - df['GA'].max()) / (df['GA'].min() - df['GA'].max()), 2)
    
    print('Standings Updated')
    return df
    
def get_fixture(week):
    url = 'https://fbref.com/en/comps/905/schedule/Copa-de-la-Liga-Profesional-Scores-and-Fixtures'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')

    data = []
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        data.append(row_data)
        
    df = pd.DataFrame(data[1:], columns=data[0])
    group = df.groupby(['Wk'])
    dff = group.get_group(str(week))
    dff['Home'] = dff['Home'].str.replace(' ', '')
    dff['Away'] = dff['Away'].str.replace(' ', '')
    dff['Home'] = dff['Home'].apply(remove_accents)
    dff['Away'] = dff['Away'].apply(remove_accents)
    return dff[['Day', 'Time', 'Home', 'Away']]

def get_proxy():
    return {
        'http': FreeProxy().get(),
    }

def get_player_data():
    urls = ['https://fbref.com/en/squads/40bb0ce9/Independiente-Stats', 'https://fbref.com/en/squads/ef99c78c/River-Plate-Stats', 'https://fbref.com/en/squads/e2f19203/Instituto-Atletico-Central-Cordoba-Stats',
        'https://fbref.com/en/squads/d01a653b/Argentinos-Jun-Stats', 'https://fbref.com/en/squads/1d89634b/Barracas-Central-Stats', 'https://fbref.com/en/squads/ceda2145/Talleres-Stats',
        'https://fbref.com/en/squads/41c139b6/Velez-Sarsfield-Stats', 'https://fbref.com/en/squads/950a95f2/Gimnasia-ELP-Stats', 'https://fbref.com/en/squads/87a920fa/Rosario-Cent-Stats',
        'https://fbref.com/en/squads/8a9d5afa/Independiente-Rivadavia-Stats', 'https://fbref.com/en/squads/1d3d37ae/CA-Huracan-Stats', 
        'https://fbref.com/en/squads/b3d222b1/Deportivo-Riestra-Stats', 'https://fbref.com/en/squads/06c1606c/Banfield-Stats',
        'https://fbref.com/en/squads/42a1ab8b/Tucuman-Stats', 'https://fbref.com/en/squads/ac9a09b4/Godoy-Cruz-Stats',
        'https://fbref.com/en/squads/df734df9/Estudiantes-Stats', 'https://fbref.com/en/squads/11b6dba8/Lanus-Stats', 'https://fbref.com/en/squads/9bf4eaf4/Newells-OB-Stats',
        'https://fbref.com/en/squads/a4570206/Defensa-y-Just-Stats', 'https://fbref.com/en/squads/8e20e13d/Racing-Club-Stats',
        'https://fbref.com/en/squads/795ca75e/Boca-Juniors-Stats', 'https://fbref.com/en/squads/5adc7e67/CA-Union-Stats', 'https://fbref.com/en/squads/66da6009/San-Lorenzo-Stats',
        'https://fbref.com/en/squads/3cbfa767/Platense-Stats', 'https://fbref.com/en/squads/7765008b/Club-Atletico-Belgrano-Stats',
        'https://fbref.com/en/squads/9aa97c75/CC-Cordoba-Stats', 'https://fbref.com/en/squads/e9ae80b7/Sarmiento-Stats',
        'https://fbref.com/en/squads/0e92bf17/Tigre-Stats']
    pb1 = tqdm(total=len(urls), desc="Descargando Datos de Jugadores")
    for url in urls:
        team = url.split('/')[-1].split('Stats')[0].replace('-', '')
        try:
            response = requests.get(url, proxies=get_proxy())
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            data = []
            for row in table.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                data.append(row_data)
            df = pd.DataFrame(data[2:], columns=data[1])
            df['team'] = team
            if 'Belgrano' in url.split('/')[-1].split('-'):
                df.to_csv('./stats/Belgrano_stats.csv')
            elif 'Newells' in url.split('/')[-1].split('-'):
                df.to_csv('./stats/Newell\'\sOB_stats.csv')
            elif 'InstitutoAtleticoCentralCordoba' in url.split('/')[-1].replace('-',''):
                df.to_csv('./stats/Instituto_stats.csv')
            else:
                df.to_csv('./stats/' + team + '_stats.csv')
            pb1.update(1)
        except Exception as e:
            print('Error:', e)

def show_standings():
    standings_df = get_standings()
    entry_2.delete(1.0, tk.END)  # Clear previous text
    entry_2.insert(tk.END, standings_df[['Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].to_string(index=False))
          
def show_fixture():
    week = int(entry_week.get())
    fixture_df = get_fixture(week)
    entry_1.delete(1.0, tk.END)  # Clear previous text
    entry_1.insert(tk.END, fixture_df.to_string(index=False))
    
def get_opponent_and_location(team, fixture_df):
    # Find rows where the team is either home or away
    team_home = fixture_df[fixture_df['Home'] == team]
    team_away = fixture_df[fixture_df['Away'] == team]

    # Check if the team is playing home or away
    if not team_home.empty:
        return team_home['Away'].iloc[0], 1
    elif not team_away.empty:
        return team_away['Home'].iloc[0], 0
    else:
        return None, None 

def score_gk(team, rival, teamstats, std, f1, f2, f3, local, fecha):
    dp = std[std['Squad']==team]['PD'].values[0]
    op = std[std['Squad']==rival]['PO'].values[0]
    gks = teamstats[(teamstats['Pos'] == 'GK') & (teamstats['Min'] > 0)]
    dfs = []
    for idx, row in gks.iterrows():
        score = dp*f1 + local*f2 - op*f3
        minutos = row[7]/((fecha-1)*90)
        if team == 'IndependienteRivadavia':
            team = 'IndRivadavia'
        df0 = pd.DataFrame({'Jugador': [row[1]], 'Equipo': [team], 'Score': [round(score,3)], 'Minutos': [round(minutos,2)*100]})
        dfs.append(df0)
    df = pd.concat(dfs)
    return df

def score_def(team, rival, teamstats, std, f1, f2, f3, f4, f5, f6, local, fecha):
    dp = std[std['Squad']==team]['PD'].values[0]
    opt = std[std['Squad']==team]['PO'].values[0]
    opr = std[std['Squad']==rival]['PO'].values[0]
    defs = teamstats[(teamstats['Pos'] == 'DF') & (teamstats['Min'] > 0)]
    dfs = []
    for idx, row in defs.iterrows():
        minutos = row[7]/((fecha-1)*90)
        golespp = row[9] * 90 / row[7]
        amarillaspp = row[15] * 90 / row[7]
        rojaspp = row[16] * ((fecha-1)*90) / row[7]
        score = dp*f1 + local*f2 + golespp*f3 - amarillaspp*f4 - rojaspp*f5 - opr*f6
        if team == 'IndependienteRivadavia':
            team = 'IndRivadavia'
        df0 = pd.DataFrame({'Jugador': [row[1]], 
                            'Equipo': [team], 
                            'Score': [round(score, 3)], 
                            'Minutos': [round(minutos * 100, 2)],
                            'Golespp': [round(golespp, 3)],
                            'Amarillaspp': [round(amarillaspp, 3)],
                            'Rojaspp': [round(rojaspp, 3)]})
        dfs.append(df0)
    df = pd.concat(dfs)
    return df

def score_mf(team, rival, teamstats, std, f1, f2, f3, f5, f6, f7, local, fecha):
    opt = std[std['Squad']==team]['PO'].values[0]
    dpr = std[std['Squad']==rival]['PD'].values[0]
    meds = teamstats[(teamstats['Pos'] == 'MF') & (teamstats['Min'] > 0)]
    dfs = []
    for idx, row in meds.iterrows():
        minutos = row[7]/((fecha-1)*90)
        golespp = row[9] * 90 / row[7]
        asistpp = row[10] * 90 / row[7]
        amarillaspp = row[15] * 90 / row[7]
        rojaspp = row[16] * ((fecha-1)*90) / row[7]
        score = opt*f1 + local*f2 + golespp*f3 - amarillaspp*f5 - rojaspp*f6 - dpr*f7
        if team == 'IndependienteRivadavia':
            team = 'IndRivadavia'
        df0 = pd.DataFrame({'Jugador': [row[1]], 
                            'Equipo': [team], 
                            'Score': [round(score, 3)], 
                            'Minutos': [round(minutos * 100, 2)],
                            'Golespp': [round(golespp, 3)],
                            'Asistpp': [round(asistpp, 3)],
                            'Amarillaspp': [round(amarillaspp, 3)],
                            'Rojaspp': [round(rojaspp, 3)]})
        dfs.append(df0)
    df = pd.concat(dfs)
    return df

def score_del(team, rival, teamstats, std, f1, f2, f3, f4, f5, f6, f7, local, fecha):
    opt = std[std['Squad']==team]['PO'].values[0]
    dpr = std[std['Squad']==rival]['PD'].values[0]
    dels = teamstats[(teamstats['Pos'] == 'FW') & (teamstats['Min'] > 0)]
    dfs = []
    for idx, row in dels.iterrows():
        minutos = row[7]/((fecha-1)*90)
        golespp = row[9] * 90 / row[7]
        asistpp = row[10] * 90 / row[7]
        amarillaspp = row[15] * 90 / row[7]
        rojaspp = row[16] * ((fecha-1)*90) / row[7]
        score = opt*f1 + local*f2 + golespp*f3 + asistpp*f4 - amarillaspp*f5 - rojaspp*f6 - dpr*f7
        if team == 'IndependienteRivadavia':
            team = 'IndRivadavia'
        df0 = pd.DataFrame({'Jugador': [row[1]], 
                            'Equipo': [team], 
                            'Score': [round(score, 3)], 
                            'Minutos': [round(minutos * 100, 2)],
                            'Golespp': [round(golespp, 3)],
                            'Asistpp': [round(golespp, 3)],
                            'Amarillaspp': [round(amarillaspp, 3)],
                            'Rojaspp': [round(rojaspp, 3)]})
        dfs.append(df0)
    df = pd.concat(dfs)
    return df

def analyze(fec, week, std):
    arqs = []
    defs = []
    meds = []
    dels = []
    for teamstats in os.listdir('./stats'):
        team = teamstats.split('_')[0]
        if teamstats != '.ipynb_checkpoints':
            df = pd.read_csv('./stats/'+teamstats)
            try:
                rival, local = get_opponent_and_location(team, fec)
                arqs.append(score_gk(team, rival, df, std, 0.5, 0.2, 0.6, local, week))
                defs.append(score_def(team, rival, df, std, 0.6, 0.3, 0.8, 0.6, 0.6, 0.5, local, week))
                meds.append(score_mf(team, rival, df, std, 0.7, 0.1, 0.9, 0.6, 0.5,0.3, local, week))
                dels.append(score_del(team, rival, df, std, 0.7, 0.1, 0.8, 0.5, 0.5, 0.5,0.5, local, week))
                #print('Listo: '+team)
            except Exception as e:
                print(team, e)
    arq = pd.concat(arqs)
    df = pd.concat(defs)
    med = pd.concat(meds)
    dl = pd.concat(dels)
    
    return arq, df, med, dl

def show_analysis():
    week = int(entry_week.get())
    fixture_df = get_fixture(week)
    std = get_standings()
    arq, df, med, dl = analyze(fixture_df, week, std)
    selected_columns = ['Jugador', 'Equipo', 'Score']
    entry_3.delete(1.0, tk.END)  # Clear previous text
    entry_3.insert(tk.END, arq[arq['Minutos'] > 50].sort_values(by=['Score'], ascending= False)[selected_columns].head(25).to_string(index=False))
    entry_4.delete(1.0, tk.END)  # Clear previous text
    entry_4.insert(tk.END, df[df['Minutos'] > 50].sort_values(by=['Score'], ascending= False)[selected_columns].head(25).to_string(index=False))
    entry_5.delete(1.0, tk.END)  # Clear previous text
    entry_5.insert(tk.END, med[med['Minutos'] > 50].sort_values(by=['Score'], ascending= False)[selected_columns].head(25).to_string(index=False))
    entry_6.delete(1.0, tk.END)  # Clear previous text
    entry_6.insert(tk.END, dl[dl['Minutos'] > 50].sort_values(by=['Score'], ascending= False)[selected_columns].head(25).to_string(index=False))
    
    
window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    720.0,
    512.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    1154.5,
    329.5,
    image=entry_image_1
)
# ~ canvas.place(x = 0, y = 0)

canvas.place(x = 0, y = 0)
# ~ image_image_1 = PhotoImage(
    # ~ file=relative_to_assets("image_1.png"))
# ~ image_1 = canvas.create_image(
    # ~ 1024.0,
    # ~ 1440.0,
    # ~ image=image_image_1
# ~ )


entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    1154.5,
    329.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_1.place(
    x=969.0,
    y=123.0,
    width=371.0,
    height=411.0
)

canvas.create_text(
    1029.0,
    78.0,
    anchor="nw",
    text="Fecha Actual",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    719.5,
    329.5,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_2.place(
    x=534.0,
    y=123.0,
    width=371.0,
    height=411.0
)

canvas.create_text(
    594.0,
    78.0,
    anchor="nw",
    text="Posiciones",
    fill="#FFFFFF",
    font=("Inter", 32 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    196.5,
    797.5,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_3.place(
    x=33.0,
    y=610.0,
    width=327.0,
    height=373.0
)

canvas.create_text(
    54.0,
    567.0,
    anchor="nw",
    text="Mejores Arqueros",
    fill="#000000",
    font=("Inter", 32 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    547.5,
    797.5,
    image=entry_image_4
)
entry_4 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_4.place(
    x=384.0,
    y=610.0,
    width=327.0,
    height=373.0
)

canvas.create_text(
    405.0,
    567.0,
    anchor="nw",
    text="Mejores Defensores",
    fill="#000000",
    font=("Inter", 32 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    899.0,
    797.5,
    image=entry_image_5
)
entry_5 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_5.place(
    x=735.0,
    y=610.0,
    width=328.0,
    height=373.0
)

canvas.create_text(
    756.0,
    567.0,
    anchor="nw",
    text="Mejores Medios",
    fill="#000000",
    font=("Inter", 32 * -1)
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    1242.5,
    797.5,
    image=entry_image_6
)
entry_6 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 9)
)
entry_6.place(
    x=1079.0,
    y=610.0,
    width=327.0,
    height=373.0
)

canvas.create_text(
    1100.0,
    567.0,
    anchor="nw",
    text="Mejores Delanteros",
    fill="#000000",
    font=("Inter", 32 * -1)
)
button_image_0 = PhotoImage(
    file=relative_to_assets("jugs.png"))
button_0 = Button(
    image=button_image_0,
    borderwidth=0,
    highlightthickness=0,
    command=get_player_data,
    relief="flat"
)
button_0.place(
    x=33.0,
    y=13.0,
    width=369.0,
    height=100.0
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=show_standings,
    relief="flat"
)
button_1.place(
    x=33.0,
    y=153.0,
    width=369.0,
    height=100.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
entry_week = tk.Entry(
)
entry_week.place(
    x=413.0,
    y=292.0,
    width=72.0,
    height=75.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=show_fixture,
    relief="flat"
)
button_3.place(
    x=33.0,
    y=279.0,
    width=369.0,
    height=100.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=show_analysis,
    relief="flat"
)
button_4.place(
    x=33.0,
    y=397.0,
    width=369.0,
    height=100.0
)
window.resizable(False, False)
window.mainloop()
