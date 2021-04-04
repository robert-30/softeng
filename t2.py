from POD import POD
from station import Station

def main():
    pod1 = POD("ASDDEA")
    pod2 = POD("ADEFFAQ")
    station1 = Station('Centraal Station', 'ad')
    station2 = Station('Station Heyendaal-1', 'hd')
    station1.callshuttle()
    station2.callshuttle()
    station1.shuttle_is_here()
    
if __name__ == "__main__":
    main()
