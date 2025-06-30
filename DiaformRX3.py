import random
import requests
import time

# Configurations for each campaign
campaigns = [
    {
        'name': 'DiaformRX - message 3',
        'page_id': '708174525712395',
        'place_ids': [
            '103082828241702',  # Graz
            '111165112241092',  # Vienna
            '106242929412108',  # Linz
            '107713179252134',  # Austria
            '102189213155511',  # Salzburg
        ],
        'user_access_token': 'EAASbYg8NcwcBO4KzTxJuHS3By9CreKAcBQytiInEIIqFtZAQLZAaPwZCbCNrye0GsLkrATK2D047AtstZBPNWLPrhTlz0adMWVQocGH9RyIfiuCQ2MyRt1CqR3hHE1AjVXJiOqZA8htZC8ftmzqq1lMqHF76Cnxbj7L1fDgHnKZC3ljOzTMZAYuFOA8CElkTlbZBR',
        'default_images': [
            'https://drive.google.com/uc?export=view&id=1S1Zsm-9JmDezc_gGBrHYbuqnlnHO65Su',
            'https://drive.google.com/uc?export=view&id=1SC8-Y-wXNRr9CKSRKdTaGZgZusdFb0LM',
            'https://drive.google.com/uc?export=view&id=1pIZ6bH5WTX3g_JroAaJ6nSbc4IlJiBa9'
        ],
        'message': """
Unterstützen Sie Ihren Blutzuckerspiegel mit Wissenschaft & Natur 🍃
🎁 Sonderangebot: Nur heute 49 €
👉 👉 https://sites.google.com/view/auto-diaform/home
Fühlen Sie sich jeden Tag rundum wohl mit DiaformRX – dem einzigen zertifizierten Nahrungsergänzungsmittel zur Unterstützung des Blutzuckergleichgewichts.

💚 Warum DiaformRX?
🌿 Hilft, einen gesunden Blutzuckerspiegel aufrechtzuerhalten
⚡️ Fördert Stoffwechsel und Energie
😌 Verbessert Stimmung, Schlaf und Immunsystem
📃 Zertifiziert sicher – keine Nebenwirkungen

💳 Zahlung bei Lieferung | Kein Risiko
📍 Klicken Sie unten, um noch heute Ihre kostenlose Flasche zu erhalten!
👉 👉 https://sites.google.com/view/auto-diaform/home

#DiaformRX #NatürlicheUnterstützung #Blutzuckergesundheit #WissenschaftTrifftNatur #ZertifiziertesWohlbefinden #EU-Angebot
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
