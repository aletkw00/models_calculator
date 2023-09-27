\LoadClass[a4paper,12pt]{report} 

%--------------------- Packages ------------------------

\RequirePackage[italian]{babel} 
\RequirePackage[utf8]{inputenc} 
\RequirePackage[section]{placeins}
\RequirePackage[T1]{fontenc}
\RequirePackage{mathtools}
\RequirePackage{siunitx}
\RequirePackage{float}
\RequirePackage{graphicx} 
\RequirePackage[justification=centering]{caption} 
\RequirePackage{subcaption}
\RequirePackage{wallpaper}
\RequirePackage{nomencl}
\RequirePackage{fancyhdr}

\RequirePackage{url}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[left=3cm,right=3cm,top=2.3cm,bottom=3.5cm]{geometry} 

%-------------------- Informations sur le rapport ----------------------


\newcommand{\reportitle}[1]{\renewcommand{\reportitle}{#1}}
\newcommand{\supervisor}[1]{\renewcommand{\supervisor}{#1}}


\newcommand{\margins}{
\makenomenclature
\pagestyle{fancy}
\fancyheadoffset{1cm}
\setlength{\headheight}{1.3cm}

\rhead{\nouppercase{\leftmark}}


}

\newcommand{\mytitlepage}{
\begin{titlepage}

	\centering 
	{\scshape\LARGE Università degli Studi di Verona \par} 
	\vspace{1.5cm}
	\textsc{\Large Dipartimento di informatica}\\[0.5cm]
	\textsc{\large Laurea Triennale - Informatica}\\[0.5cm]

    \rule{\linewidth}{0.35 mm} \\[0.4 cm]
	{\huge \bfseries \reportitle \par} \
    \rule{\linewidth}{0.35 mm} \\[1.5 cm]
	\vspace{1cm}
    
	\begin{minipage}{0.5\textwidth} 
		\begin{flushleft}
			\large
			\textit{Autore:}\\
			Alessio \textsc{Bonizzato}\\
			\textit{Matricola:}\\
			VR446437
		\end{flushleft}
	\end{minipage}
	~
	\begin{minipage}{0.4\textwidth}
		\begin{flushright}
			\large
			\textit{Relatore:}\\
			Davide \textsc{Quaglia}\\
			\textit{Co-Relatore:}\\
			Elia \textsc{Brentarolli}
		\end{flushright}
		
	\end{minipage}
    
	\vfill\vfill\vfill
	{\large Anno accademico 2022-2023 \par} 

\end{titlepage}
}

\newcommand{\toc}{
\tableofcontents
\newpage
}

\newcommand{\fig}{
\listoffigures
\listoftables
\newpage
}

\newcommand{\insertfigure}[4]{
\begin{figure}[ht]
\centering
\includegraphics[height=#2]{#1}
\caption{#3}
\label{fig: #4}
\end{figure}
}