# mwbackup

A python backup script for backing up MediaWiki installations. Uses APIs for upload and download, so works best when you do not have access to the database.

## Usage

1. Configure by setting the `url` value in `backup.py` and then run it. If your wiki isn't in the root directory, simply change the value of `path` on line 10 from `/` to whatever.
2. Run `backup.py`.
3. Create an account for the script, or you can use your own. (Not recommended on public boards, unless it's your own)
4. Configure by setting the `url`, `username` and `password` value in `upload.py`. If your wiki isn't in the root directory, simply change the value of `path` on line 15 from `/` to whatever.
5. Run `upload.py`.
6. You're done!

## Limitations

* Cannot backup file history. (File info text is stored since that is considered a 'page' like any other wiki page)
