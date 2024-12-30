function iprocPar = generateIprocPar()
    % 定义并初始化 iprocPar 结构体
    
    % 初始化结构体
    iprocPar = struct();

    % 定义字段及其默认值
    iprocPar.vsIndex = 'cn2';                           
    iprocPar.interfmethod = 'Coherence';                
    iprocPar.interftimespan = 'acausal+causal';         
    iprocPar.whiteNoise = 0.5;                          
    iprocPar.tfpresent = 'temporal';                    
    iprocPar.TWIN = 4;                                  
    iprocPar.paralFlag = 0;                             
    iprocPar.iterationFlag = 0;                         
end
