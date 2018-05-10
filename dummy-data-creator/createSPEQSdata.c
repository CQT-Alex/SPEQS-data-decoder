/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/

#include <stdio.h>
#include <stdint.h>

#define uint32_t uint32_t
#define uint16_t uint16_t
#define uint8_t uint8_t

uint32_t count32_APDTop1Counter;
uint32_t count32_APDTop2Counter;
uint32_t count32_APDBot1Counter;
uint32_t count32_APDBot2Counter;
uint32_t count32_APDCoincidenceCounter;

uint16_t DAC1DigitalValue;
uint16_t DAC2DigitalValue;
uint16_t OPAMP1_DC_Offset;
uint16_t OPAMP2_DC_Offset;

uint8_t Thermistors_record[5] = {0xAB,0xCD,0xEF,0x12,0x34}; // [BUG]?? may be he is putting the thermo data from the next variable. that is why the data is always zero!!!
uint16_t Thermistors[5];
uint16_t TEMP_SetPt;

uint16_t LD_DAC;
uint32_t LEPDCurrents[4];
uint32_t LEPD_Total;
uint32_t LEPD_Mov_Total;
uint32_t uk_LD;
int32_t ek_LD; // never used. Should it be uint32_t ? 
uint16_t LD_Cons_Power_Mode;
uint16_t LD_Cons_Current_Mode;
uint32_t LEPD_Total_Stability_Buf[20];
uint8_t LD_Pow_Stability;
uint8_t LD_Stability_Index;

// uint16_t set_cap[9];
// uint8_t cap_set_counter;
float LC_meas_capacitance_pF;
uint16_t uk_LCPR_1;
uint16_t RC_1_fout_Hz;
float LC_1_capacitance_pF;
uint16_t uk_LCPR_2;
uint16_t RC_2_fout_Hz;
float LC_2_capacitance_pF;

uint16_t uk_LCPR_1_curr;
uint16_t uk_LCPR_2_curr; 

float dX;
float dY;

uint8_t LCPR_rotate_index;
uint8_t LCPR_sweep_index;
uint8_t LCPR_cap_ref_index;

float monitor_Buf[6];
float cap_monitor_Buf[6];
uint8_t Flash_sec_num;
uint16_t Flash_page_num;

uint16_t event_index;

uint32_t Random_Buffer[10];

uint8_t Min_Entropy;


// define a 35 byte structure to be compatible with the Flash memory
struct Expt_Record{
uint32_t APD_Counts[3];   // includes 20bit singles (x4) + 16bit coincidences
uint32_t APD_DACs;        // includes (x2) 12bit APD DAC settings
uint8_t Thermistors[5];  // includes 9bit thermistor readings (x5)
uint16_t Laser_DAC;
uint16_t LCPR[3];
uint32_t LEPD;
uint16_t index;
};

struct Expt_Record Entangled_Event;

uint8_t Expt_record_byte_form[35] = {0};          // This contains 1s data bytes (35) from a single event
uint8_t Rx_Buf[35];

void Struct_DataStuff(void){

	uint32_t temp_val;
    uint16_t temp_val1;
    uint8_t index = 0;
    
	count32_APDTop1Counter = 0x12345;
	count32_APDTop2Counter = 0xABCDE;
	count32_APDBot1Counter = 0x67890;
	count32_APDBot2Counter = 0x12345;
	count32_APDCoincidenceCounter = 0xABCD;
	DAC1DigitalValue = 0x051;
	DAC2DigitalValue = 0xCD2;
	
	LD_DAC = 0x567;
	
	LC_meas_capacitance_pF = (float) 0xDEF; //24 bits
	uk_LCPR_1 = 0x1234;
	uk_LCPR_2 = 0xABCD;
	
	LEPD_Total = 0x245; //10 bits
	dX = 0x723;//11 bits
	dY = 0x612; //11bits	
	LCPR_cap_ref_index = 0x2;
	Entangled_Event.APD_Counts[0] = Entangled_Event.APD_Counts[0] | (count32_APDTop1Counter & 0x000FFFFF);    // 20bits APD1 top singles
    
    temp_val = count32_APDTop2Counter;
    Entangled_Event.APD_Counts[0] = Entangled_Event.APD_Counts[0] | ((temp_val << 20) & 0xFFF00000);          // 12 LSB bits of APD2 top singles
    
    
    Entangled_Event.APD_Counts[1] = Entangled_Event.APD_Counts[1] | ((temp_val >> 12) & 0x000000FF);         // 8 MSB bits of APD2 top singles
    
    temp_val = count32_APDBot1Counter;    
	Entangled_Event.APD_Counts[1] =  Entangled_Event.APD_Counts[1] | ((temp_val << 8) & 0x0FFFFF00);         // 20bits APD1 bot singles
	
	
    temp_val = count32_APDBot2Counter;
    /*[BUG] !!Bug found in below line. Change main repo*/
    Entangled_Event.APD_Counts[1] = Entangled_Event.APD_Counts[1] | ((temp_val << 28) & 0xF0000000);          // 4 LSB bits of APD2 bot
    Entangled_Event.APD_Counts[2] = Entangled_Event.APD_Counts[2] | ((temp_val >> 4) & 0x0000FFFF);           // 16 MSB bits of APD2 bot
    
    temp_val = count32_APDCoincidenceCounter;
    Entangled_Event.APD_Counts[2] = Entangled_Event.APD_Counts[2] | ((temp_val << 16) & 0xFFFF0000);        // 16 bit coincidences
 		
    temp_val1 = DAC1DigitalValue;
	Entangled_Event.APD_DACs = temp_val1 & 0x00000FFF;                                                      // 12 bit ADC1 value
    
    temp_val = DAC2DigitalValue;
    Entangled_Event.APD_DACs = Entangled_Event.APD_DACs | ((temp_val << 12) & 0x00FFF000);                  // 12 bit ADC2 value
    
    for (index = 0 ; index < 5 ; index++){                                                                  // 5x thermistor readings in Celsius
    Entangled_Event.Thermistors[index] = Thermistors_record[index];
    }
    
    temp_val1 = LD_DAC;
	Entangled_Event.Laser_DAC = temp_val1 & 0x0FFF;                                                          // 12 bit LD dac
    
    temp_val = (uint32_t) LC_meas_capacitance_pF;  // 12 bits to represent the meas. capacitance  
    temp_val = temp_val << 2;
	temp_val = temp_val + (LCPR_cap_ref_index & 0x03);    // 2 bits for ref. capacitance
	Entangled_Event.LCPR[0] = temp_val;
    
    Entangled_Event.LCPR[1] = uk_LCPR_1;
    Entangled_Event.LCPR[2] = uk_LCPR_2;
	
	temp_val = LEPD_Total & 0x000003FF;	        // 10 bits
	temp_val = (temp_val << 22) & 0xFFC00000;
    Entangled_Event.LEPD = temp_val;
	
	temp_val = dX;
    temp_val = (temp_val << 11) & 0x003FF800;   // 11 bits
    Entangled_Event.LEPD = Entangled_Event.LEPD + temp_val;
    
    temp_val = dY;
    temp_val = temp_val & 0x000007FF;           // 11 bits
	Entangled_Event.LEPD = Entangled_Event.LEPD + temp_val;
    
    //index 16 bits
    
    //[BUG] index assignment missing
    //test print
    printf("%0x\n%0x\n%0x\n",Entangled_Event.APD_Counts[0],Entangled_Event.APD_Counts[1],Entangled_Event.APD_Counts[2]);
}

// convert structure data to byte format
void Struct_Data_Array(struct Expt_Record *Entangled_Event_ptr){
    
    
    uint8_t i = 0;
    uint32_t temp;
    uint16_t temp1;
    
    for(i = 0 ; i < 3 ; i++){
        temp = Entangled_Event_ptr->APD_Counts[i]; 
        //Expt_record_byte_form[4*i] = (uint8_t) temp;  // LSB
        Rx_Buf[4*i] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_Counts[i]>>8; 
        //Expt_record_byte_form[4*i+1] = (uint8_t) temp;  // 2nd byte
        Rx_Buf[4*i+1] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_Counts[i]>>16; 
        //Expt_record_byte_form[4*i+2] = (uint8_t) temp;  // 3rd byte
        Rx_Buf[4*i+2] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_Counts[i]>>24; 
        //Expt_record_byte_form[4*i+3] = (uint8_t) temp;  // MSB
        Rx_Buf[4*i+3] = (uint8_t) temp;
    }
    
        temp = Entangled_Event_ptr->APD_DACs;
        //Expt_record_byte_form[12] = (uint8_t) temp;   // LSB
        Rx_Buf[12] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_DACs>>8;
        //Expt_record_byte_form[13] = (uint8_t) temp;   // 2nd byte
        Rx_Buf[13] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_DACs>>16;
        //Expt_record_byte_form[14] = (uint8_t) temp;   // 3rd byte
        Rx_Buf[14] = (uint8_t) temp;
        temp = Entangled_Event_ptr->APD_DACs>>24;
        //Expt_record_byte_form[15] = (uint8_t) temp;   // MSB
        Rx_Buf[15] = (uint8_t) temp;
    
    for(i = 0 ; i<5 ; i++){
        //Expt_record_byte_form[16+i] = Entangled_Event_ptr->Thermistors[i];
        Rx_Buf[16+i] = Entangled_Event_ptr->Thermistors[i];
    }
    
        temp1 = Entangled_Event_ptr->Laser_DAC;
        //Expt_record_byte_form[21] = (uint8_t) temp1;
        Rx_Buf[21] = (uint8_t) temp1;
        temp1 = Entangled_Event_ptr->Laser_DAC>>8;
        //Expt_record_byte_form[22] = (uint8_t) temp1;
        Rx_Buf[22] = (uint8_t) temp1;
        
    for(i = 0 ; i<3 ; i++){
        temp1 = Entangled_Event_ptr->LCPR[i]; 
        //Expt_record_byte_form[23+3*i] = (uint8_t) temp1;  // LSB
        Rx_Buf[23+2*i] = (uint8_t) temp1;  // LSB
        temp1 = Entangled_Event_ptr->LCPR[i]>>8; 
        //Expt_record_byte_form[24+3*i] = (uint8_t) temp1;  // MSB
        Rx_Buf[24+2*i] = (uint8_t) temp1;  // LSB
    }
        
        temp = Entangled_Event_ptr->LEPD;
        Rx_Buf[29] = (uint8_t) temp;
        
        temp = Entangled_Event_ptr->LEPD;
        Rx_Buf[30] = (uint8_t) (temp >> 8);
        
        temp = Entangled_Event_ptr->LEPD;
        Rx_Buf[31] = (uint8_t) (temp >> 16);
        
        temp = Entangled_Event_ptr->LEPD;
        Rx_Buf[32] = (uint8_t) (temp >> 24);
        
        temp1 = Entangled_Event_ptr->index;
        Rx_Buf[33] = (uint8_t) temp1;
        
        temp1 = Entangled_Event_ptr->index>>8;
        Rx_Buf[34] = (uint8_t) temp1;
        
}

int main(void){
    int i,j;
    
    Struct_DataStuff();
    
    Struct_Data_Array(&Entangled_Event);
    FILE *hfp;
    
    
    FILE *fp;
    fp = fopen("out.bin","wb");
    for (i = 0; i< 7;i++){
        fwrite(Rx_Buf,sizeof(uint8_t),35,fp);
    }
    fclose(fp);
    for (i=0;i<35;i++){
        printf("%0x ",(int)Rx_Buf[i]);
    }
    printf("\n");
    hfp = fopen("hexout.txt","w");
    for (i=0;i<7;i++){
        for (j=0;j<35;j++){
            fprintf(hfp,"%02X ", Rx_Buf[j]);
        }
        fprintf(hfp,"\n");
    }
    
    return 0; //compile test
}

/* [] END OF FILE */
