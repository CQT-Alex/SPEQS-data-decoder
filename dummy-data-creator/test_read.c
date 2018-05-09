#include <stdio.h>
#include <stdint.h>

uint8_t R[35];

int main(){
    FILE *rf;
    uint8_t i = 0;
    for (i = 0 ; i<35; i++){
        R[i] = i;
    }
    
    rf = fopen( "out.bin","rb");
    fread(R,sizeof(uint8_t),35,rf);
    fclose(rf);
    for (i = 0 ; i<35; i++){
        printf("%0x ",(int)R[i]);
    }
    printf("\n");
return 0;
}
