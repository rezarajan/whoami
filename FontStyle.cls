% Intro Options
\ProvidesClass{resume-openfont}[2014/04/30 CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=1.5cm, vmargin=0.7cm]{geometry}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{babel}
\usepackage[UKenglish]{isodate}
\usepackage{fontspec,xltxtra,xunicode}
\usepackage{pgffor}
\usepackage{tikz}
\usetikzlibrary{shapes.misc}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     CUSTOM FUNCTIONS
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Define a command that takes a list of arguments and formats them with \textbullet separator, on a single line
\newcommand{\formattedlist}[1]{%
    \foreach \item [count=\i] in {#1}{%
	\ifnum\i=1
	  \item~
	\else
	  {\textbullet}~{\item}~
	\fi
    }%
}

% A list with different (unindented) formatting compared to `itemize`
\newcommand{\straightlist}[1]{%
    \foreach \item [count=\i] in {#1}{%
    	\textbullet~\item\\
    }%
}
% A list with a formatted box (tags)
\newcommand{\boxedlist}[1]{%
    \vspace{3pt}
    \foreach \item in {#1}{%
        \boxeditem{\item}
    }%
}
% A counter to check for the last item in the list
%\newcounter{listLength}
%\newcommand{\countlistlength}[1]{%
  %\setcounter{listLength}{0}
  %\foreach \item in {#1} {%
    %\stepcounter{listLength}
  %}
%}
% See example usage below:
%\newcommand{\straightlist}[1]{%
    %\begin{minipage}{\linewidth}
    %\countlistlength{#1} % Count the list length into the listLength counter
    %\def\listLen{\value{listLength}} % Create the value listLen based on listLength
    %\foreach \item [count=\i] in {#1}{%
    	%\ifnum\i<\listLen % Compute some logic against the value of listLen
		%\\%Do something
	%\fi
    %}
    %\end{minipage}%
%}

% Color definitions
\definecolor{date}{HTML}{666666} 
\definecolor{primary}{HTML}{2b2b2b} 
\definecolor{headings}{HTML}{6A6A6A}
\definecolor{subheadings}{HTML}{333333}
\definecolor{mygray}{gray}{0.9}
\definecolor{tagbg}{HTML}{5A5A5A} % New fill color for the box

% Set main fonts
\defaultfontfeatures{Mapping=tex-text}
\setmainfont[Color=primary, Path = fonts/lato/, ItalicFont = Lato-LigIta]{Lato-Lig}
\setsansfont[Scale=MatchLowercase,Mapping=tex-text, Path = fonts/raleway/]{Raleway-ExtraLight}
\newcommand{\custombold}[1]{\color{subheadings}\fontspec[Path = fonts/lato/]{Lato-Reg}\selectfont #1 \normalfont}
\newcommand{\nerdfont}[1]{\fontspec[Path=fonts/firacode/]{FiraCodeNerdFont-Regular}\selectfont #1 \kern-0.15em \normalfont}

% Date command
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{5mm} % start everyth
\newcommand{\lastupdated}{\begin{textblock}{60}(165,0)
\color{date}\fontspec[Path = fonts/raleway/]{Raleway-ExtraLight}\fontsize{8pt}{10pt}\selectfont 
Last Updated on
\today
\end{textblock}}


% Name command
\newcommand{\namesection}[3]{\color{black}
	\centering{
		\sffamily
		\fontspec[Path = fonts/lato/]{Lato-Hai}\fontsize{32pt}{1em}\selectfont #1 
		\fontspec[Path = fonts/lato/]{Lato-Lig}\selectfont #2
	} \\
	\vspace{5pt}
	\centering{ \color{headings}\fontspec[Path = fonts/raleway/]{Raleway-Light}\fontsize{11pt}{14pt}\selectfont #3}
	\noindent\makebox[\linewidth]{\color{mygray}\rule{\paperwidth}{0.4pt}}
	\vspace{-15pt}
}
\titlespacing{\section}{0pt}{0pt}{0pt}

% Headings command
\titleformat{\section}{\color{headings}
\scshape\fontspec[Path = fonts/lato/]{Lato-Lig}\fontsize{16pt}{19pt}\selectfont \raggedright\uppercase}{} {0em}{}

% Subeadings command
\titleformat{\subsection}{\color{subheadings}
\fontspec[Path = fonts/lato/]{Lato-Bol}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase}{}{0em}{}
\titlespacing{\subsection}{0pt}{\parskip}{-\parskip}
\titlespacing{\subsubsection}{0pt}{\parskip}{-\parskip}
\newcommand{\runsubsection}[1]{%
    \color{subheadings}%
    \fontspec[Path = fonts/lato/]{Lato-Bol}%
    \fontsize{12pt}{12pt}%
    \selectfont\bfseries\uppercase {#1} \normalfont%
}

% Descriptors command
\newcommand{\descript}[1]{%
	\color{subheadings}%
	\raggedright%
	\scshape%
	\fontspec[Path = fonts/raleway/]{Raleway-Medium}%
	\fontsize{11pt}{13pt}%
	\selectfont {#1 \\} %
	\normalfont%
}

% Location command
\newcommand{\location}[1]{%
    \noindent\color{headings}%
    \raggedright%
    \fontspec[Path = fonts/raleway/]{Raleway-Medium}%
    \fontsize{10pt}{12pt}%
    \selectfont%
    #1%
    \par%
    \normalfont%
}

% Section seperators command
\newcommand{\sectionsep}[0]{\vspace{8pt}}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}

% Formatted Boxes (tags) command
\newcommand{\boxeditem}[1]{%
  \tikz[baseline=(X.base)] \node[rectangle, rounded corners, inner sep=4pt, fill=tagbg, text depth=2pt] (X) {\custombold{\textcolor{white}{#1}}};%
}

