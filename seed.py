from database.db import get_connection, init_db
import random
from datetime import date, timedelta


categories = [
    ("Groceries","Food and household products"),
    ("Restaurants","Food and drinks"),
    ("Fuel","Car gas"),
    ("Hotels","Staying expenses"),
    ("Entertainment","Movies, amusement parks, etc."),
    ("Car maintenance","Oil changes, repairs, and other car-related expenses"),
    ("Shopping","Leisure shopping expenses"),
    ("Phone/Home Internet","Home internet and cellular bills"),
    ("Lease/Auto Loan","Monthly car lease or auto loan payments"),
    ("Rent/Mortgage","Monthly rent or mortgage expenses"),
    ("Subscriptions","Subscriptions of all kinds"),
    ("Uncategorized","Expenses that do not fall under any other category")
]


expense_settings = {
    "Groceries": {
        "names": ["Walmart","Costco","Publix","Aldi","Target","Whole Foods"],
        "min": 2500,
        "max": 24000
    },
    "Restaurants": {
        "names": ["Restaurant","Lunch","Dinner","Breakfast","Coffee shop","Fast food"],
        "min": 1200,
        "max": 18000
    },
    "Fuel": {
        "names": ["Shell","Chevron","Exxon","BP","Circle K","Mobil"],
        "min": 3500,
        "max": 12000
    },
    "Hotels": {
        "names": ["Hotel","Motel","Airbnb","Resort","Business hotel","Road hotel"],
        "min": 8500,
        "max": 65000
    },
    "Entertainment": {
        "names": ["Movies","Theme park","Concert","Bowling","Museum","Gaming"],
        "min": 1500,
        "max": 30000
    },
    "Car maintenance": {
        "names": ["Oil change","Tires","Car wash","Repair","Brake service","Maintenance"],
        "min": 2500,
        "max": 95000
    },
    "Shopping": {
        "names": ["Amazon","Target","Mall","Clothing","Electronics","Online shopping"],
        "min": 1500,
        "max": 45000
    },
    "Phone/Home Internet": {
        "names": ["Verizon","T-Mobile","AT&T","Home Internet","Phone bill","Internet bill"],
        "min": 4000,
        "max": 22000
    },
    "Lease/Auto Loan": {
        "names": ["Auto loan","Lease payment","Vehicle payment","Car financing"],
        "min": 35000,
        "max": 95000
    },
    "Rent/Mortgage": {
        "names": ["Rent payment","Mortgage payment","Housing payment"],
        "min": 90000,
        "max": 320000
    },
    "Subscriptions": {
        "names": ["Netflix","Spotify","YouTube","iCloud","Software","Streaming"],
        "min": 499,
        "max": 6000
    },
    "Uncategorized": {
        "names": ["Miscellaneous","Other expense","Cash expense","Unknown purchase","General expense"],
        "min": 500,
        "max": 25000
    }
}


# Old seed version: generated data for the last 36 months.
# def get_last_months(month_count):
#     today = date.today()
#     months = []
#     year = today.year
#     month = today.month
#     for _ in range(month_count):
#         months.append((year,month))
#         month -= 1
#         if month == 0:
#             month = 12
#             year -= 1
#     months.reverse()
#     return months


# New seed version: generates a random date inside the selected period.
def get_random_date(start_date: date, end_date: date) -> date:
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0,days_between))


def seed_database():
    init_db()
    random.seed(42)
    conn = get_connection()
    conn.executemany(
        "INSERT OR IGNORE INTO categories (name,description) VALUES (?,?)",
        categories
    )
    conn.commit()
    category_rows = conn.execute(
        "SELECT id,name FROM categories"
    ).fetchall()
    category_ids = {name: category_id for category_id,name in category_rows}

    # Old seed version.
    # months = get_last_months(36)

    # New seed version.
    start_date = date(2026,3,1)
    end_date = date.today()

    created = 0
    skipped = 0
    for category_name,_ in categories:
        category_id = category_ids[category_name]
        settings = expense_settings[category_name]

        # Old seed version: 10 expenses per category every month for 36 months.
        # for year,month in months:
        #     for expense_number in range(1,11):
        #         seed_marker = f"SEED:{category_name}:{year}-{month:02d}:{expense_number:02d}"
        #         existing = conn.execute(
        #             "SELECT id FROM expenses WHERE description = ?",
        #             (seed_marker,)
        #         ).fetchone()
        #         if existing:
        #             skipped += 1
        #             continue
        #         expense_name = random.choice(settings["names"])
        #         amount_cents = random.randint(settings["min"],settings["max"])
        #         day = random.randint(1,28)
        #         if year == today.year and month == today.month:
        #             day = random.randint(1,today.day)
        #         expense_date = f"{year}-{month:02d}-{day:02d}"
        #         conn.execute(
        #             """
        #             INSERT INTO expenses
        #             (category_id,name,currency,amount_cents,date,description)
        #             VALUES (?,?,?,?,?,?)
        #             """,
        #             (category_id,expense_name,"USD",amount_cents,expense_date,seed_marker)
        #         )
        #         created += 1

        # New seed version: 5 expenses per category = 60 total expenses.
        for expense_number in range(1,6):
            seed_marker = f"SEED:{category_name}:{expense_number:02d}"
            existing = conn.execute(
                "SELECT id FROM expenses WHERE description = ?",
                (seed_marker,)
            ).fetchone()
            if existing:
                skipped += 1
                continue
            expense_name = random.choice(settings["names"])
            amount_cents = random.randint(settings["min"],settings["max"])
            expense_date = get_random_date(start_date,end_date)
            conn.execute(
                """
                INSERT INTO expenses
                (category_id,name,currency,amount_cents,date,description)
                VALUES (?,?,?,?,?,?)
                """,
                (
                    category_id,
                    expense_name,
                    "USD",
                    amount_cents,
                    expense_date.strftime("%Y-%m-%d"),
                    seed_marker
                )
            )
            created += 1
    conn.commit()
    conn.close()
    print("Seed completed successfully")
    print(f"Categories: {len(categories)}")
    print(f"Expenses created: {created}")
    print(f"Expenses skipped: {skipped}")

    # Old seed version.
    # print(f"Expected seed expenses: {len(categories) * 10 * 36}")

    # New seed version.
    print(f"Expected seed expenses: {len(categories) * 5}")


if __name__ == "__main__":
    seed_database()