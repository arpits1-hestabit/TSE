# MERGE POSTMORTEM

## Explanation
In this merge, we had two clones of the repository making changes to the same file, `readme.md`. The first clone made a modification on line 1, and the second clone made a different modification to the same line. This resulted in a **merge conflict**.
- Snapshot(merge conflict):
    ![new merge conflict](<../Attachments/image copy 6.png>)


I resolved the conflict by comparing both conflicts and keeping both changes, as both modifications were necessary for the file's intended purpose. The conflict was manually resolved by merging both changes into the file.
- Snapshot(Comparing conflict):
    ![compare conflict](<../Attachments/image copy 7.png>)

- Snapshot(Accepting both changes):
    ![accepting both changes](<../Attachments/image copy 8.png>)


After resolving the conflict, a merge commit was created and pushed to the remote repository.

## Commit graph
Below is a screenshot of the **commit graph** showing the branches and the merge:
    ![commit graph](<../Attachments/image copy 9.png>)
