# Resume Build Instructions
Resume source files, in XeTeX, version-controlled 😎. Will be updated as new skills and experience are acquired.


## Getting Started
It's important to note that the resume is generated using the XeTeX engine. The [Arch repo](https://wiki.archlinux.org/title/TeX_Live) provides a good rundown of the Tex typesetting system.

## Installation
### Dependencies
- [TexLive](https://tug.org/texlive/) (or any other XeTeX-compatible utility) for generating output
- Fonts
     - [Raleway](https://fonts.google.com/specimen/Raleway)
     - [Lato](https://fonts.google.com/specimen/Lato)
     - [FiraCode Nerd Font](https://www.nerdfonts.com/font-downloads)

### TexLive
<!-- TODO: Include setup guides for other OSes -->
For general installation instructions of TexLive, see the [docs](https://tug.org/texlive/).

#### Linux
```sh
# Arch Linux (See AUR: https://archlinux.org/groups/x86_64/texlive)
paru -S texlive-basic texlive-latex texlive-xetex texlive-luatex texlive-latexextra texlive-latexrecommended texlive-bibtexextra texlive-binextra texlive-context texlive-fontsextra texlive-fontsrecommended texlive-fontutils texlive-pictures
```

### Fonts
To keep the repo lightweight, the fonts will not be hosted in the repo. Download the [required](#dependencies) fonts, and extract them to the [fonts](./fonts/) directory.

## Compiling
### Linux
```sh
# Produces resume.pdf in the specified directory
dirName=build; fileName=resume;
xelatex --output-directory ${dirName} ${fileName}.xetex \
&& cp ${dirName}/${fileName}.pdf . \
&& unset dirName fileName
```
