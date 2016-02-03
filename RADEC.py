from astrodbkit.astrodbkit import astrodb
import numpy as np
import re 
db=astrodb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')
DB_data=db.query("select names,ra,dec from sources")
#DA_data=np.genfromtxt('/Users/Joe/Desktop/obj_list.txt', delimiter=",", dtype=object)

#Function to generate shortnames from a given name for a list of objects
def get_shortname(name):
    #Establishes whether a given name has a "+" or a "-"  
    if "+" in name:
        n="+"
    else:
        n="-"
      
    #Splits up the name on a whitespace   
    com="ABab"
    nums="1234567890"
    q=re.split("\W+", name)
  
    #For the easiest names, where it is just "Survey J123456+78900"
    if len(q)==3:
        partone=q[1]
        parttwo=q[2]
      
        #Accounts for objects with names that have three parts seperated by a whitespace, but are not structured like "Survey J123456+78900"
        if partone[0]!="J":
            shortname = ''
            
          
        #Deals with objects that are structured properly 
        else:
            shortone=partone[1:5]
            if shortone[0] and shortone [1] and shortone [2] and shortone[3] in nums:
              
                #Deals with AB at the end
                if parttwo[-1] in com and parttwo[-2] in com: 
                    shorttwo=parttwo[:4]
                    shortname=shortone+n+shorttwo
                  
                #For companions     
                elif parttwo[-1] in com:
                    shorttwo=parttwo[:4]+parttwo[-1]
                    shortname= shortone+n+shorttwo
                  
                #For isolated objects
                else:
                    shorttwo=parttwo[:4]
                    shortname=shortone+n+shorttwo

            else:
                shortname = ''
              
    #For objects with a "." in their name, of which there were quite a few. It gives an object like "2MASS 123.4+567.8" the shortname "1234+5678"            
    if len(q)>3:  
        t=re.sub(r"\.",r"",name)
        o=re.split("\W+", t)
        p1=o[1]
        p2=o[2]
      
        #For objects like "Denis-P" that have an extra letter
        if len(p1)==1:
            partone=o[2]
            parttwo=o[3]
          
            #Gets rid of objects that don't start with "J"
            if partone[0]!="J":
                shortname = ''
                
        else:
            partone=p1
            parttwo=p2
            if partone[0]!="J":
                shortname = ''
                
        shortone=partone[1:5]
        if len(shortone)<4:
            shortname = ''
            
        elif shortone[0] and shortone [1] and shortone [2] and shortone[3] in nums:
            shortone=partone[1:5]
          
            #Deals with AB at the end
            if parttwo[-1] in com and parttwo[-2] in com: 
                shorttwo=parttwo[:4]
                shortname=shortone+n+shorttwo
              
            #Deals with companions
            elif parttwo[-1] in com:
                shorttwo=parttwo[:4]+parttwo[-1]
                shortname= shortone+n+shorttwo
              
            #Deals with isolated objects
            else:
                shorttwo=parttwo[:4]
                shortname=shortone+n+shorttwo
          
        else:
            shortname = ''         
          
    #Passes on objects with "q" values less than 3    
    if len(q)<3: 
        shortname = ''
    
    #Gets rid of any weird shortnames before priting
    for letter in shortname:
        if letter not in nums:
            if letter not in com:
                shortname = ''
    return shortname
