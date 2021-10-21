# Spotifarr

<p>This is a small python code that I use with my NAS server connected to Plex<br />I didn't appreciate how Lidarr works because it downloads a full Album. So I created something on my own.</p>
<h2>Way of working</h2>
<ul>
<li>The python script will connect to your Spotify and will retrieve your playlists using <a href="https://github.com/plamere/spotipy">spotipy</a>&nbsp;package</li>
<li>The python script will create an SQL database with your playlist &amp; the list of tracks</li>
<li>The python script will then search a youtube video based on the name &amp; the artist gathered from the metadata (it will search in YouTube music and if not found YouTube videos)</li>
<li>The python script will download the video in .mp3 using <a href="https://github.com/ytdl-org/youtube-dl">youtube-dl</a> package</li>
<li>The python script will update the metadata and prepare it for plex using <a href="https://github.com/quodlibet/mutagen">mutagen</a></li>
<li>Finally, the python script will trigger an update and will create the same playlist that is in your Spotify in plex using <a href="https://github.com/pkkid/python-plexapi">PlexAPI</a></li>
</ul>
<h2>Configuration</h2>
<p>To make the script work you need to configure the document <a class="js-navigation-open Link--primary" title="credentials.json" href="https://github.com/Khormologia/Spotifarrr/blob/main/config/credentials.json" data-pjax="#repo-content-pjax-container">credentials.json</a></p>
<ul>
<li>"username": "your spotify username found in <a href="https://www.spotify.com/us/account/overview/">Overview</a>"</li>
</ul>
<p>You need then to create a spotify APP - <a href="https://developer.spotify.com/dashboard/">Spotify for developers</a> to retrieve both of these parameters&nbsp;</p>
<ul>
<li>"client_id": "",</li>
<li>"client_secret": "",</li>
</ul>
<p>Define the location of where you will save your media (for me I used /media/Music )</p>
<ul>
<li>"path_music": "",</li>
</ul>
<p>(Optional) You can create a password app to allow youtube-dl to download explicit music, else you can leave it blank</p>
<ul>
<li>"ytb_username": "",</li>
<li>"ytb_password": "",</li>
</ul>
<p>Now to configure plex you need to enter the base URL for example <a href="http://localhost:32400/">http://localhost:32400/</a> and for the token, you can follow-up <a href="https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/">Plex tutorial</a>&nbsp;</p>
<ul>
<li>"plex_base_url": "",</li>
<li>"plex_token": ""</li>
</ul>
<h2>Requirements</h2>
<p>If you are running on windows you can install all the pip found in the <a href="https://github.com/Khormologia/Spotifarrr/blob/main/setup/requirements.txt">requirement.txt</a></p>
<p>Else on FreeBSD you need to install:</p>
<p>pkg install python, py38-sqlite3</p>
<h2>Run</h2>
<p>Now you only have to run main.py and enjoy</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>PS:</p>
<ol>
<li>I tried to create a web interface using FLASK but I'm still in the learning process. So sorry for that.</li>
<li>If you want to have daily monitoring you can add a corn job for main.py and&nbsp;</li>
<li>I created this for fun and not for business use. I am always enrolled in Spotify premium services but I just wanted to try. So please I do not encourage any prohibited behavior&nbsp;</li>
</ol>
