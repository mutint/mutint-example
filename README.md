# mutint-example

The stub plugin for [MutInt](https://github.com/mutint/mutint-core) — one of everything a plugin
is likely to want, small enough to read in one sitting and copy.

From a single `apps.py` it registers a page in the sidebar's experiment section (**Example**, at
`/example/`), a panel on the experiment Overview, and a section on `/about/`. The page and the
panel render the same table: each sample's mutations, and how many of them another sample
carries.

**It is installed in no assembled project, on purpose.** It exists to be copied — start from
working code rather than a skeleton — so it is deliberately absent from every `.gitmodules`.

Its tests run from mutint-core with a settings module that adds the app; the command is in
`CLAUDE.md`.

## Using it

Copy the directory, rename `mutint_example` to your app, and delete what you do not need. No
changes to mutint-core are required for a new plugin.

MIT licensed. See [mutint-core](https://github.com/mutint/mutint-core) for the platform.
