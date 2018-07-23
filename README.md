# Song-Recommender-Spotify-
* Originally deployed on Heroku, but something changed and it doesn't work, so I'm posting here *
Takes a Spotify username and displays the user's public playlists. Then it displays 10 recommended songs.
## Usage
Install directory. Then open terminal and go to the directory. Install requirements through pip:
<code>pip install -r requirements.txt</code> or <code>pip3 install -r requirements</code>
Then, run
<code>python3 flaskrec.py</code>
Which will open the webpage on localhost:5000
## Algorithm
I used Spotify's API along with Spotipy a Spotify API python wrapper.
I used the audio features from the API to gather the data along with all the related artists from the playlist.
I trim the playlist by removing songs that are furthest away from each other to remove outliers and songs that don't resemble
the playlist as well as reduce the number of API calls.

Once I had all the data, I K-Nearest-Neighbor algorithm with a majority vote of summing instead of classification. I used
euclidean distances to find the distances.
## Goals
1. Exposure to API's and gathering data on a larger scale.
2. Learn the balance between number of API calls (too many is too slow and too many will result in an error)
3. Using my knowlege of basic data-science algorithms for real-world applications
4. Understand the differences between NodeJS and Flask and the strengths of each
5. Exposure to the workflow of testing on iPython Notebooks and translating that to the text editor
## Todo:
- [] Tweak algorithm (accuracy and time-efficiency)
- [] Connect database for possible memoization
