\LoadClass[a4paper,12pt]{report} % Classe du document

%--------------------- Packages ------------------------

\RequirePackage[italian]{babel} %Langue du document
\RequirePackage[utf8]{inputenc} %Caractères spéciaux
\RequirePackage[section]{placeins}%Pour placement de section
\RequirePackage[T1]{fontenc} %Quelques lettres qui sont pas inclus dans UTF-8
\RequirePackage{mathtools} %Paquet pour des équations et symboles mathématiques
\RequirePackage{siunitx} %Pour écrire avec la notation scientifique (Ex.: \num{2e+9})
\RequirePackage{float} %Pour placement d'images
\RequirePackage{graphicx} %Paquet pour insérer des images
\RequirePackage[justification=centering]{caption} %Pour les légendes centralisées
\RequirePackage{subcaption}
\RequirePackage{wallpaper}
\RequirePackage{nomencl}
%\makenomenclature
\RequirePackage{fancyhdr}
%\pagestyle{fancy}
%\fancyheadoffset{1cm}
%\setlength{\headheight}{2cm}
\RequirePackage{url}
\RequirePackage[hidelinks]{hyperref}%Paquet pour insérer légendes dans des sous-figures comme Figure 1a, 1b
\RequirePackage[left=3cm,right=3cm,top=2.3cm,bottom=3.5cm]{geometry} %Configuration de la page

%-------------------- Informations sur le rapport ----------------------


\newcommand{\reportitle}[1]{\renewcommand{\reportitle}{#1}}
\newcommand{\supervisor}[1]{\renewcommand{\supervisor}{#1}}


\newcommand{\margins}{
\makenomenclature
\pagestyle{fancy}
\fancyheadoffset{1cm}
\setlength{\headheight}{1.3cm}
\lhead{\includegraphics[scale=0.15]{images/univrLogo.png}} %Affichage de l'image au top de la page
\rhead{\nouppercase{\leftmark}}
\fancyfoot[C]{\small \reportitle}

}

\newcommand{\mytitlepage}{
\begin{titlepage}

	\centering %Centraliser le contenu
	\includegraphics[width=0.7\textwidth]{images/univrLogo.png}\par\vspace{1cm} %Insertion du logo
	{\scshape\LARGE Università degli Studi di Verona \par} %Nom de l'université
	\vspace{1.5cm}%Espace de 1,5cm
	\textsc{\Large Dipartimento di informatica}\\[0.5cm]
	% Minor heading such as course title
	\textsc{\large Laurea Triennale - Informatica}\\[0.5cm]

    \rule{\linewidth}{0.2 mm} \\[0.4 cm]
	{\LARGE \bfseries \reportitle \par} \
    \rule{\linewidth}{0.2 mm} \\[1.5 cm]
	\vspace{1cm}%Espace de 3cm
    
	\begin{minipage}{0.5\textwidth} %Minipage pour faire deux colonnes
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
		
	\end{minipage}\\[4cm]
    
	\vfill
	{\large Anno accademico 2022-2023 \par} %Affichage de la date

\end{titlepage}
}

\newcommand{\toc}{
\tableofcontents
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