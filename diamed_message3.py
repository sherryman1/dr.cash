import random
import requests
import time

# Configurations for each campaign
campaigns = [ 
    {
        'name': 'Diamed - message 3',
        'page_id': '667776219757335',
        'place_ids': [
            '106287062743373', #barcelona
            '106504859386230',  #Madrid
            '111812165504902',  #seville
            '111939165490631',  #tijuana
            '114897945188014',  #mexico city
            '103982989637871',  #Guadalajara
            '587956921701546',  #Durango
            '110852402276862',  #Monterrey
        ],
        'user_access_token': 'EAAKimZAyg6mcBOxNt4GTjAVTLFcdFk3OAWbCUkp2odBIlZCZCX5LdMlpe2nkyRqtGylIqOqc9LjGqa8Q20vjV7WMIlZAMGqO6mXI5CGjk9eviYn8fZAkLQEfN8Ao3SVdW564Ed265O7cZCqz25sEooFp7uDyEuGdVvYtljZAmzZBTcuYpGjaGiSOqIWBRMS1',
        'default_images': [
            'https://drive.google.com/uc?export=view&id=1PhjNRZ_H-B_qpIml01igI1raVkHCFRwr',
            'https://drive.google.com/uc?export=view&id=1Yr3EhSaRyJYnSxGn2cErD93kNvzV4Ceh',
            'https://drive.google.com/uc?export=view&id=1lBRrc-vhkz8tomBk2Cugc5q4R6tICGVs',
            'https://drive.google.com/uc?export=view&id=1mB3S4abv8sphjsQxVCXXNk83BCMbyCHS',
            'https://drive.google.com/uc?export=view&id=1qU7XqqQHu0cWdBE1VavOhmUFT1xr7Gml',
        ],
        'message': """
¿Tienes problemas con el azúcar? ¡Diamed puede ayudarte!
🔥 OFERTA POR TIEMPO LIMITADO: 50% DE DESCUENTO
👉👉 https://sites.google.com/view/auto-diamed/home
⏳ ¡Solo quedan 60 unidades!
✅ Ingredientes 100% naturales
✅ Favorece la función insulínica
✅ Promueve un metabolismo equilibrado

🚀 -50% DE DESCUENTO 👉👉 https://sites.google.com/view/auto-diamed/home
#SaludNatural #ApoyoGlucosa #BienestarDiamed
#BienestarDiamed
"""
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
    # Step 1: Upload the photo as unpublished
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

    # Step 2: Create feed post with attached media and location
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

# Main loop
for campaign in campaigns:
    print(f"\n📢 Starting campaign: {campaign['name']}")
    token = get_page_access_token(campaign['page_id'], campaign['user_access_token'])

    if not token:
        print(f"❌ Skipping campaign {campaign['name']} due to token issue.")
        continue

    place_ids = campaign['place_ids'][:]
    images = campaign['default_images'][:]

    while place_ids:
        place = place_ids.pop(random.randint(0, len(place_ids) - 1))
        image = random.choice(images)  # Reuse images
        print(f"📸 Posting image: {image} | 📍 Place: {place}")
        post_with_location(campaign['page_id'], token, image, place, campaign['message'])
        time.sleep(2)

print("✅ All campaigns finished.")
