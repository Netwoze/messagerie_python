from datetime import datetime

def date_jour():
    return datetime.now().strftime("%d/%m/%Y")
  

def date_heure():
    return f"{str(datetime.now())[11:16]}"
    

def date_heure_secondes():
    return f"{str(datetime.now())}"
   

def timestamp_to_readable(time_stamp):
    """
    Timestamp to readable date
    """
    return datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y %H:%M:%S')

def time_stamp():
    return datetime.timestamp(datetime.now())
