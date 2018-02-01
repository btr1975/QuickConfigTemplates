; QuickConfigTemplates Installer Buld NSIS
; Version: 1.0.0

;--------------------------------

; The name of the installer
Name "QuickConfigTemplates Version 1.0.9"

; The file to write
OutFile "QuickConfigTemplates.exe"

; The default installation directory
InstallDir C:\Users\Ben\Desktop\QuickConfigTemplates

; Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /nonfatal /a /r "C:\Users\Ben\Desktop\GitRepos\dist\QuickConfigTemplates-v1-0-9\"

SectionEnd ; end the section

