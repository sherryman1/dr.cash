import random
import requests
import time

# ✅ Campaign configuration for Difort
campaigns = [
    {
        'name': 'Cardiotone-message1',
        'page_id': '645888668615183',
        'user_access_token': 'EAAOfZBBEKyBgBO0NDFJAJJ9OqscKTvZAKfNXuOZCnG0njeh79x50iXHUpzQo9Td41da6tVavrfGIiBxJfqXC1JcLOxruliC4pQZAgpZBdhwlb3ZAYAHQRZCsPTV8CiWVYbaITpjdkM4tCNHKBhtpocl6LJYbaQvzrRUjXOdQZCfZB89OqNNSDJ1XZCoKaoZA39c',
        'place_ids': [
'480092272000799', #bogota
'116555792238945', #cALI 
'111841478834264', #Medellin 
'485526138210586', #Barranquilla-Colombia
'385204625657774' #Cartagena, Colombia
        ],
        'images': [
'https://drive.google.com/uc?export=view&id=18qlEujV9yi5sdmbFlQ6_Es8XF2y1f6dN', 'https://drive.google.com/uc?export=view&id=1YLKS_zm3wSAM_NtDMQ_IibVSO5jE7Can', 'https://drive.google.com/uc?export=view&id=1ieAP3yJ_sXnSG7VgElsFLDmR75Xml67Z'     
        ],
        'message': '''
Cuida tu corazón de forma natural ❤️
Tu corazón podría estar pidiendo ayuda 💔
Cardioton ayuda a mantener una presión arterial normal, fortalecer el corazón y promover una mejor circulación. 🌿
🎉 SOLO HOY: ¡50% de descuento! ¡Solo 159,000 COP!
👉 👉 https://sites.google.com/view/auto-carditone/home

🌟 ¿Qué hace único a Cardioton?
✅ Ayuda a mantener una presión arterial saludable
✅ Favorece la energía, la calma y el bienestar cardíaco
✅ Recomendado por médicos | Sin receta
✅ Suave y seguro, incluso para adultos mayores

Da un paso hacia un corazón más fuerte.
👉 👉 https://sites.google.com/view/auto-carditone/home
🚚 Entrega en 1 a 5 días | 💰 Pago contra entrega

#Cardioton #SaludCorazón #ApoyoNatural #ImpulsoCirculación #CorazónSaludable #Colombia
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
