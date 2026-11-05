# User-story command compatibility

`create-userstories`, `user-stories` and `stories` now run the merged [create-milestones workflow](create-milestones.md). State that the result includes native milestones and one milestone document with grouped user stories, then follow that workflow.

Do not create new UserStory issues, a UserStories View or standalone per-story documents. Preserve existing issue-based stories and Views as legacy sources; never migrate or delete them automatically. New PRDs use the canonical milestone document's structural story index and stable story IDs.
