import requests
import base64
import json

# Datos de auth. (acuerdate de borrarlos)
CLIENT_ID = ''
CLIENT_SECRET = ''

ENDPOINT = 'https://api.spotify.com/v1/artists/'

# Id de los grupos de musica. Obtenido a traves del propio enlace del artista en la version web. 
id_oasis = '2DaxqgrOhkeH0fpeiQq2f4'
id_linkin_park = '6XyY86QOPPrYVGvF9ch6wz'

# Metodo que obtiene el token del usuario
def obtener_token():
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type':'client_credentials'
    }
    response = requests.post(url, data=data, auth=(CLIENT_ID,CLIENT_SECRET))    
    token = response.json().get("access_token")
    return token

def obtener_info_artista(id_artista, token):    
    url = f'https://api.spotify.com/v1/artists/{id_artista}'
    headers = {
        'Authorization':f'Bearer {token}'
    }
    reponse = requests.get(url,headers=headers)
    return reponse.json()

def obtener_top_tracks(id_artista, token):
    url = f'https://api.spotify.com/v1/artists/{id_artista}/top-tracks?market=ES'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def comparar_valores(oasis_stat,linkin_park_stat, puntuacion):
    o_puntuacion, lp_puntuacion = puntuacion
    if(oasis_stat > linkin_park_stat):
        o_puntuacion += 1
    elif(oasis_stat < linkin_park_stat):
        lp_puntuacion += 1
    return o_puntuacion,lp_puntuacion

def comparar_canciones(oasis_top_tracks, linkin_park_top_tracks, estadistica):
    o_puntuacion,lp_puntuacion = estadistica
    oasis_1_top_track = oasis_top_tracks['tracks'][0]['popularity']
    linkin_1_top_track = linkin_park_top_tracks['tracks'][0]['popularity']
    print (f" - Oasis [1]: {oasis_top_tracks['tracks'][0]['name']}, Popularidad {oasis_1_top_track}")
    print (f" - Linkin Park [1]: {linkin_park_top_tracks['tracks'][0]['name']}, Popularidad {linkin_1_top_track}")

    oasis_2_top_track = oasis_top_tracks['tracks'][1]['popularity']
    linkin_2_top_track = linkin_park_top_tracks['tracks'][1]['popularity']
    print (f" - Oasis [2]: {oasis_top_tracks['tracks'][1]['name']}, Popularidad {oasis_2_top_track}")
    print (f" - Linkin Park [2]: {linkin_park_top_tracks['tracks'][1]['name']}, Popularidad {linkin_2_top_track}")
    if(oasis_1_top_track > linkin_1_top_track):
        o_puntuacion += 1
    elif (oasis_1_top_track < linkin_1_top_track):
        lp_puntuacion += 1
    
    if(oasis_2_top_track > linkin_2_top_track):
        o_puntuacion += 1
    elif(oasis_2_top_track < linkin_2_top_track):
        lp_puntuacion += 1
    
    return o_puntuacion, lp_puntuacion

def main():
    token = obtener_token()  
    oasis_info = obtener_info_artista(id_artista=id_oasis,token=token)
    linkin_park_info = obtener_info_artista(id_artista=id_linkin_park,token=token)    

    oasis_top_tracks = obtener_top_tracks(id_oasis, token)
    linkin_park_top_tracks = obtener_top_tracks(id_linkin_park, token)

    oasis_followers = oasis_info['followers']['total']
    oasis_popularity = oasis_info['popularity']
    
    linkin_park_followers = linkin_park_info['followers']['total']
    linkin_park_popularity = linkin_park_info['popularity']

    print("Comparar followers Oasis / Linkin Park")
    print(f" - Oasis: {oasis_followers}")
    print(f" - Linkin Park: {linkin_park_followers}")
    estadistica = comparar_valores(oasis_followers, linkin_park_followers,(0,0))    
    print("Comparar popularidad Oasis / Linkin Park")
    print(f" - Oasis: {oasis_popularity}")
    print(f" - Linkin Park: {linkin_park_popularity}")
    estadistica = comparar_valores(oasis_popularity, linkin_park_popularity, estadistica)
    
    print("Comparar popularidad canciones Oasis / Linkin Park")
    estadistica = comparar_canciones(oasis_top_tracks, linkin_park_top_tracks, estadistica)
    
    o_puntuacion, l_puntuacion = estadistica

    print (f"Banda mas popular: {'Oasis' if o_puntuacion > l_puntuacion else 'Linkin Park'}")
    
if __name__ == '__main__':
    main() 