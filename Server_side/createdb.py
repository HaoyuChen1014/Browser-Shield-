
import sqlite3

# Function to create the database and insert URLs
def create_database_and_insert_urls(db_file, txt_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phishing_sites (
            id INTEGER PRIMARY KEY,
            url TEXT
        )
    ''')

    # Read the URLs from the text file and insert them into the database
    with open(txt_file, 'r') as file:
        urls = file.read().splitlines()
        for url in urls:
            cursor.execute('INSERT INTO phishing_sites (url) VALUES (?)', (url,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data imported successfully.")

# Function to check if a URL is in the database (bad website)
def is_url_bad(db_file, url):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the URL exists in the database
    cursor.execute('SELECT COUNT(*) FROM phishing_sites WHERE url = ?', (url,))
    count = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    return count > 0

# Usage example:
if __name__ == "__main__":
    db_file = 'phishing_sites.db'
    txt_file = 'openphish.com_feed.txt'
    
    # Create the database and insert URLs from the text file
    create_database_and_insert_urls(db_file, txt_file)

    # Test if a URL is in the database
    test_url = 'http://robbinhodlogii.mystrikingly.com/'
    if is_url_bad(db_file, test_url):
        print(f"{test_url} is a bad website.")
    else:
        print(f"{test_url} is not in the database.")

    # You can use the is_url_bad function to check other URLs as well
