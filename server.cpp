#include "httplib.h"
#include <iostream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <tuple>
#include <sstream>
#include <string>

class twitter{
private:
    int time;
    std::unordered_map<int, std::unordered_set<int>> followers;
    std::unordered_map<int, std::unordered_set<int>> following;
    std::unordered_map<int, std::vector<std::pair<int, int>>> tweets;  // user -> list of (time, tweetId)

public:
    // constructor
    twitter() : time(0) {
        // member variables are declared above and initialized here
    }

    void postTweet(int userId, int tweetId) {
        if (tweets.find(userId) == tweets.end()) {
            tweets[userId] = {};
        }
        if (following.find(userId) == following.end()) {
            following[userId] = {};
        }

        time++;
        tweets[userId].push_back({time, tweetId});
    }

    std::vector<int> getNewsFeed(int userId) {
        if (following.find(userId) == following.end()) {
            following[userId] = {};
        }
        if (tweets.find(userId) == tweets.end()) {
            tweets[userId] = {};
        }

        std::unordered_set<int> followees = following[userId];
        followees.insert(userId);

        using T = std::tuple<int, int, int, int>;  // time, tweetId, authorId, index
        std::priority_queue<T> heap;

        for (int uid : followees) {
            if (tweets.find(uid) == tweets.end()) {
                tweets[uid] = {};
            }
            if (following.find(uid) == following.end()) {
                following[uid] = {};
            }

            auto& tlist = tweets[uid];
            if (!tlist.empty()) {
                int idx = tlist.size() - 1;
                auto [t, tid] = tlist[idx];
                heap.push({t, tid, uid, idx});
            }
        }

        std::vector<int> res;
        while (!heap.empty() && res.size() < 10) {
            auto [t, tid, uid, idx] = heap.top();
            heap.pop();
            res.push_back(tid);

            idx--;
            if (idx >= 0) {
                auto [t2, tid2] = tweets[uid][idx];
                heap.push({t2, tid2, uid, idx});
            }
        }

        return res;
    }

    void follow(int followerId, int followeeId) {
        if (followerId == followeeId) return;
        if (following.find(followerId) == following.end()) {
            following[followerId] = {};
        }
        if (tweets.find(followerId) == tweets.end()) {
            tweets[followerId] = {};
        }
        if (following.find(followeeId) == following.end()) {
            following[followeeId] = {};
        }
        if (tweets.find(followeeId) == tweets.end()) {
            tweets[followeeId] = {};
        }

        following[followerId].insert(followeeId);
    }

    void unfollow(int followerId, int followeeId) {
        if (followerId == followeeId) return;
        if (following.find(followerId) == following.end()) {
            following[followerId] = {};
        }
        // if not following, erase does nothing
        following[followerId].erase(followeeId);
    }
};

// Global Twitter instance
twitter twitterApp;

// Helper function to convert vector<int> to JSON-like string
std::string vectorToJson(const std::vector<int>& vec) {
    std::stringstream ss;
    ss << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        if (i > 0) ss << ",";
        ss << vec[i];
    }
    ss << "]";
    return ss.str();
}

// Helper function to extract parameter from request
int getParam(const httplib::Request& req, const std::string& key, int defaultValue = 0) {
    auto it = req.params.find(key);
    if (it != req.params.end()) {
        return std::stoi(it->second);
    }
    return defaultValue;
}

int main() {
    httplib::Server svr;

    // Serve static HTML page at root
    svr.Get("/", [](const httplib::Request&, httplib::Response& res) {
        std::string html = 
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        "<title>Twitter Clone C++</title>"
        "<style>"
        "body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }"
        ".section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }"
        "input, button { margin: 5px; padding: 8px; }"
        "button { background: #1da1f2; color: white; border: none; cursor: pointer; border-radius: 3px; }"
        "button:hover { background: #0d95e8; }"
        "#newsfeed { background: #f5f8fa; }"
        ".tweet { background: white; margin: 10px 0; padding: 10px; border-radius: 5px; border: 1px solid #e1e8ed; }"
        "</style>"
        "</head>"
        "<body>"
        "<h1>Twitter Clone (C++ Backend)</h1>"
        "<div class=\"section\">"
        "<h3>Post Tweet</h3>"
        "<input type=\"number\" id=\"postUserId\" placeholder=\"User ID\" />"
        "<input type=\"number\" id=\"tweetId\" placeholder=\"Tweet ID\" />"
        "<button onclick=\"postTweet()\">Post Tweet</button>"
        "</div>"
        "<div class=\"section\">"
        "<h3>Follow/Unfollow</h3>"
        "<input type=\"number\" id=\"followerId\" placeholder=\"Follower ID\" />"
        "<input type=\"number\" id=\"followeeId\" placeholder=\"Followee ID\" />"
        "<button onclick=\"followUser()\">Follow</button>"
        "<button onclick=\"unfollowUser()\">Unfollow</button>"
        "</div>"
        "<div class=\"section\">"
        "<h3>News Feed</h3>"
        "<input type=\"number\" id=\"feedUserId\" placeholder=\"User ID\" />"
        "<button onclick=\"getNewsFeed()\">Get News Feed</button>"
        "<div id=\"newsfeed\"></div>"
        "</div>"
        "<script>"
        "function postTweet() {"
        "const userId = document.getElementById('postUserId').value;"
        "const tweetId = document.getElementById('tweetId').value;"
        "fetch(`/postTweet?userId=${userId}&tweetId=${tweetId}`, {method: 'POST'})"
        ".then(response => response.text())"
        ".then(data => alert('Tweet posted: ' + data));"
        "}"
        "function followUser() {"
        "const followerId = document.getElementById('followerId').value;"
        "const followeeId = document.getElementById('followeeId').value;"
        "fetch(`/follow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})"
        ".then(response => response.text())"
        ".then(data => alert('Followed: ' + data));"
        "}"
        "function unfollowUser() {"
        "const followerId = document.getElementById('followerId').value;"
        "const followeeId = document.getElementById('followeeId').value;"
        "fetch(`/unfollow?followerId=${followerId}&followeeId=${followeeId}`, {method: 'POST'})"
        ".then(response => response.text())"
        ".then(data => alert('Unfollowed: ' + data));"
        "}"
        "function getNewsFeed() {"
        "const userId = document.getElementById('feedUserId').value;"
        "fetch(`/getNewsFeed?userId=${userId}`)"
        ".then(response => response.json())"
        ".then(data => {"
        "const feedDiv = document.getElementById('newsfeed');"
        "feedDiv.innerHTML = '<h4>Latest Tweets:</h4>';"
        "if (data.length === 0) {"
        "feedDiv.innerHTML += '<p>No tweets in feed</p>';"
        "} else {"
        "data.forEach(tweetId => {"
        "feedDiv.innerHTML += `<div class=\"tweet\">Tweet ID: ${tweetId}</div>`;"
        "});"
        "}"
        "});"
        "}"
        "</script>"
        "</body>"
        "</html>";
        res.set_content(html, "text/html");
    });

    // API Endpoints
    svr.Post("/postTweet", [](const httplib::Request& req, httplib::Response& res) {
        int userId = getParam(req, "userId");
        int tweetId = getParam(req, "tweetId");
        
        twitterApp.postTweet(userId, tweetId);
        res.set_content("{\"status\":\"success\",\"message\":\"Tweet posted\"}", "application/json");
    });

    svr.Get("/getNewsFeed", [](const httplib::Request& req, httplib::Response& res) {
        int userId = getParam(req, "userId");
        
        auto feed = twitterApp.getNewsFeed(userId);
        res.set_content(vectorToJson(feed), "application/json");
    });

    svr.Post("/follow", [](const httplib::Request& req, httplib::Response& res) {
        int followerId = getParam(req, "followerId");
        int followeeId = getParam(req, "followeeId");
        
        twitterApp.follow(followerId, followeeId);
        res.set_content("{\"status\":\"success\",\"message\":\"Followed user\"}", "application/json");
    });

    svr.Post("/unfollow", [](const httplib::Request& req, httplib::Response& res) {
        int followerId = getParam(req, "followerId");
        int followeeId = getParam(req, "followeeId");
        
        twitterApp.unfollow(followerId, followeeId);
        res.set_content("{\"status\":\"success\",\"message\":\"Unfollowed user\"}", "application/json");
    });

    std::cout << "🚀 C++ Twitter Server starting on http://localhost:8080" << std::endl;
    svr.listen("localhost", 8080);

    return 0;
}