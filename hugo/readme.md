# Building
This resume utilizes the [resume-a4](https://gitlab.com/mertbakir/resume-a4) hugo theme. It's goal is simplicity and precision.

```sh
# Pulls the submodule
git submodule update --init --recursive
```

The resume will be generated as a static site. To export as a PDF, simply print the site and the overrides will ensure that it saves as a PDF - links in-tact and all.

# Editing
The layout can be altered in [hugo.toml](./hugo.toml), and the content can be modified via yaml files in the [data](./data) directory.
