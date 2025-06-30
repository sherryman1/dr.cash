import random
import requests
import time

# ✅ Campaign configuration for Difort
campaigns = [
    {
        'name': 'DIFORT-message1',
        'page_id': '683824754817425',
        'user_access_token': 'EAAlWcWKxteoBO0QwZAefNolmWShAAlnPUqZBHJaLPZA5KzaklejUhRUokUXsRmZBNKtMe4u8UaeIfP0NpDqZBFzJwxWYnhLLPzo2sNx5ZBa3kVmjeHY0rPYySVvSd8T83ubtbu0QaXeGse33jeZAdyNnQSniroZCpQTP4ZCYiJAxvab6ZCjCI2pjNKIyb6js5U',
        'place_ids': [
'109318109087339',#puebla city
'109486839070556',#mexico
'114897945188014',#mexico city
'111939165490631',#tijuana
'298956890297260',#leon
'198130383580063',#Ecatepec
'104116582957771',#juarez
'112228142122051',#Zapopan
'103982989637871',#guadalajara
'110852402276862',#monterrey
'110846342273459',#nezahualcoyotl
'111820335503160',#mexicali
'110885848932443',#queretaro
'106152312753526',#culiacan
        ],
        'images': [
'https://drive.google.com/uc?export=view&id=13XCIcjn2yMfCFFJQPdXOe6ra5TOKjIsk', 'https://drive.google.com/uc?export=view&id=1RyDPfmZ2UXrjvyjoLU2NDId_wGcHdm3w', 'https://drive.google.com/uc?export=view&id=1V6YTg9UEjkTFzz7oyyg8qSgjTNqCHHCS', 'https://drive.google.com/uc?export=view&id=1VvwhbkBOAqBXiHQCUnW6CqtsPrNIkA6Q', 'https://drive.google.com/uc?export=view&id=1bkzcQFOAF0cb9q37qi-xjSQ-5aCmIKzx', 'https://drive.google.com/uc?export=view&id=1foqVbndK8vlfWjaEytOMrtnPDbBQkbYN', 'https://drive.google.com/uc?export=view&id=1iIyp_4D_IM0tME7SOuPqHrVV5jLkK3OW', 'https://drive.google.com/uc?export=view&id=1nKpVwzUw1mWPFlnS6JlWPMVejefuoiAQ'
        ],
        'message': '''
Siéntete en equilibrio de nuevo — Naturalmente con Difort🌿
¿Te cuesta mantener tus niveles de azúcar bajo control?
🎉 ¡Solo hoy: Descuento por tiempo limitado!
👉 👉 https://sites.google.com/view/auto-difort/home

🌿 Con ingredientes como moringa, neem y nopal
✅ Favorece un metabolismo saludable del azúcar
✅ Ayuda a reducir el estrés, la ansiedad y los antojos
✅ Favorece un sueño reparador y una mayor claridad cognitiva
✅ Recomendado por médicos | Sin receta

Recupera tu equilibrio: ¡pídelo ya!
👉 👉 https://sites.google.com/view/auto-difort/home
🚚 Entrega rápida | 💳 Pago contra entrega

#ApoyoNatural #EquilibrioDeAzúcar #BienestarDifort #CuidadoDeDiabetes #AlivioDelEstrés #VidaSaludable #méxico
        '''
    }
]

def get_page_access_token(page_id, user_token):
    url = f'https://graph.facebook.com/v20.0/{page_id}?fields=access_token&access_token={user_token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        print(f"❌ Error retrieving access token for page {page_id}: {e}")
        return None

def post_with_location(page_id, token, image_url, place_id, message):
    photo_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'
    photo_payload = {
        'access_token': token,
        'url': image_url,
        'published': 'false'
    }
    photo_response = requests.post(photo_url, data=photo_payload)
    if photo_response.status_code != 200:
        print(f"❌ Failed to upload photo: {photo_response.text}")
        return

    photo_id = photo_response.json().get('id')
    if not photo_id:
        print("❌ No photo ID returned.")
        return

    feed_url = f'https://graph.facebook.com/v20.0/{page_id}/feed'
    feed_payload = {
        'access_token': token,
        'message': message,
        'place': place_id,
        'attached_media': [{'media_fbid': photo_id}]
    }
    feed_response = requests.post(feed_url, json=feed_payload)
    if feed_response.status_code == 200:
        print(f"✅ Post successful at place {place_id}")
    else:
        print(f"❌ Failed to post to feed: {feed_response.status_code} {feed_response.text}")

# 🚀 Start posting
for campaign in campaigns:
    print(f"\n📢 Starting campaign: {campaign['name']}")
    token = get_page_access_token(campaign['page_id'], campaign['user_access_token'])

    if not token:
        print(f"❌ Skipping campaign {campaign['name']} due to token issue.")
        continue

    place_ids = campaign['place_ids'][:]
    images = campaign['images'][:]

    while place_ids:
        place = random.choice(place_ids)
        place_ids.remove(place)

        image = random.choice(images)
        print(f"📸 Posting image: {image} | 📍 Place: {place}")
        post_with_location(campaign['page_id'], token, image, place, campaign['message'])
        time.sleep(2)

print("✅ All campaigns finished.")
