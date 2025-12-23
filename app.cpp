#include <iostream>
#include <stdlib.h>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <tuple>


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

    /*
    // original wrong implementation commented out
    twitter(){
        int time = 0;
        
        // if in python we use a set and list should we use std list and vector?? in cpp i mean
        
        // or maybe dictionary or hashmap

        // can u do something liek this ie hashmap of user id to the set/list of followers
        std::unordered_set<double, std::string> followers;
        // didn't know we had to include unordered set on its own to use it but ok

        

        

    }
    */

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




int main(){



    std::cout << "whatever";

    return 0;
}





/*




general question:
how to break down and remember what is in private and public and how to figure out
what is in scope and not in scope

in a simple class with public and private what has to be public??
the non negotiable thigns?









*/