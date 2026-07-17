def find_large_transaction(transactions, threshold):
    for t in transactions:
        if t >= threshold:
            return t
    return None
