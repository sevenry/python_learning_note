def save_transaction(price,credit_card,description):
    file=open("transaction.txt","a")
    file.write("%07d%16s%s\n" % (price*100,credit_card,description))
    file.close()
