# Bedrock-Server-Mod-Manager
GUI mod management for dedicated Bedrock servers. Designed on Linux, works on Windows, powered by Python. 
Opens and modifies *server.properties* file, as well as re-ordering and activating installed addons. It works by reading through resource and behavior_packs folders, reads the manifests for each mod, and updates the world json files accordingly. Mod order is configurable. 

Be sure to change the WORLDS_DIR to your world directory (ie. /home/bedrock-server/worlds) in the mod_manager file.

Use *python3 application.py* to launch manager application within your terminal.

*Be sure to stop your server before making changes*

The mod manager can be used independently from the server manager (application.py) using *python3 mod_manager.py* 

In the Mod Manager, press 'space' to make selection, move up or down with 'ctrl+up/dn', view filepath with 'v', or delete with 'd'.

This is still a work in progress, and may not work for everyone, or at all. Backup your *server.properties* and your *world_resource/behavior_packs.json* in *~/PathTo/worlds/"Your World"/** before using. 
