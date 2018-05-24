
# coding: utf-8

# In[2]:

#all the import statements are here. 
import numpy as np
import pandas as pd


# In[31]:

raw_data = None
bin_data = None
data = None
def load_data(file):
    global raw_data
    global bin_data
    global data
    raw_data  = np.fromfile(file, dtype='uint8')
    print("bytes loaded: {0}".format(len(raw_data)))
    bin_data = raw_data.reshape(int(raw_data.shape[0]/(248)),248)
    #bin_data = raw_data
    print("Number of data frames: {0}".format(bin_data.shape[0]) )
    #bin_data = raw_data.reshape(7,38)
    bin_data= bin_data[:,0:-3].flatten()
    #bin_data = bin_data[:,1:-2].flatten()
    #bin_data = bin_data[:,1:-2][0] #just checking with one 245 byte frame
    bin_data = bin_data.reshape(int(bin_data.shape[0]/35),35)
    print("Number of event packets: {0}".format(bin_data.shape[0]) )
    #tdf = pd.DataFrame(bin_data)
    #tdf.to_csv("_byte_data.csv")
    #data = bin_data
    np.savetxt('_byte_data.csv', bin_data, delimiter=',')   # X is an array
    #return bin_data
    
load_data("data/S1_1_n")          
          
    


# In[4]:

print("test{0}".format(55))


# In[5]:

##print in hex
vhex = np.vectorize(hex)
#vhex(bin_data)


# In[6]:

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


# In[7]:

#w = create_word(bin_data[1,0:3])


# In[8]:

#vhex(get_val(w,0xFFFFF,0) )


# In[9]:

def extract_column(data, begin_byte, end_byte,pattern, right_shift):
    warr = map(create_word,data[:,begin_byte:end_byte])
    r = [get_val(w,pattern,right_shift) for  w in warr]

    return r


# In[10]:

def APD1Top(data):
    return extract_column(data,0,3,0xFFFFF,0)
#vhex(APD1Top(bin_data))


# In[11]:

def APD2Top(data):
    return extract_column(data,2,5,0xFFFFF0,4)
#vhex(APD2Top(bin_data))


# In[12]:

def APD1Bot(data):
    return extract_column(data,5,8,0xFFFFF,0)
#vhex(APD1Bot(bin_data))


# In[13]:

def APD2Bot(data):
    return extract_column(data,7,10,0xFFFFF0,4)
#vhex(APD2Bot(bin_data))


# In[14]:

def coinc(data):
    return extract_column(data,10,13,0xFFFF,0)
#vhex(coinc(bin_data))


# In[15]:

def APD_DAC1(data):
    return extract_column(data,12,15,0xFFF,0)
#vhex(APD_DAC1(bin_data))


# In[16]:

def APD_DAC2(data):
    return extract_column(data,12,15,0xFFF000,12)
#vhex(APD_DAC2(bin_data))


# In[17]:

def thermistors_x_5(data):
    return data[:,16:21]

#vhex(thermistors_x_5(bin_data) )


# In[18]:

def Laser_DAC(data):
    return extract_column(data,21,23,0xFFF,0)
#vhex(Laser_DAC(bin_data))


# In[19]:

def LCPR_cap_pf(data):
    return extract_column(data,23,25,(0xFFF<<2),2)
#vhex(LCPR_cap_pf(bin_data))


# In[20]:

def LCPR_ref_i(data):
    return extract_column(data,23,25,0x3,0)
##vhex(LCPR_ref_i(bin_data))


# In[21]:

def LCPR_1(data):
    return extract_column(data,25,27,0xFFFF,0)
#vhex(LCPR_1(bin_data))


# In[22]:

def LCPR_2(data):
    return extract_column(data,27,29,0xFFFF,0)
#vhex(LCPR_2(bin_data))


# In[23]:

def LEPD_total(data):
    return extract_column(data,29,33,(0x3FF<<22),22)
#vhex(LEPD_total(bin_data))


# In[24]:

def LEPD_dX(data):
    return extract_column(data,29,33,(0x7FF<<11),11)
#vhex(LEPD_dX(bin_data))


# In[25]:

def LEPD_dY(data):
    return extract_column(data,29,33,(0x7FF),0)
#vhex(LEPD_dY(bin_data))


# In[26]:

def get_index(data):
    return extract_column(data,33,35,(0xFFFF),0)
#vhex(get_index(bin_data))


# In[98]:

def process(infile,outfile):
    print("loading:",infile)
    #bin_data = load_data(infile)
    COLUMN_NAMES = ["APDTop1","APDTop2","APDBot1","APDBot2",
                "Coincidence","APD_DAC1","APD_DAC2","T1",
                "T2","T3","T4","T5","Laser_DAC","LCPR_cap_pf",
                "LCPR_ref_i","LCPR_1","LCPR_2","LEPD_total",
                "LEPD_dX","LEPD_dY","Index"]
    df = pd.DataFrame(columns=COLUMN_NAMES)
    
    ind_list = get_index(bin_data)
    heater_begin = 14
    heater_end = ind_list[heater_begin:].index(0) + heater_begin
    
    data = bin_data[heater_end:]
    
    df["APDTop1"] = APD1Top(data)
    df["APDTop2"] = APD2Top(data)
    df["APDBot1"] = APD1Bot(data)
    df["APDBot2"] = APD2Bot(data)
    df["Coincidence"] = coinc(data)
    df["APD_DAC1"] = APD_DAC1(data)
    df["APD_DAC2"] = APD_DAC2(data)
    T = thermistors_x_5(data)
    df["T1"] = T[:,0].astype(int) *4
    df["T2"] = T[:,1].astype(int) *4
    df["T3"] = T[:,2].astype(int) *4
    df["T4"] = T[:,3].astype(int) *4
    df["T5"] = T[:,4].astype(int) *4
    df["Laser_DAC"] = Laser_DAC(data)
    df["LCPR_cap_pf"] = LCPR_cap_pf(data)
    df["LCPR_ref_i"] = LCPR_ref_i(data)
    df["LCPR_1"] = LCPR_1(data)
    df["LCPR_2"] = LCPR_2(data)
    df["LEPD_total"] = LEPD_total(data)
    df["LEPD_dX"] = LEPD_dX(data)
    df["LEPD_dY"] = LEPD_dY(data)
    df["Index"] = get_index(data)
    df = df.drop_duplicates() # 
    df = df[df.Index !=65535  ]
    
    df.to_csv(outfile)
    print("output written to:",outfile)


# In[99]:

process("data/heater-test/S12_1_n","out_S12.csv")
#process("out.bin","out_dummy.csv")


# In[100]:

def get_heating_data(infile, outfile): #("data/heater-test/S12_1_n","out_S12.csv")
    global bin_data
    #df = pd.DataFrame(columns=COLUMN_NAMES)
    data = bin_data
    ind_list = get_index(data)
    heater_begin = 14
    heater_end = ind_list[heater_begin:].index(0) + heater_begin
    
    hdata = data[heater_begin:heater_end].astype(dtype='uint16') *4
    
    np.savetxt(outfile, hdata, delimiter=",")
    #print(hdata)
    
    #print (heater_begin,heater_end)
    #print( ind_list [heater_end])
    #print (ind_list)
    
get_heating_data("data/heater-test/S12_1_n","heat_S12.csv")


# In[ ]:



