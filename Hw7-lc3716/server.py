
from markupsafe import Markup
from flask import Flask, request, jsonify, render_template, redirect, url_for

import re


app = Flask(__name__)

current_id = 10

restaurants = {
    1:{
    "id": 1,
    "Restaurant": "Sweetgreen", 
    "Description": "Health food restaurant",
    "Restaurant_image": "https://media-cdn.tripadvisor.com/media/photo-s/0a/60/81/43/upper-westside-location.jpg",
    "Food_image1": "http://thecorestories.com/wp-content/uploads/2016/02/sweetgreen-x-Columbia-U-47-of-92-1.jpg",
    "Food_image2": "https://tb-static.uber.com/prod/image-proc/processed_images/96d204a8cff606290825f677cc52aedd/c9252e6c6cd289c588c3381bc77b1dfc.jpeg",
    "Summary": "Sweetgreen is celebrated for its fresh, health-focused menu featuring a variety of salads, warm bowls, and high-protein plates that cater to diverse dietary preferences including vegan and gluten-free options. Targeting health-conscious individuals, Sweetgreen emphasizes sustainable sourcing and transparency, aspiring to connect communities to real food. Their innovative approach extends to customer service with digital ordering and loyalty programs like Sweetpass, enhancing convenience without compromising on quality. Sweetgreen's commitment to health, community, and sustainability positions it as a leader in the fast-casual dining sector, appealing to those who value both their well-being and environmental impact.",

    "Address": "2937 Broadway, New York, NY 10025",
    "price_range": "$$",
    "Rating":3.9,
    "Menu": "https://www.sweetgreen.com/",
    "Hours": "Mon-Sun: 10:30AM - 10:00PM",
    "Distance_from_campus": "0.2 mile, 4 mins walking",
    "Contact": "+1 9176756616",
    "Offerings": ["comfort food", "Healthy options","Organic dishes", "Quick bite", "Salad bar", "Vegan options", "Vegetarian options"],
    },
    2:{
    "id": 2,
    "Restaurant": "Junzi Kitchen", 
    "Description": "Chinese restaurant",
    "Restaurant_image": "https://media-cdn.tripadvisor.com/media/photo-s/0f/b9/e9/d5/inside-junzi-kitchen.jpg",
    "Food_image1": "https://media-cdn.tripadvisor.com/media/photo-s/10/ff/e0/c8/bings-noodles.jpg",
    "Food_image2": "https://images.squarespace-cdn.com/content/v1/538acfa1e4b01f1c805e1329/267c020c-7a16-4d31-a1e6-614321c0682d/13_Noodles%2BRice%2BSalad%2Bfinal.jpeg",
    "Summary": "This fast-casual eatery specializes in Chinese chun bing, offering a delightful selection of savory pancakes that perfectly encapsulate traditional flavors. Alongside these, the restaurant boasts a variety of noodles, providing a comprehensive taste of authentic Chinese cuisine. It caters to the late-night crowd, especially on weekends, by featuring an exclusive menu designed to satisfy those after-hour cravings. Whether you're looking for a quick lunch or a late-night feast, this spot promises an exceptional culinary experience with its focus on chun bing and noodles.",

    "Address": "2896 Broadway, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.3,
    "Menu": "https://order.junzi.menu/kitchen-columbia/menu",
    "Hours": ["Mon-Sun: 11:00AM - 10:00PM"],
    "Distance_from_campus": "0.2 mile, 4 mins walking",
    "Contact": "+1 9172612497",
    "Offerings": ["Alcohol","Beer", "Cocktails", "Healthy options", "Late-night food","Quick bite","Vegan options", "Vegetarian options","Wine"],
    },
    3:{
    "id": 3,
    "Restaurant": "Sapps", 
    "Description": "Japanese restaurant",
    "Restaurant_image": "https://images.squarespace-cdn.com/content/v1/6102e7626a5b787b16fd3f65/1698954469632-BOX6PTRR0I11DXR4UH16/230909-Sapps+UWS+interior-138-Edit.jpg",
    "Food_image1": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/store/header/4cc373f2-b5ff-42e9-9379-4713c99a434a.jpg",
    "Food_image2": "https://images.squarespace-cdn.com/content/v1/6102e7626a5b787b16fd3f65/1698954116414-BCKHOTWHD8B0Y0HHJFZ6/230909-02-069.jpg",
    "Summary": "SAPPS roots trace back to the East Village, where its owner, Shih Lee, was inspired by a no-frills, authentic Japanese restaurant that specialized in izakaya-style dishes, setting the stage for what would become a beloved culinary tradition. This inspiration led to the establishment of SAPPS in LIC, aiming to blend the essence of traditional Japanese izakaya with a modern New York City vibe. Under the partnership of Shih Lee, bartender Eric Lehrer, and waiter Selix Lai, the team is dedicated to recreating that authentic dining experience, focusing on a menu that promises to bring a unique and vibrant taste of Japan to the neighborhood. Their goal is to offer Manhattan residents a dynamic dining spot that goes beyond the conventional restaurant experience, serving up a carefully curated selection of dishes that pay homage to the rich flavors and casual dining style of a Tokyo izakaya.",

    "Address": "2888 Broadway, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.4,
    "Menu": "https://www.sappsuws.com/menu",
    "Hours": "Mon-Thu: 11:30AM - 10:00PM",
    "Distance_from_campus": "0.2 mile, 4 mins walking",
    "Contact": "+1 9172612497",
    "Offerings": ["Alcohol", "Beer","Cocktails", "Healthy options", "Late-night food","Quick bite","Vegan options", "Vegetarian options","Wine"],
    },
    4:{
    "id": 4,
    "Restaurant": "DIG", 
    "Description": "American restaurant",
    "Restaurant_image": "https://images.squarespace-cdn.com/content/v1/553a8ddae4b0bd1c1a10972e/1523324868292-KZVNLCHRMT48K56SI790/ke17ZwdGBToddI8pDm48kNBhxsR5AixTPaSt36FQjZRZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIHEpb-MmdDNvFVgjmeoENIlexef176In2EgYPtI8R2-8KMshLAGzx4R3EDFOm1kBS/image-asset.jpeg",
    "Food_image1": "https://images.squarespace-cdn.com/content/v1/6377acee19258c4978a8a37b/a13c4e6f-e75a-4739-bef8-98e5374f6c39/dig+177.jpg",
    "Food_image2": "https://images.squarespace-cdn.com/content/v1/6377acee19258c4978a8a37b/e0e44a53-27bc-4e6f-b834-a38bff8d737c/TL_dg8kpz.jpg",
    "Summary": "This New York City-based cafeteria-style chain is renowned for its commitment to serving seasonal, thoughtfully sourced dishes, ensuring every bite is both delicious and responsible. Specializing in a wide array of sandwiches and salads, the menu reflects a dedication to freshness and quality, catering to the diverse tastes of its urban clientele. Each item is crafted with ingredients sourced from local farms and suppliers, highlighting the chain's support for sustainable agriculture and local economies. Whether you're in search of a quick lunch or a nutritious meal on the go, this establishment offers a conscientious dining experience that doesn't compromise on flavor or quality",

    "Address": "2884 Broadway, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.2,
    "Menu": "https://www.diginn.com/menu/",
    "Hours": "Mon-Sun: 11:00AM - 10:00PM",
    "Distance_from_campus": "0.2 mile, 5 mins walking",
    "Contact": "+1 2127764047",
    "Offerings": ["Comfort food", "Healthy options","Quick bite","Vegan options", "Vegetarian options"],
    },
    5:{
    "id": 5,
    "Restaurant": "Tom's", 
    "Description": "American restaurant",
    "Restaurant_image": "https://media-cdn.tripadvisor.com/media/photo-s/09/24/be/e7/tom-s-restaurant.jpg",
    "Food_image1": "https://fastly.4sqi.net/img/general/600x600/352133_kvaf5K_8LsIX-Ah2dh-_s-IAXTtqY5Z7rqLmLAWPsw8.jpg",
    "Food_image2": "https://tb-static.uber.com/prod/image-proc/processed_images/1b86be1fe639c2cc6b65bedc40d40260/3ac2b39ad528f8c8c5dc77c59abb683d.jpeg",
    "Summary": "This quaint local coffee shop gained fame for its recurring cameo appearances on the classic TV sitcom Seinfeld, embedding itself in the hearts of fans as a beloved pop culture landmark. Known for its unassuming charm and welcoming atmosphere, it offers a simple yet satisfying menu that has become a staple for both locals and visiting enthusiasts alike. Its walls, often buzzing with the laughter of customers reminiscing about their favorite Seinfeld moments, tell stories of its unique place in television history. Beyond its fame, the coffee shop remains a cozy spot for anyone looking to enjoy a basic cup of coffee and the warmth of shared memories in a setting that feels like a slice of TV history.",

    "Address": "2880 Broadway, New York, NY 10025",
    "price_range": "$",
    "Rating":4.2,
    "Menu": "https://tomsrestaurant-2451460.dine.online/locations/900332?fulfillment=pickup&utm_source=menu",
    "Hours": "Mon-Sun: 7:00AM - 11:00PM",
    "Distance_from_campus": "0.2 mile, 5 mins walking",
    "Contact": "+1 2128646137",
    "Offerings": ["Alcohol", "Beer","Coffee", "Comfort food", "Late-night food", "Quick bite", "Small plates"],
    },
    6:{
    "id": 6,
    "Restaurant": "Koronet Pizza", 
    "Description": "Pizza restaurant",
    "Restaurant_image": "https://assets.dnainfo.com/generated/photo/2012/12/cleon-minakas-of-koronet-pizza-13545387409996.JPG/extralarge.jpg",
    "Food_image1": "https://slicelife.imgix.net/1236/photos/original/KoronetPizza_MargheritaPizza.jpg",
    "Food_image2": "https://fastly.4sqi.net/img/general/600x600/19696169_xWQzITMCmetESPt9gipT7ugncde0Xwz46How6rSMeCI.jpg",
    "Summary": "Koronet Pizza prides itself on using only fresh, high-quality ingredients to craft an array of mouthwatering pizzas, including classic cheese, Margherita, pepperoni, Buffalo chicken, Sicilian, and Grandma pizza, ensuring there's a flavor for every palate. Whether you're in the mood for a whole pie or just a slice, our menu accommodates any appetite, offering the quintessential New York pizza experience. Beyond our renowned pizzas, we also serve a variety of tasty appetizers, calzones, rolls, and patties, perfect for complementing your meal. Each bite at Koronet Pizza captures the essence of New York's vibrant culinary scene, promising an unforgettable dining experience that will leave you eager to return.",

    "Address": "2848 Broadway, New York, NY 10025",
    "price_range": "$",
    "Rating":4.5,
    "Menu": "https://www.koronetpizzany.com/#menu",
    "Hours": "Mon-Sun: 12:30AM - 3:00AM",
    "Distance_from_campus": "0.3 mile, 7 mins walking",
    "Contact": "+1 2122221566",
    "Offerings": ["Comfort food", "Late-night food","Quick bite","Vegetarian options"],
    },
    7:{
    "id": 7,
    "Restaurant": "Atlas Kitchen", 
    "Description": "Chinese restaurant",
    "Restaurant_image": "https://cdn.vox-cdn.com/thumbor/6keS08HUKMW50QcMWy3xG2FU8go=/0x0:5760x3840/1200x0/filters:focal(0x0:5760x3840):no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/14739070/Atlas_Kitchen_1.jpg",
    "Food_image1": "https://doordash-static.s3.amazonaws.com/media/store/header/315254.jpg",
    "Food_image2": "https://images.squarespace-cdn.com/content/v1/5be61e0d45776e7a5933efe9/1575520897954-ECKWQCSL40B7N5G5SASH/DSC01293.jpg",
    "Summary": "A new contemporary Chinese restaurant has opened on the Upper West Side, drawing inspiration from The Classics of Mountains and Seas, an ancient Chinese text that dates back to the 4th century B.C. This literary masterpiece, known for its rich compilation of mythical figures and diverse geographical descriptions, influences the restaurant's culinary creations. The menu is a homage to the text, featuring dishes that embody the essence of the mountains, seas, and wilderness areas described across the cardinal directions. Through innovative cooking techniques and authentic flavors, the restaurant offers diners a unique journey through China's ancient mythology and geography.",

    "Address": "258 W 109th St, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.0,
    "Menu": "https://www.atlaskitchennyc.com/menu",
    "Hours": "Mon-Sun: 11:30AM - 9:30PM",
    "Distance_from_campus": "0.5 mile, 11 mins walking",
    "Contact": "+1 6469280522",
    "Offerings": ["Alcohol","Beer","Comfort food","Happy hour drinks","Small plates","Wine"],
    },
    8:{
    "id": 8,
    "Restaurant": "Himalayan Curry House (Uptown Branch)", 
    "Description": "Indian restaurant",
    "Restaurant_image": "https://ik.imagekit.io/awwybhhmo/satellite_images/indian/beyondmenu/hero/10.jpg?tr=w-3840,q-50",
    "Food_image1": "https://d1ralsognjng37.cloudfront.net/b0a75ab5-660c-42f7-9cf2-c659c3ad7bfe.jpeg",
    "Food_image2": "https://pyxis.nymag.com/v1/imgs/d77/8c4/9072f3b89e2e97af7412bcb7b79e3f54be-bony-himalayan-woodside-1.1x.rsocial.w1200.jpg",
    "Summary": "Nestled in an easygoing setting, this dining spot specializes in traditional Indian cuisine, offering a tantalizing array of curries, biryani, and other classic dishes. Each recipe is meticulously prepared to bring out the rich, aromatic flavors that Indian fare is celebrated for, using a blend of authentic spices and ingredients. Whether you're craving the comforting warmth of a slow-cooked curry or the fragrant layers of a well-spiced biryani, there's something on the menu to satisfy every palate. The restaurant's relaxed atmosphere makes it the perfect place to unwind and enjoy the culinary delights of India, whether you're dining alone or with company.",

    "Address": "254 W 108th St, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.3,
    "Menu": "https://www.himalayancurrynyc.com/iaooy89p/himalayan-curry-houseuptown-branch-new-york-10025/order-online#menu",
    "Hours": "Mon-Sun: 10:30AM - 9:45PM",
    "Distance_from_campus": "0.5 mile, 12 mins walking",
    "Contact": "+1 2127497800",
    "Offerings": ["Comfort food", "Halal food","Healthy options","Quick bite","Small plates","Vegan options","Vegetarian options"],
    },
    9:{
    "id": 9,
    "Restaurant": "Kyuramen - Upper West Side", 
    "Description": "Ramen restaurant",
    "Restaurant_image": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/16e2211e-fceb-4833-b312-0cda04ef387f-9c4dd627-f62c-44ba-85e5-f298c771eeab-retina-large.jpg",
    "Food_image1": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_iZ_FJ1SHEEGzRqhOU-PzeqhVPgwKCgR4zA&usqp=CAU",
    "Food_image2": "https://media.bizj.us/view/img/12276296/61a0c1560ea9eca3fd7d6ac4c9a4651c*1200xx2700-1519-0-141.jpg",
    "Summary": "This ramen restaurant prides itself on delivering the authentic taste of traditional Japanese ramen, meticulously prepared to reflect the rich culinary heritage of Japan. Each bowl is a carefully crafted symphony of flavors, offering diners a genuine experience of classic ramen. In addition to the traditional offerings, the restaurant boasts a variety of drink options to complement your meal, ranging from Japanese sake and beer to non-alcoholic beverages. The diverse menu ensures that every guest can find the perfect pairing to enhance their ramen experience, making it a must-visit destination for enthusiasts of Japanese cuisine.",

    "Address": "2787 Broadway, New York, NY 10025",
    "price_range": "$$",
    "Rating":4.6,
    "Menu": "https://kyuramenny.com/",
    "Hours": "Mon-Sun: 11:00AM - 10:30PM",
    "Distance_from_campus": "0.5 mile, 12 mins walking",
    "Contact": "+1 9172658722",
    "Offerings": ["Alcohol","Beer","Comfort food","Happy hour drinks","Quick bite","Small plates","Vegetarian options"],
    },
    10:{
    "id": 10,
    "Restaurant": "Massawa", 
    "Description": "Ethiopian restaurant",
    "Restaurant_image": "https://bwog.com/wp-content/uploads/2021/10/IMG_2415-scaled.jpg",
    "Food_image1": "https://media-cdn.tripadvisor.com/media/photo-s/10/92/33/ac/a-family-meal-fit-for.jpg",
    "Food_image2":"https://www.africanrestaurantweek.com/wp-content/uploads/2021/06/Massawa.jpg",
    "Summary": "This East African eatery offers an authentic dining experience, specializing in traditional Ethiopian and Eritrean cuisine that is traditionally scooped by hand using injera, a spongy sourdough flatbread. The menu features a variety of stews, meats, and vegetarian dishes, all infused with the unique spices and flavors characteristic of the region. Diners are invited to share meals communally, embracing the cultural practice of eating from the same platter, which fosters a sense of unity and friendship. This culinary haven is a perfect spot for those looking to explore the rich tapestry of East African food traditions, served in a warm and welcoming atmosphere.",

    "Address": "1239 Amsterdam Ave, New York, NY 10027",
    "price_range": "$$",
    "Rating":4.5,
    "Menu": "https://www.massawanyc.com/menu",
    "Hours": "Mon-Sun: 11:30AM - 10:00PM",
    "Distance_from_campus": "0.4 mile, 8 mins walking",
    "Contact": "+1 2126630505",
    "Offerings": ["Alcohol","Beer","Cocktails","Coffee","Comfort food","Happy hour drinks","Hard liquor","Healthy options","Late-night food","Small plates","Vegan options","Vegetarian options","Wine"],
    },
}

# ROUTES
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/restaurants')
def get_restaurants():
    return jsonify(restaurants=list(restaurants.values()))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()  # Convert query to lowercase
    filtered_restaurants = []
    for restaurant in restaurants.values():
        # Copy restaurant to avoid mutating the original
        restaurant_copy = restaurant.copy()
        
        # Highlight the text in the Restaurant name, Description, and Offerings
        restaurant_copy['Restaurant'] = highlight_text(restaurant['Restaurant'], query)
        restaurant_copy['Description'] = highlight_text(restaurant['Description'], query)
        restaurant_copy['Offerings'] = [highlight_text(offering, query) for offering in restaurant['Offerings']]
        
        # Check if restaurant matches query, now including highlighted Restaurant name in search criteria
        if (highlight_text(restaurant['Restaurant'], query) != restaurant['Restaurant']  # Check if the Restaurant name contains the query
                or query in restaurant['Description'].lower()
                or any(query in offering.lower() for offering in restaurant['Offerings'])):
            filtered_restaurants.append(restaurant_copy)
    
    count = len(filtered_restaurants)
    return render_template('search_results.html', items=filtered_restaurants, search_query=request.args.get('query', ''), count=count)


def calculate_stars(rating):
    full_stars = int(rating)  # Get the integer part for full stars
    half_star = 0
    empty_stars = 0

    # Check if there's a need for a half star
    if rating - full_stars >= 0.4:
        half_star = 1
    # Calculate empty stars
    empty_stars = (5 - full_stars) - half_star

    return full_stars, half_star, empty_stars


def highlight_text(text, search_query):
    """Highlight search query in text, case-insensitive, without separating from other words."""
    if not search_query:  # Avoid processing if the search query is empty
        return text
    # Escape the search query to ensure it's treated as a literal string in the regex
    escaped_query = re.escape(search_query)
    # Use re.sub() to wrap the search query in <mark> tags for highlighting
    # The flags=re.IGNORECASE makes the search case-insensitive
    highlighted_text = re.sub(f'({escaped_query})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return Markup(highlighted_text)


@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    global current_id, restaurants  # Reference the global variables so you can modify them
    if request.method == 'GET':
        return render_template('add_restaurant.html')
    elif request.method == 'POST':
        # Handle JSON data
        data = request.get_json()
        restaurant = {
            "id": current_id + 1,
            "Restaurant": data.get('Restaurant', ''),
            "Description": data.get('Description', ''),
            "Restaurant_image": data.get('Restaurant_image', ''),
            "Food_image1": data.get('Food_image1', ''),
            "Food_image2": data.get('Food_image2', ''),
            "Summary": data.get('Summary', ''),
            "Address": data.get('Address', ''),
            "price_range": data.get('price_range', ''),
            "Rating": float(data.get('Rating', 0)),  # Assuming rating is a decimal
            "Menu": data.get('Menu', ''),
            "Hours": data.get('Hours', []),
            "Distance_from_campus": data.get('Distance_from_campus', ''),
            "Contact": data.get('Contact', ''),
            "Offerings": data.get('Offerings', '').split(', '),  # Assuming offerings are comma-separated
        }
        current_id += 1
        restaurants[current_id] = restaurant
        return jsonify({"success": True, "message": "Restaurant added", "id": current_id})


@app.route('/view/<int:id>')
def view_restaurant(id):
    # Assume 'restaurants' is a global dictionary storing restaurant data.
    restaurant = restaurants.get(id)
    if not restaurant:
        return "Restaurant not found", 404

    # Calculate star ratings
    full_stars, half_star, empty_stars = calculate_stars(restaurant['Rating'])

    # Render the template with the restaurant data and the star ratings
    return render_template('restaurant_detail.html', restaurant=restaurant, 
                           full_stars=full_stars, half_star=half_star, 
                           empty_stars=empty_stars)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_restaurant(id):
    restaurant = restaurants.get(id)
    if not restaurant:
        return "Restaurant not found", 404

    if request.method == 'POST':
        if 'save' in request.form:  # Check if the save button was clicked
            # Process the form submission
            # Update restaurant details based on form input
            restaurant['Restaurant'] = request.form['Restaurant']
            restaurant['Description'] = request.form['Description']
            restaurant['Restaurant_image'] = request.form['Restaurant_image']
            restaurant['Food_image1'] = request.form['Food_image1']
            restaurant['Food_image2'] = request.form['Food_image2']
            restaurant['Summary'] = request.form['Summary']
            restaurant['Address'] = request.form['Address']
            restaurant['price_range'] = request.form['price_range']
            restaurant['Rating'] = float(request.form['Rating'])
            restaurant['Menu'] = request.form['Menu']
            restaurant['Hours'] = request.form['Hours']
            restaurant['Distance_from_campus'] = request.form['Distance_from_campus']
            restaurant['Contact'] = request.form['Contact']
            restaurant['Offerings'] = [offering.strip() for offering in request.form['Offerings'].split(',') if offering.strip()]
            # Repeat for other fields...
            # Redirect to the view page
            return redirect(url_for('view_restaurant', id=id))
        # Note: With the JavaScript approach for discarding, this part of the code might not be reached for discarding changes
        if 'discard' in request.form:
            return redirect(url_for('view_restaurant', id=id))

    # GET request or form errors: render the edit form with pre-populated data
    return render_template('edit_restaurant.html', restaurant=restaurant)


if __name__ == '__main__':
    app.run(debug=True)