#!/usr/bin/env python3
from flask import Flask, request, jsonify
import heapq
from typing import List

class Twitter:
    def __init__(self):
        self.time = 0
        self.followers = {}
        self.following = {}
        self.tweets = {}

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

        heap = []
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
        self.following[followerId].discard(followeeId)


app = Flask(__name__)
twitter_app = Twitter()

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Clone Python</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f0f8ff; }
        .container { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #1da1f2; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 2px solid #1da1f2; border-radius: 8px; background: #f8f9fa; }
        input, button { margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
        button { background: #1da1f2; color: white; border: none; cursor: pointer; font-weight: bold; }
        button:hover { background: #0d95e8; }
        #newsfeed { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .tweet { background: white; margin: 10px 0; padding: 10px; border-radius: 5px; border-left: 4px solid #1da1f2; }
        .python-badge { background: #3776ab; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Python Twitter Clone <span class="python-badge">Flask Backend</span></h1>
        
        <div class="section">
            <h3>Post Tweet</h3>
            <input type="number" id="postUserId" placeholder="User ID" />
            <input type="number" id="tweetId" placeholder="Tweet ID" />
            <button onclick="postTweet()">Post Tweet</button>
        </div>

        <div class="section">
            <h3>Follow/Unfollow</h3>
            <input type="number" id="followerId" placeholder="Follower ID" />
            <input type="number" id="followeeId" placeholder="Followee ID" />
            <button onclick="followUser()">Follow</button>
            <button onclick="unfollowUser()">Unfollow</button>
        </div>

        <div class="section">
            <h3>News Feed</h3>
            <input type="number" id="feedUserId" placeholder="User ID" />
            <button onclick="getNewsFeed()">Get News Feed</button>
            <div id="newsfeed"></div>
        </div>
    </div>

    <script>
        function postTweet() {
            const userId = document.getElementById('postUserId').value;
            const tweetId = document.getElementById('tweetId').value;
            
            fetch(`/postTweet?userId=${userId}&tweetId=${tweetId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('Tweet posted: ' + data.message));
        }

        function followUser() {
            const followerId = document.getElementById('followerId').value;
            const followeeId = document.getElementById('followeeId').value;
            
            fetch(`/follow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('Followed: ' + data.message));
        }

        function unfollowUser() {
            const followerId = document.getElementById('followerId').value;
            const followeeId = document.getElementById('followeeId').value;
            
            fetch(`/unfollow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => alert('Unfollowed: ' + data.message));
        }

        function getNewsFeed() {
            const userId = document.getElementById('feedUserId').value;
            const startTime = performance.now();
            
            fetch(`/getNewsFeed?userId=${userId}`)
                .then(response => response.json())
                .then(data => {
                    const endTime = performance.now();
                    const responseTime = (endTime - startTime).toFixed(2);
                    
                    const feedDiv = document.getElementById('newsfeed');
                    feedDiv.innerHTML = `<h4>Latest Tweets (${responseTime}ms):</h4>`;
                    if (data.length === 0) {
                        feedDiv.innerHTML += '<p>No tweets in feed</p>';
                    } else {
                        data.forEach(tweetId => {
                            feedDiv.innerHTML += `<div class="tweet">Tweet ID: ${tweetId}</div>`;
                        });
                    }
                });
        }
    </script>
</body>
</html>
    '''

@app.route('/postTweet', methods=['POST'])
def post_tweet():
    user_id = int(request.args.get('userId', 0))
    tweet_id = int(request.args.get('tweetId', 0))
    
    twitter_app.postTweet(user_id, tweet_id)
    return jsonify({"status": "success", "message": "Tweet posted!"})

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
    return jsonify({"status": "success", "message": "Followed user!"})

@app.route('/unfollow', methods=['POST'])  
def unfollow():
    follower_id = int(request.args.get('followerId', 0))
    followee_id = int(request.args.get('followeeId', 0))
    
    twitter_app.unfollow(follower_id, followee_id)
    return jsonify({"status": "success", "message": "Unfollowed user!"})

if __name__ == '__main__':
    print("Python Flask Twitter Server starting on http://localhost:5500")
    print("Compare with C++ server at http://localhost:8080")
    try:
        # Port 5500 is generally safe and not blocked by browsers (unlike 6000)
        app.run(host='0.0.0.0', port=5500, debug=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying alternative port 5501...")
        app.run(host='0.0.0.0', port=5501, debug=False) 