import random
import requests
import time

# ✅ Campaign configuration for Difort
campaigns = [
    {
        'name': 'Diabetin',
        'page_id': '727247863799787',
        'user_access_token': 'EAAR9UVr2DNABO4d7VlXHh0xx6WYHyRHWF576187bDCUh1TkjuQ2WHei62e29KkD6nXJiL3k2GUNGFmAtZBLaZAReQ4SoSEX0HR99iFmrAkjZBL89PjttZC8s380X3pK94PDkS0ui3HFEijZC30Rb4ZA95Bfs6Uz8rZB6YGl7CGAhNsyVc2NiRf3BlmydRgC',
        'place_ids': [
'399227480119669', #Queson City
'106322966073780', #Manila 
'108343052523582', #Davao City
'101904068654639', #Caloocan
'102182963156749' #Taguig
        ],
        'images': [
'https://drive.google.com/uc?export=view&id=16Kv3j1TpEOktrQCvS0f06v7bDkxtY-ET', 'https://drive.google.com/uc?export=view&id=19xyHc8z9w50OT_PCetHbPemXpo2K9pqH', 'https://drive.google.com/uc?export=view&id=1TtqadqueO-VPAi60c84PW18XGDY4o4dR', 'https://drive.google.com/uc?export=view&id=1Uv_L_S3ZbSaJmYLdbGelTqGL4jWWvhpZ', 'https://drive.google.com/uc?export=view&id=1X5xz5yv0BnkjY2mfLjHPBORoXQU3u3Vn', 'https://drive.google.com/uc?export=view&id=1bO2fFZQWmJSILhqbYeXKoRyLJ1_2a6Yo'
        ],
        'message': '''
Natural na Pamahalaan ang Blood Sugar – Sa Diabetin 🌿
Pagod na sa pakikipaglaban sa asukal sa dugo, presyon, at mga isyu sa timbang?

🎉 Ngayon Lang: ₱1980 (Dating ₱3960) – 50% OFF
👉 👉 https://sites.google.com/view/auto-diabetin/home

💚 Ano ang sinusuportahan ng Diabetin:
✔️ Normal na asukal sa dugo at presyon
✔️ Mas malusog na balanse ng kolesterol
✔️ Metabolismo at pagsunog ng taba
✔️ Balanse ng hormonal at pagiging sensitibo sa insulin

🌿 100% natural na sangkap tulad ng Fig Leaf, White Mulberry at Berberine
📦 Mabilis na delivery sa buong Pilipinas
💰 Magbayad ng cash on delivery

🕐 Limitadong Oras na Promo – Order na! 
👉 👉 https://sites.google.com/view/auto-diabetin/home

#Diabetin #SuportaSaAsukalSaDugo #KalusugangLikas #Pag-aalagaSaKolesterol #SuportaSaMetabolismo #KalusuganNgPilipinas
        '''
    },

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
