# slimeGPT
repo for the [slimeGPT workshop](https://wiki.idiot.io/slimeGPT)

## install deps
on windows WSL
```bash
git clone git@github.com:anonette/slimeGPT.git
cd slimeGPT

python -m venv venv
source venv/bin/activate
pip install openai flask
```

we are using [piper](https://github.com/rhasspy/piper) for text to speach.  follow piper [install](https://github.com/rhasspy/piper#installation) method.

we are using ffmpeg to playback the audio (for now)

### run
```bash
#you will need to supply an openai api_key
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxx"
python server.py
```

to test locally using curl
```bash
curl https://8ao7p7gfn784.share.zrok.io/tts -X POST -H "Content-Type: application/json"
```

or using android using [http-shortcut](https://http-shortcuts.rmy.ch/)

<details>
<summary>import the following json to the app to test</summary>

```json
{
  "categories": [
    {
      "id": "81e0defe-bb89-4c10-9113-d7ca2b75d469",
      "name": "Shortcuts",
      "shortcuts": [
        {
          "contentType": "application/json",
          "description": "test TTS ",
          "iconName": "flat_color_plugin",
          "id": "dc08b46b-d50b-443e-9b16-df272db84090",
          "method": "POST",
          "name": "tts public ",
          "responseHandling": {},
          "timeout": 0,
          "url": "https://8ao7p7gfn784.share.zrok.io/tts"
        }
      ]
    }
  ],
  "compatibilityVersion": 60,
  "version": 66
}
```

</details>


### network stuff
to keep the API keys hidden from the esp32 we run the api on a (local) server on my win pc. this means we need some kind of easy method to talk between the esp32 http endpoint and the server. 

to make the network connction easier we use [zrok](https://zrok.io), its an open zero-trust network layer that punches throu firewalls in public internet hotspots :)

```bash
#find wsl WSL_IP
$ ip addr show eth0
192.168.0.229
```
in powershell on windows host
```powershell
#port fwd
$ netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=192.168.0.229

#show open ports
$ netsh interface portproxy show v4tov4

#release port, if needed
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=5000
```
run zrok
```powershell
#run reserved zrok endpoint (on win host)
PS C:\bin> .\zrok.exe reserve public 127.0.0.1:5000
    your reserved share token is '8ao7p7gfn784'
    reserved frontend endpoint: https://8ao7p7gfn784.share.zrok.io
c:\bin> .\zrok.exe share reserved 8ao7p7gfn784
```
