#!/bin/bash

echo "Testing C++ Twitter API..."
echo "Server should be running on http://localhost:8080"
echo ""

# Test 1: Post some tweets
echo "1. Posting tweets..."
curl -X POST "http://localhost:8080/postTweet?userId=1&tweetId=101"
echo ""
curl -X POST "http://localhost:8080/postTweet?userId=2&tweetId=201" 
echo ""
curl -X POST "http://localhost:8080/postTweet?userId=1&tweetId=102"
echo ""

# Test 2: Follow users
echo ""
echo "2. Setting up follows..."
curl -X POST "http://localhost:8080/follow?followerId=1&followeeId=2"
echo ""

# Test 3: Get news feed
echo ""
echo "3. Getting news feed for user 1:"
curl "http://localhost:8080/getNewsFeed?userId=1"
echo ""

echo ""
echo "4. Getting news feed for user 2:"
curl "http://localhost:8080/getNewsFeed?userId=2"
echo ""

echo ""
echo "✅ API Tests complete!"
echo "🌐 Open http://localhost:8080 in your browser to use the web interface!"