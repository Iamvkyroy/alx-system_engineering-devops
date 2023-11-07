import praw

# Create a Reddit instance
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='YOUR_USER_AGENT')

def count_words(subreddit, word_list, posts=None, word_counts=None):
    if posts is None:
        # Initialize posts and word_counts on the first call
        posts = []
        word_counts = {}

    if len(word_list) == 0:
        # All keywords have been counted, so print the results
        sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word.lower()}: {count}")
        return

    keyword = word_list[0].lower()

    if keyword in word_counts:
        # Skip keywords that have already been counted
        count_words(subreddit, word_list[1:], posts, word_counts)
        return

    if subreddit not in posts:
        try:
            # Fetch the hot articles from the subreddit
            subreddit_obj = reddit.subreddit(subreddit)
            for submission in subreddit_obj.hot(limit=25):
                posts.append(submission.title)
        except Exception as e:
            print(f"Error: {e}")
            return

    # Count the occurrences of the keyword in post titles
    count = sum(1 for post in posts if f" {keyword} " in post.lower())
    word_counts[keyword] = count

    count_words(subreddit, word_list[1:], posts, word_counts)

# Example usage:
subreddit = 'learnprogramming'
word_list = ['Python', 'JavaScript', 'java']
count_words(subreddit, word_list)

