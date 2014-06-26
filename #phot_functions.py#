import functions,os,sys,ephem,string
from numpy import *
import matplotlib.pyplot as plt

### Create airmass plot for a candidate

def compute_alt_plot(ra,dec,obsvat,date):
    ### get alt every hr
    hr = arange(0,1,0.01)
    dates = []
    alt = []
    for hr_i in hr:
        date_time = date + str(hr_i)[1:] 
        alt_i,az_i = functions.compute_alt_az(ra,dec,obsvat,date_time)

        dates.append(ephem.date(date_time).datetime())
        alt.append(alt_i)

    return transpose(array([dates,alt]))

def plot_airmass(objectlist,obsvat,date):
    #ax = plt.subplot(111)
    
    for obj in objectlist:
        altdata = compute_alt_plot(obj[0],obj[1],obsvat,date)
        plt.plot(altdata[:,0],altdata[:,1])


    morn_twilight,even_twilight = functions.calc_twilight(obsvat,date)
    

    plt.fill_betweenx([0,90],[morn_twilight.datetime(),morn_twilight.datetime()],x2=[even_twilight.datetime(),even_twilight.datetime()],color="0.5")

    locs,labels = plt.xticks()
    plt.setp(labels,rotation=45)
    plt.ylim(0,90)
    plt.show()


### Does a candidate transit on a night
def check_visible_transit(ra,dec,obsvat,date):
    



### Find candidates transiting on a night
#def find_transiting_hscandidates(obsvat,date,hatsplrank=5,CPHFU=None,PPHFU=None)



if __name__ == "__main__":
    #objectlist = [["2:31:48.7","-25:15:50.7"],["18:00:00","-10:00:00"],["10:00:00","-45:00:00"]]
    #plot_airmass(objectlist,"sso","2014/06/24")
