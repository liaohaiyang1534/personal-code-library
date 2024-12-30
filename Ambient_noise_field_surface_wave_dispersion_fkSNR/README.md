Demos for passive surface wave imaging techniques, including data processing, quality control, and imaging enhancement, used in USTC seismo training class in 2023 July.

3 demos are packed inside ./demo directory, and the dependent MATLAB modules are stored inside ./codes directory. please also find the related journal papers inside ./doc directory. 

Questions and comments? Email Feng Cheng (fengcheng@zju.edu.cn)

May you guys find these demos helpful! Good luck with the class! 

-F. Cheng (程逢)
July, 2023

references:

Cheng, F., Xia, J., Zhang, K., Zhou, C., & Ajo-Franklin, J. B. (2021). Phase-weighted slant stacking for surface wave dispersion measurement. Geophysical Journal International, 226(1), 256–269. https://doi.org/10.1093/gji/ggab101
Cheng, F., Xia, J., & Xi, C. (2023). Artifacts in High-Frequency Passive Surface Wave Dispersion Imaging: Toward the Linear Receiver Array | SpringerLink. Surveys in Geophysics. https://link.springer.com/article/10.1007/s10712-023-09772-1
Cheng, F., Ajo-Franklin, J., Rodriguez Tribaldos, V., and the Imperial Valley Dark Fiber Team (2023). High-resolution near-surface imaging at the basin scale using dark fiber and distributed acoustic sensing: towards site effect estimation in urban environments. JGR: Solid Earth. (doi will coming soon)

the directory tree: 
.
├── codes
│         ├── Interf
│         │        ├── Interferometry.m
│         │        ├── copstacking.m
│         │        ├── matrixInterf_index.m
│         │        └── mkvsg_InterfSeis.m
│         ├── fkSNR
│         │        ├── FPhaseshift2fk2.m
│         │        ├── fkfanfilter.m
│         │        ├── phaseshiftdsp2fk.m
│         │        ├── s_calfkSNR.m
│         │        └── s_localselectfunction2.m
│         ├── misc
│         │        ├── between.m
│         │        ├── col2row.m
│         │        ├── fclc.m
│         │        ├── fftrl.m
│         │        ├── flt2str.m
│         │        ├── gcdSTR.m
│         │        ├── ifftrl.m
│         │        ├── inpoly2.m
│         │        ├── inpoly2_mat.m
│         │        ├── norm1d.m
│         │        ├── norm2d.m
│         │        ├── sTenv.m
│         │        └── smooth2a.m
│         ├── plt
│         │        ├── pltdsp.m
│         │        ├── pltseis.m
│         │        ├── pltspec_AmbiSeis.m
│         │        ├── pltspec_InterfSeis.m
│         │        ├── pltxt_AmbiSeis.m
│         │        ├── pltxt_InterfSeis.m
│         │        ├── setplt.m
│         │        ├── turbo.m
│         │        └── wigb.m
│         ├── preProc
│         │        ├── rmmean.m
│         │        ├── runSmooth.m
│         │        └── whiten.m
│         └── pwslantstacking
│             ├── FPhaseshift.m
│             ├── Fstack.m
│             ├── README.md
│             └── phaseshiftdsp.m
├── demo
│         ├── demo1-2018.12.XiXi-Geophone
│         │        ├── AmbiSeis.mat
│         │        ├── demo1_workflow.m
│         │        ├── demo1_workflow.mlx
│         │        └── demo1_workflow.pdf
│         ├── demo2-2021.03.IVDF-DAS
│         │        ├── AmbiSeis-IVDF-DAS20210302-ch6350-6374.mat
│         │        ├── InterfSeis_workspace.mat
│         │        ├── demo2_fkSNR.m
│         │        ├── demo2_fkSNR.mlx
│         │        ├── demo2_fkSNR.pdf
│         │        ├── fkSNR-workspace.mat
│         │        └── ivdfx100m-fk-target-fundamental.mat
│         └── demo3-pwslantStacking
│             ├── demo3_dcImage.m
│             ├── demo3_dcImage.mlx
│             ├── demo3_dcImage.pdf
│             └── synthetic-seismic-data.mat
└── doc
    ├── Cheng_et_al_2021_Phase-weighted-slant-stacking.pdf
    ├── Cheng_et_al_2023-JGR-IVDF.pdf
    └── Cheng_et_al_2023-SIG-Artifacts.pdf



