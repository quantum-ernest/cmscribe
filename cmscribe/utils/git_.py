from git import Repo, InvalidGitRepositoryError

try:
    repo = Repo(".", search_parent_directories=True)
except InvalidGitRepositoryError:
    print("No git repository found. Please run `git init` first.")


def get_staged_files():
    diffs = repo.index.diff(repo.head.commit)
    return [diff.a_path for diff in diffs]


def get_repo_name():
    """Get the name of the repository."""
    return repo.working_tree_dir.split("/")[-1]


def get_staged_content():
    return repo.git.diff("--staged")


def get_file_content_before_after(staged_files):
    """Get content of staged files before (HEAD) and after (staged)."""
    content = {}
    for file_path in staged_files:
        try:
            blob_before = repo.head.commit.tree[file_path]
            content_before = blob_before.data_stream.read().decode("utf-8")
        except KeyError:
            content_before = "<new file, no prior content>"
        try:
            blob_after = repo.index.entries[(file_path, 0)].to_blob(repo)
            content_after = blob_after.data_stream.read().decode("utf-8")
        except KeyError:
            with open(file_path, "r", encoding="utf-8") as f:
                content_after = f.read()
        except IndexError:
            content_after = "<file deleted>"

        content[file_path] = {"before": content_before, "after": content_after}
    return content
