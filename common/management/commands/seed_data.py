import random
import uuid

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from posts.models import CommentLike, Post, PostComment, PostLike

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with test data (Users, Posts, Comments, Likes)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        users = []
        for i in range(10):
            username = f"user_{uuid.uuid4().hex[:8]}"
            email = f"{username}@example.com"
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={"is_verified": True, "full_name": f"Test User {i}"},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        self.stdout.write(f"Created/Found {len(users)} users.")

        posts = []
        for i in range(100):
            author = random.choice(users)
            post = Post.objects.create(
                author=author,
                title=f"Test Post {i} by {author.username}",
                content=f"This is a generated test content for post {i}. " * 3,
            )
            posts.append(post)

        self.stdout.write(f"Created {len(posts)} posts.")

        comments = []
        for i in range(200):
            post = random.choice(posts)
            author = random.choice(users)
            comment = PostComment.objects.create(
                post=post, author=author, content=f"Nice post! Comment number {i}."
            )
            comments.append(comment)

        self.stdout.write(f"Created {len(comments)} comments.")

        post_likes_count = 0
        for post in posts:
            likers = random.sample(users, k=random.randint(0, len(users)))
            for liker in likers:
                if liker != post.author:
                    PostLike.objects.get_or_create(author=liker, post=post)
                    post_likes_count += 1

        self.stdout.write(f"Created {post_likes_count} post likes.")

        comment_likes_count = 0
        for comment in comments:
            likers = random.sample(users, k=random.randint(0, 5))
            for liker in likers:
                if liker != comment.author:
                    CommentLike.objects.get_or_create(author=liker, comment=comment)
                    comment_likes_count += 1

        self.stdout.write(f"Created {comment_likes_count} comment likes.")
        self.stdout.write(self.style.SUCCESS("Successfully seeded database!"))
