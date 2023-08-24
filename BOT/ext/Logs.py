import datetime
def log(data):
    print(datetime.datetime.now().time().strftime('[%H:%M:%S]')+" -> "+data+"\n\n")