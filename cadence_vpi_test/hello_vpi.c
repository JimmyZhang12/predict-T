#include <stdio.h>
#include "vpi_ams.h"
#include "vpi_user.h"
#include "vpi_user_cds.h"

void hello()
{
    printf("HELLO\n");
}

void register_hello()
{
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$hello";
    data.calltf=hello;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}
