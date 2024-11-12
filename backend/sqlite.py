import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# URLs for the images
image_urls = [
    'https://www.decornation.in/wp-content/uploads/2020/07/modern-dining-table-chairs.jpg',
    'https://www.decornation.in/wp-content/uploads/2020/06/cafe-living-room-dining-chair.jpg',
    'https://cdn.decornation.in/wp-content/uploads/2020/06/decornation-furniture-dining-chair-650x650.jpg',
]

# Fetch all item IDs from the e_cart_item table
cursor.execute("SELECT id FROM e_cart_item")
item_ids = cursor.fetchall()  # This returns a list of tuples

# Insert image data for each item
for item_id_tuple in item_ids:
    item_id = item_id_tuple[0]  # Extract the ID from the tuple
    for image_url in image_urls:
        cursor.execute(
            "INSERT INTO e_cart_image (item_id, image_path) VALUES (?, ?)",
            (item_id, image_url)
        )

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Images have been successfully inserted into the SQLite database.")
