from BDNYCdb import BDdb
db=BDdb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')
DB_data=db.list("select names,ra,dec from sources").fetchall()
DA_data=np.genfromtxt('/Users/Joe/Desktop/obj_list.txt', delimiter=",", dtype=object)
def generate_DA_shortnames(DA_data):  
    allshortnames=[]
    allnames=[]
    wierdones=[]
    
    #For objects without shortnames
    for (name, ra, dec) in DA_data:
        shortname = get_shortname(name)
        allshortnames.append(shortname)
    
    data = np.concatenate([np.array([allshortnames]),DA_data.T]).T
    
    return data

#USED THIS FOR THE FINAL CODE 
def generate_DB_shortnames():
    """
    Generates shortnames for objects in need using designations and names    
    """
    need_sn = db.list("select id,names,designation from sources where shortname is null or shortname=''").fetchall()
    for source_id,names,designation in need_sn:
      shortname = ''
      if designation: shortname = get_shortname(designation)
      if names and not shortname: shortname = get_shortname(names)
      if shortname: 
        response = raw_input("Update source {} {} {} with shortname {}?[y,n] ".format(source_id,designation,names,shortname))
        if response=='y': db.list("update sources set shortname='{}' where id={}".format(shortname,source_id))
        else: print 'Not updated.'
    
def fix_RA(data):       
    for shortname,name,ra,dec in data:
      try:
        print db.list("select ra,dec from sources where shortname='{}'".format(shortname)).fetchone(), (ra,dec)
        db.dict("update sources set ra={}, dec={} where shortname='{}'".format(float(ra),float(dec),shortname)) 
      except: print 'No object with shortname '+shortname