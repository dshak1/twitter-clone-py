class twitter:
    def __init__(self):
        self.time = 0
        self.followers = {}
        self.following = {}

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
            _, tid, uid, idx = heapq.heappop(heap) # bro wtf u can name a variable _? is that some sort of general naming convention like th dunder init?
            
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





# so basically time in this file is not like an actual internal clock or anything like that but rather just a count to enumerate the tweets so then we can sort them by taking the max time
# since it only goes up (monotonic increas.) this means taking the top 10 tweets with max times is taking the 10 most recent
# its not realistic but it works for this problem at this mini scale right
    



























# '''
# questions to consider :


# why or why not and when and when not to create a user class







# '''