def transaction_status(amount, balance):
    if amount > balance:
        return 'declined'
    return 'approved'
