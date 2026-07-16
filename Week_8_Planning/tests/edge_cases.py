def test_invalid_order():
    print("Test 1")
    print("Order ID not found")
    print("Expected : Referential Integrity Error")

def test_discount():
    discount = 120
    if discount > 100:
        print("Invalid Discount")

def test_zero_quantity():
    quantity = 0
    revenue = quantity * 500
    print("Revenue :", revenue)

from datetime import datetime

def test_future_date():
    order = datetime(2030, 1, 1)
    if order > datetime.now():
        print("Future Date Found")

test_invalid_order()
test_discount()
test_zero_quantity()
test_future_date()