#find wsl WSL_IP
$ ip addr show eth0
192.168.0.229
#port fwd
$ netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=192.168.0.229

#show open ports
$ netsh interface portproxy show v4tov4

#release port
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=5000

#run reserved zrok endpoint (on win host)
PS C:\bin> .\zrok.exe reserve public 127.0.0.1:5000
    your reserved share token is '8ao7p7gfn784'
    reserved frontend endpoint: https://8ao7p7gfn784.share.zrok.io
c:\bin> .\zrok.exe share reserved 8ao7p7gfn784
