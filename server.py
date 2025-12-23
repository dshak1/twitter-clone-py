from flask import Flask, request, jsonify, render_template_string
import heapq
from typing import List

class twitter:
    def __init__(self):
        self.time = 0
        self.followers = {}
        self.following = {}
        self.tweets = {}  # Added missing tweets initialization

    def postTweet(self, userId: int, tweetId: int) -> None:
        if userId not in self.tweets:
            self.tweets[userId] = []
        if userId not in self.following:
            self.following[userId] = set()

        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        if userId not in self.following:
            self.following[userId] = set()
        if userId not in self.tweets:
            self.tweets[userId] = []

        followees = set(self.following[userId])
        followees.add(userId)

        heap = []  # (-time, tweetId, authorId, index)
        for uid in followees:
            if uid not in self.tweets:
                self.tweets[uid] = []
            if uid not in self.following:
                self.following[uid] = set()

            tlist = self.tweets[uid]
            if tlist:
                idx = len(tlist) - 1
                t, tid = tlist[idx]
                heapq.heappush(heap, (-t, tid, uid, idx))

        res = []
        while heap and len(res) < 10:
            _, tid, uid, idx = heapq.heappop(heap)
            res.append(tid)

            idx -= 1
            if idx >= 0:
                t, tid2 = self.tweets[uid][idx]
                heapq.heappush(heap, (-t, tid2, uid, idx))

        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        if followerId not in self.following:
            self.following[followerId] = set()
        if followerId not in self.tweets:
            self.tweets[followerId] = []
        if followeeId not in self.following:
            self.following[followeeId] = set()
        if followeeId not in self.tweets:
            self.tweets[followeeId] = []

        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        if followerId not in self.following:
            self.following[followerId] = set()
        # if not following, discard does nothing anyway
        self.following[followerId].discard(followeeId)


# Create Flask app and Twitter instance
app = Flask(__name__)
twitter_app = twitter()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Clone Python</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container { 
            background: white; 
            border-radius: 10px; 
            padding: 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #1da1f2; 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .section { 
            margin: 25px 0; 
            padding: 20px; 
            border: 2px solid #1da1f2; 
            border-radius: 10px; 
            background: #f8f9fa;
        }
        .section h3 {
            color: #1da1f2;
            margin-top: 0;
            font-size: 1.3em;
        }
        input, button { 
            margin: 8px; 
            padding: 12px; 
            border-radius: 6px;
            border: 1px solid #ddd;
            font-size: 14px;
        }
        button { 
            background: #1da1f2; 
            color: white; 
            border: none; 
            cursor: pointer; 
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover { 
            background: #0d95e8; 
            transform: translateY(-1px);
        }
        #newsfeed { 
            background: #e3f2fd; 
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }
        .tweet { 
            background: white; 
            margin: 12px 0; 
            padding: 15px; 
            border-radius: 8px; 
            border-left: 4px solid #1da1f2;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .python-badge {
            background: #3776ab;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            float: right;
        }
        .performance-note {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Twitter Clone <span class="python-badge">Python Backend</span></h1>
        
        <div class="performance-note">
            <strong>🔬 Performance Test:</strong> Compare this Python Flask server (port 5000) 
            with the C++ server (port 8080) to see the speed difference!
        </div>
        
        <div class="section">
            <h3>📝 Post Tweet</h3>
            <input type="number" id="postUserId" placeholder="User ID" />
            <input type="number" id="tweetId" placeholder="Tweet ID" />
            <button onclick="postTweet()">Post Tweet</button>
        </div>

        <div class="section">
            <h3>👥 Follow/Unfollow</h3>
            <input type="number" id="followerId" placeholder="Follower ID" />
            <input type="number" id="followeeId" placeholder="Followee ID" />
            <button onclick="followUser()">Follow</button>
            <button onclick="unfollowUser()">Unfollow</button>
        </div>

        <div class="section">
            <h3>📰 News Feed</h3>
            <input type="number" id="feedUserId" placeholder="User ID" />
            <button onclick="getNewsFeed()">Get News Feed</button>
            <div id="newsfeed"></div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:3000';
        
        function postTweet() {
            const userId = document.getElementById('postUserId').value;
            const tweetId = document.getElementById('tweetId').value;
            
            fetch(`${API_BASE}/postTweet?userId=${userId}&tweetId=${tweetId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('✅ Tweet posted: ' + data.message));
        }

        function followUser() {
            const followerId = document.getElementById('followerId').value;
            const followeeId = document.getElementById('followeeId').value;
            
            fetch(`${API_BASE}/follow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('✅ Followed: ' + data.message));
        }

        function unfollowUser() {
            const followerId = document.getElementById('followerId').value;
            const followeeId = document.getElementById('followeeId').value;
            
            fetch(`${API_BASE}/unfollow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('✅ Unfollowed: ' + data.message));
        }

        function getNewsFeed() {
            const userId = document.getElementById('feedUserId').value;
            const startTime = performance.now();
            
            fetch(`${API_BASE}/getNewsFeed?userId=${userId}`)
                .then(response => response.json())
                .then(data => {
                    const endTime = performance.now();
                    const responseTime = (endTime - startTime).toFixed(2);
                    
                    const feedDiv = document.getElementById('newsfeed');
                    feedDiv.innerHTML = `<h4>📋 Latest Tweets (${responseTime}ms response time):</h4>`;
                    if (data.length === 0) {
                        feedDiv.innerHTML += '<p>No tweets in feed</p>';
                    } else {
                        data.forEach(tweetId => {
                            feedDiv.innerHTML += `<div class="tweet">🐦 Tweet ID: ${tweetId}</div>`;
                        });
                    }
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/postTweet', methods=['POST'])
def post_tweet():
    user_id = int(request.args.get('userId', 0))
    tweet_id = int(request.args.get('tweetId', 0))
    
    twitter_app.postTweet(user_id, tweet_id)
    return jsonify({"status": "success", "message": "Tweet posted via Python!"})

@app.route('/getNewsFeed', methods=['GET'])
def get_news_feed():
    user_id = int(request.args.get('userId', 0))
    
    feed = twitter_app.getNewsFeed(user_id)
    return jsonify(feed)

@app.route('/follow', methods=['POST'])
def follow():
    follower_id = int(request.args.get('followerId', 0))
    followee_id = int(request.args.get('followeeId', 0))
    
    twitter_app.follow(follower_id, followee_id)
    return jsonify({"status": "success", "message": "Followed user via Python!"})

@app.route('/unfollow', methods=['POST'])  
def unfollow():
    follower_id = int(request.args.get('followerId', 0))
    followee_id = int(request.args.get('followeeId', 0))
    
    twitter_app.unfollow(follower_id, followee_id)
    return jsonify({"status": "success", "message": "Unfollowed user via Python!"})

if __name__ == '__main__':
    print("🐍 Python Flask Twitter Server starting on http://localhost:3000")
    print("🔬 Compare performance with C++ server at http://localhost:8080")
    app.run(host='localhost', port=3000, debug=True)