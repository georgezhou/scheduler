import os,sys,ephem,string,mysql_query
from numpy import *

### Check of number is NaN
def isnan(num):
    return num == num

### Check if string is number
def is_number(s):
    test = False
    try:
        float(s)
        test = True
    except ValueError:
        test = False

    if test:
        test = isnan(s)
    return test

### Read ascii file function
def read_ascii(file_location):
    ascii_file_temp = []
    ascii_file = open(file_location).read()
    ascii_file = string.split(ascii_file,"\n")
    for i in range(len(ascii_file)):
        if not ascii_file[i] == "":
            if not ascii_file[i][0] == "#":
                ascii_file_temp.append(ascii_file[i])
    return ascii_file_temp

### Tables are passed on from read_ascii to read_table
def read_table(input_list):
    for i in range(len(input_list)):
        input_list[i] = string.split(input_list[i])
        input_list_temp = []
        for j in range(len(input_list[i])):
            if not input_list[i][j] == "":
                input_list_temp.append(input_list[i][j])
        input_list[i] = input_list_temp
        for j in range(len(input_list[i])):
            if is_number(input_list[i][j]):
                input_list[i][j] = float(input_list[i][j])
    return input_list


def load_observatories():
    observatories = read_table(read_ascii("observatories"))
    return observatories

observatories = load_observatories()

def return_observatory(obsvat):
    obs_found = False
    for obs in observatories:
        if obs[0] == obsvat:
            obs_found = True
            return obs
            break

    if not obs_found:
        print "Observatory not found"
        raise NameError("Observatory not found") 

def compute_alt_az(ra,dec,obsvat,date_time):
    obj = ephem.readdb("obj,f|M|F7,"+ra+","+dec+"0,2000")

    obsvat_data = return_observatory(obsvat)
    obsvat = ephem.Observer()
    obsvat.lat = obsvat_data[2]
    obsvat.lon = obsvat_data[1]
    obsvat.elevation = obsvat_data[3]
    obsvat.date = date_time

    obj.compute(obsvat)

    return obj.alt*180./pi,obj.az*180/pi

def calc_twilight(obsvat,date):
    obsvat_data = return_observatory(obsvat)
    obsvat = ephem.Observer()
    obsvat.lat = obsvat_data[2]
    obsvat.lon = obsvat_data[1]
    obsvat.elevation = obsvat_data[3]
    obsvat.date = date
    obsvat.horizon = "-12"

    sun = ephem.Sun()
    morn_twilight = obsvat.next_rising(sun)
    even_twilight = obsvat.next_setting(sun)

    return morn_twilight,even_twilight

def select_hscandidates(return_fields,hatsplrank=5,CPHFU=None,PPHFU=None,RV=None):

    ### Return fields: for example "HATSname,HATSra,HATSdec,HATSP,HATSE,HATSq"

    query = "select "+return_fields+",HATSTODO from HATS where HATSplrank <= "+str(hatsplrank)
    query_result = mysql_query.query_hscand(query)

    return_result = []

    def get_prio(prioname,hatstodo):
        prioexist = False

        for i in hatstodo:
            if prioname in i:
                prio = eval(string.split(i,":")[1])
                prioexist = True
                break

        if not prioexist:
            prio = 99
            
        return prio
                
    for entry in query_result:
        good_candidate = True

        hatstodo = string.split(entry[-1],",")

        if CPHFU != None:
            if get_prio("CPHFU",hatstodo) > CPHFU:
                good_candidate = False

        if PPHFU != None:
            if get_prio("PPHFU",hatstodo) > PPHFU:
                good_candidate = False                

        if RV != None:
            if get_prio("RV",hatstodo) > RV:
                good_candidate = False

        if good_candidate:
            return_result.append(entry)

    return return_result


### For testing
if __name__ == "__main__":
    #compute_alt_az("2:31:48.7","89:15:50.7","sso","2014/06/24 16:28:00")
    #calc_twilight("sso","2014/06/24")


    print select_hscandidates("HATSname,HATSra,HATSdec",hatsplrank=1,CPHFU=5)
