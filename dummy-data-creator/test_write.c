#include <stdio.h>
#include <stdint.h>

uint8_t R[35];

int main(){
    FILE *wf;
    uint8_t i = 0;
    for (i = 0 ; i<35; i++){
        R[i] = i;
    }
    
    wf = fopen( "out.bin","wb");
    fwrite(R,sizeof(uint8_t),35,wf);
    fclose(wf);
    
return 0;
}
