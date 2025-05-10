import sqlite3

def insert_initial_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Categories
    cursor.execute("INSERT INTO page_category (name) VALUES (?)", ("Crypto",))
    cursor.execute("INSERT INTO page_category (name) VALUES (?)", ("Credit Card",))
    cursor.execute("INSERT INTO page_category (name) VALUES (?)", ("P2P",))

    # Get category IDs
    cursor.execute("SELECT id FROM page_category WHERE name = ?", ("Crypto",))
    crypto_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_category WHERE name = ?", ("Credit Card",))
    credit_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_category WHERE name = ?", ("P2P",))
    p2p_id = cursor.fetchone()[0]

    # Groups
    groups = [
        ("Bitfinex", crypto_id),
        ("AwesomePay", crypto_id),
        ("Hosted Page", credit_id),
        ("Direct Payment", credit_id),
        ("P2P Group", p2p_id),
    ]
    cursor.executemany("INSERT INTO page_group (name, category_id) VALUES (?, ?)", groups)

    # Get group IDs
    cursor.execute("SELECT id FROM page_group WHERE name = 'Bitfinex'")
    bitfinex_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_group WHERE name = 'AwesomePay'")
    awesomepay_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_group WHERE name = 'Hosted Page'")
    hosted_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_group WHERE name = 'Direct Payment'")
    direct_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM page_group WHERE name = 'P2P Group'")
    p2p_id = cursor.fetchone()[0]

    # Tabs
    tabs = [
        (bitfinex_id, "Pay In", "bitfinex-payin"),
        (bitfinex_id, "Pay Out", "bitfinex-payout"),
        (awesomepay_id, "Pay In", "awesomepay-payin"),
        (awesomepay_id, "Pay Out", "awesomepay-payout"),
        (hosted_id, "Hosted Page", "hosted"),
        (direct_id, "Direct", "direct"),
        (p2p_id, "Pay In", "p2p-payin"),
        (p2p_id, "Pay Out", "p2p-payout"),
        (p2p_id, "Check Balance", "p2p-check"),
    ]
    cursor.executemany("INSERT INTO page_tab (group_id, name, slug) VALUES (?, ?, ?)", tabs)

    conn.commit()
    conn.close()
    print("✅ Initial data inserted.")

if __name__ == "__main__":
    insert_initial_data()
