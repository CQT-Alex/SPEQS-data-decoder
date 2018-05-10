
# coding: utf-8

# In[94]:

#all the import statements are here. 
import numpy as np
import pandas as pd


# In[131]:

raw_data = None
bin_data = None
data = None
def load_data(file):
    global raw_data
    global bin_data
    global data
    raw_data  = np.fromfile(file, dtype='uint8')
    print("bytes loaded: {0}".format(len(raw_data)))
    #bin_data = raw_data.reshape(int(raw_data.shape[0]/(248)),248)
    bin_data = raw_data
    print("Number of data frames: {0}".format(bin_data.shape[0]) )
    #bin_data = raw_data.reshape(7,38)
    #bin_data = bin_data[:,1:-2].flatten()
    #bin_data = bin_data[:,1:-2][0] #just checking with one 245 byte frame
    bin_data = bin_data.reshape(int(bin_data.shape[0]/35),35)
    print("Number of event packets: {0}".format(bin_data.shape[0]) )
    tdf = pd.DataFrame(bin_data)
    tdf.to_csv("_byte_data.csv")
    data = bin_data
    
    
    
          
          
    


# In[106]:

print("test{0}".format(55))


# In[51]:




# In[52]:

#print in hex
##vhex = np.vectorize(hex)
##vhex(bin_data)

   

# In[53]:

#helper function
def create_word(barr):
    h = 0
    for b in reversed(barr):
        h = h << 8
        h = h | b
    #print (hex(h) )
    return h
    
def get_val(h, bitmask, r_shift ):
    val = (h&bitmask) >>r_shift
    return val


# In[54]:

#w = create_word(bin_data[1,0:3])


# In[55]:

##vhex(get_val(w,0xFFFFF,0) )


# In[56]:

def extract_column(data, begin_byte, end_byte,pattern, right_shift):
    warr = map(create_word,data[:,begin_byte:end_byte])
    r = [get_val(w,pattern,right_shift) for  w in warr]

    return r


# In[57]:

def APD1Top(data):
    return extract_column(data,0,3,0xFFFFF,0)
#vhex(APD1Top(bin_data))


# In[58]:

def APD2Top(data):
    return extract_column(data,2,5,0xFFFFF0,4)
#vhex(APD2Top(bin_data))


# In[59]:

def APD1Bot(data):
    return extract_column(data,5,8,0xFFFFF,0)
#vhex(APD1Bot(bin_data))


# In[60]:

def APD2Bot(data):
    return extract_column(data,7,10,0xFFFFF0,4)
#vhex(APD2Bot(bin_data))


# In[61]:

def coinc(data):
    return extract_column(data,10,13,0xFFFF,0)
#vhex(coinc(bin_data))


# In[62]:

def APD_DAC1(data):
    return extract_column(data,12,15,0xFFF,0)
#vhex(APD_DAC1(bin_data))


# In[63]:

def APD_DAC2(data):
    return extract_column(data,12,15,0xFFF000,12)
#vhex(APD_DAC2(bin_data))


# In[64]:

def thermistors_x_5(data):
    return data[:,16:21]

#vhex(thermistors_x_5(bin_data) )


# In[65]:

def Laser_DAC(data):
    return extract_column(data,21,23,0xFFF,0)
#vhex(Laser_DAC(bin_data))


# In[66]:

def LCPR_cap_pf(data):
    return extract_column(data,23,25,(0xFFF<<2),2)
#vhex(LCPR_cap_pf(bin_data))


# In[67]:

def LCPR_ref_i(data):
    return extract_column(data,23,25,0x3,0)
#vhex(LCPR_ref_i(bin_data))


# In[68]:

def LCPR_1(data):
    return extract_column(data,25,27,0xFFFF,0)
#vhex(LCPR_1(bin_data))


# In[69]:

def LCPR_2(data):
    return extract_column(data,27,29,0xFFFF,0)
#vhex(LCPR_2(bin_data))


# In[70]:

def LEPD_total(data):
    return extract_column(data,29,33,(0x3FF<<22),22)
#vhex(LEPD_total(bin_data))


# In[71]:

def LEPD_dX(data):
    return extract_column(data,29,33,(0x7FF<<11),11)
#vhex(LEPD_dX(bin_data))


# In[72]:

def LEPD_dY(data):
    return extract_column(data,29,33,(0x7FF),0)
#vhex(LEPD_dY(bin_data))


# In[73]:

def get_index(data):
    return extract_column(data,33,35,(0xFFFF),0)
#vhex(get_index(bin_data))


# In[116]:

def process(infile,outfile):
    print("loading:",infile)
    load_data(infile)
    COLUMN_NAMES = ["APDTop1","APDTop2","APDBot1","APDBot2",
                "Coincidence","APD_DAC1","APD_DAC2","T1",
                "T2","T3","T4","T5","Laser_DAC","LCPR_cap_pf",
                "LCPR_ref_i","LCPR_1","LCPR_2","LEPD_total",
                "LEPD_dX","LEPD_dY","index"]
    df = pd.DataFrame(columns=COLUMN_NAMES)
    data = bin_data
    
    df["APDTop1"] = APD1Top(data)
    df["APDTop2"] = APD2Top(data)
    df["APDBot1"] = APD1Bot(data)
    df["APDBot2"] = APD2Bot(data)
    df["Coincidence"] = coinc(data)
    df["APD_DAC1"] = APD_DAC1(data)
    df["APD_DAC2"] = APD_DAC2(data)
    T = thermistors_x_5(data)
    df["T1"] = T[:,0]
    df["T2"] = T[:,1]
    df["T3"] = T[:,2]
    df["T4"] = T[:,3]
    df["T5"] = T[:,4]
    df["Laser_DAC"] = Laser_DAC(data)
    df["LCPR_cap_pf"] = LCPR_cap_pf(data)
    df["LCPR_ref_i"] = LCPR_ref_i(data)
    df["LCPR_1"] = LCPR_1(data)
    df["LCPR_2"] = LCPR_2(data)
    df["LEPD_total"] = LEPD_total(data)
    df["LEPD_dX"] = LEPD_dX(data)
    df["LEPD_dY"] = LEPD_dY(data)
    df["index"] = get_index(data)
    df.to_csv(outfile)
    print("output written to:",outfile)


# In[132]:

process("out.bin","out_dummy.csv")


# In[125]:

##vhex(df[29:41])


# In[ ]:



