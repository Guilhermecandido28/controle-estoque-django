import requests
from bs4 import BeautifulSoup


def obter_url_foto_perfil(usuario_instagram):
    url = f"https://www.instagram.com/{usuario_instagram}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        profile_picture_url = soup.find('meta', {'property': 'og:image'})['content']                
        return profile_picture_url
    else:
        print('Erro ao acessar o perfil do Instagram')
        return None

obter_url_foto_perfil('vivimbk')
