from bank import Bank

def test_create_account():
    bank = Bank()
    assert bank.create_account(1, "A") == True
    assert bank.create_account(2, "A") == False
    assert bank.create_account(3, "B") == True

def test_deposit():
    bank = Bank()
    bank.create_account(1, "A")
    assert bank.deposit(2, "A", 100) == 100
    assert bank.deposit(3, "A", 50) == 150
    assert bank.deposit(4, "B", 100) == None

def test_transfer():
    bank = Bank()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.deposit(3, "A", 100)
    assert bank.transfer(4, "A", "B", 50) == 50
    assert bank.transfer(5, "A", "B", 60) == None
    assert bank.transfer(6, "B", "A", 30) == 80

def test_top_spenders():
    bank = Bank()
    bank.create_account(1, "A")
    bank.create_account(2, "B")
    bank.create_account(3, "C")
    bank.deposit(4, "A", 100)
    bank.deposit(5, "B", 200)
    bank.transfer(6, "A", "B", 50)
    bank.transfer(7, "B", "C", 100)
    assert bank.top_spenders(8, 2) == ["B(100)", "A(50)"]
    assert bank.top_spenders(9, 1) == ["B(100)"]

def test_level_3():
    # Test 1: Schedule a payment
    bank = Bank()
    assert bank.create_account(1, "a") is True
    assert bank.deposit(2, "a", 500) == 500
    assert bank.schedule_payment(3, "a", 100, 5) == "payment1"
    assert bank.account["a"][0] == 500  # Not deducted yet

    # Test 2: Payment executes when due
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 500)
    bank.schedule_payment(3, "a", 100, 5)

    assert bank.deposit(7, "a", 0) == 500
    assert bank.deposit(8, "a", 0) == 400

    # Test 3: Insufficient funds; payment is skipped
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 50)
    bank.schedule_payment(3, "a", 100, 5)

    assert bank.deposit(8, "a", 0) == 50
    assert bank.deposit(9, "a", 100) == 150

    # Test 4: Cancel a payment
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 500)
    assert bank.schedule_payment(3, "a", 100, 10) == "payment1"

    assert bank.cancel_payment(4, "a", "payment1") is True
    assert bank.deposit(13, "a", 0) == 500

    # Test 5: Cannot cancel another account's payment
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 500)
    bank.schedule_payment(4, "a", 100, 10)

    assert bank.cancel_payment(5, "b", "payment1") is False

    # Test 6: Payment IDs and failed scheduling
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")

    assert bank.schedule_payment(3, "missing", 100, 5) is None
    assert bank.schedule_payment(4, "a", 50, 5) == "payment1"
    assert bank.schedule_payment(5, "b", 60, 5) == "payment2"

    # Test 7: Payments due at the same timestamp
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 200)

    bank.schedule_payment(3, "a", 100, 5)  # payment1 due at 8
    bank.schedule_payment(4, "a", 150, 4)  # payment2 due at 8

    assert bank.deposit(8, "a", 0) == 100
    assert bank.outgoing["a"] == 100



    print("All Level 3 tests passed!")


test_level_3()

def test_level_4():
    # Test 1: Merge balances and outgoing totals
    bank = Bank()
    assert bank.create_account(1, "a") is True
    assert bank.create_account(2, "b") is True
    assert bank.deposit(3, "a", 500) == 500
    assert bank.deposit(4, "b", 300) == 300

    assert bank.merge_accounts(7, "a", "b") is True
    assert bank.account["a"][0] == 800
    assert "b" not in bank.account
test_level_4()