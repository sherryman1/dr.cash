import random
import requests
import time

# Campaign configuration
campaigns = [

    {
        'name': 'Flexacil_ultra_message2',
        'page_id': '758550950666580',
        'user_access_token': 'EAAJgKu2x4xMBOxQAJNnapSB8pBzZCoMMtzfGUU3cNShP2dt6ZBYAsKz1WR52YDYaji3K0qTGceo9ymkKLyPNy6pgokEVjAvQv30qwhTZCXy3XMIZA8C5bgo3wl5usBmZBNjKMnWCqQZAWYCxiMqJ4CEXZBuh05G3wH8KneMaZCohX2grY1MtozFxiOW1iKc5',
        'default_images': [
            'https://drive.google.com/uc?export=view&id=1-IV6ANzPGzwrw4V0GEZHsRZssWlgbbWu', 'https://drive.google.com/uc?export=view&id=10IXmWk21RraEoff1OaGeW5z5TH8xJ5sp', 'https://drive.google.com/uc?export=view&id=16hEUzrqsGcBOYLtNnkCaa0LwfXzOsapt', 'https://drive.google.com/uc?export=view&id=1K0zv5ncpXotW7BhzDtI1afBA67fGDp0m', 'https://drive.google.com/uc?export=view&id=1NqCX-aiZ5SD50EylB53EzAddjRbxaJKF', 'https://drive.google.com/uc?export=view&id=1cO6s11iOxQja6mo2lmiCJN--ySWM8ZgP', 'https://drive.google.com/uc?export=view&id=1qNGUHMnvhsx_toAbdrWuGMQT-PwmbI2c', 'https://drive.google.com/uc?export=view&id=1qgu0ED2s9CrbICmLjnHeRrR5kYXtPEXJ'        
            ],

        'entries': [
            {
                'name': 'PERU ',
                'place_id': [
                    '614353808990299', #Lima
                    '484104844993158', #Arequipa 
                    '112643078751316', #Trujillo 
                    '229773917228058' #Chiclayo
                    ],
                'images': None,
                'message': """
Flexacil: Recupera tu libertad de movimiento 💪
💥 ¡Solo quedan 55 paquetes! – ¡50% de descuento! 🇨🇴Colombia, 🇵🇪Perú y 🇨🇱Chile
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

✔️ Alivia las molestias articulares
✔️ Nutre el cartílago y Ligamentos
✔️ Mejora la flexibilidad y la comodidad diaria
✔️ Sin inyecciones ni químicos

📝 Pedido sencillo en 3 pasos:
1️⃣ Completa el formulario
2️⃣ Espera nuestra llamada de confirmación
3️⃣ ¡Paga al recibirlo!

🎯 ¡Date prisa! Oferta válida solo para Perú, Colombia y Chile.
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

#FlexacilCápsulas #CuidadoDeCartílago #AlivioDelDolorArticular #MuéveteLibre #CuidadoNatural #SoporteArticular #AndesRelief
"""
            },
{
                'name': 'COLUMBIA ',
                'place_id': [
                    '480092272000799', #bogota
                    '116555792238945', #cALI 
                    '111841478834264', #Medellin 
                    '485526138210586' #Barranquilla-Colombia
                    ],
                'images': None,
                'message': """
Flexacil: Recupera tu libertad de movimiento 💪
💥 ¡Solo quedan 55 paquetes! – ¡50% de descuento! 🇨🇴Colombia, 🇵🇪Perú y 🇨🇱Chile
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

✔️ Alivia las molestias articulares
✔️ Nutre el cartílago y Ligamentos
✔️ Mejora la flexibilidad y la comodidad diaria
✔️ Sin inyecciones ni químicos

📝 Pedido sencillo en 3 pasos:
1️⃣ Completa el formulario
2️⃣ Espera nuestra llamada de confirmación
3️⃣ ¡Paga al recibirlo!

🎯 ¡Date prisa! Oferta válida solo para Perú, Colombia y Chile.
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

#FlexacilCápsulas #CuidadoDeCartílago #AlivioDelDolorArticular #MuéveteLibre #CuidadoNatural #SoporteArticular #AndesRelief
"""
            },
{
                'name': 'CHILE ',
                'place_id': [
                    '112371848779363', #Santiago
                    '111908478835911', #Valparaíso 
                    '100887561594526', #Concepción 
                    '121345547978791' #Puente Alto
                    ],
                'images': None,
                'message': """
Flexacil: Recupera tu libertad de movimiento 💪
💥 ¡Solo quedan 55 paquetes! – ¡50% de descuento! 🇨🇴Colombia, 🇵🇪Perú y 🇨🇱Chile
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

✔️ Alivia las molestias articulares
✔️ Nutre el cartílago y Ligamentos
✔️ Mejora la flexibilidad y la comodidad diaria
✔️ Sin inyecciones ni químicos

📝 Pedido sencillo en 3 pasos:
1️⃣ Completa el formulario
2️⃣ Espera nuestra llamada de confirmación
3️⃣ ¡Paga al recibirlo!

🎯 ¡Date prisa! Oferta válida solo para Perú, Colombia y Chile.
👉👉 https://sites.google.com/view/auto-flexacil-ultra/home

#FlexacilCápsulas #CuidadoDeCartílago #AlivioDelDolorArticular #MuéveteLibre #CuidadoNatural #SoporteArticular #AndesRelief
"""
            }
 
        ]
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

    for entry in campaign['entries']:
        message = entry['message']
        image_list = entry['images'] if entry['images'] else campaign['default_images']
        places = entry['place_id']

        for place in places:
            image = random.choice(image_list)
            print(f"📸 Posting image: {image} | 📍 Place: {place}")
            post_with_location(campaign['page_id'], token, image, place, message)
            time.sleep(2)

print("✅ All campaigns finished.")
