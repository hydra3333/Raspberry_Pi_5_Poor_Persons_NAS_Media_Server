@ECHO ON
@setlocal ENABLEDELAYEDEXPANSION
@setlocal enableextensions

call :do_replicate_to_target "X:\ROOTFOLDER1"
call :do_replicate_to_target "V:\ROOTFOLDER2"
call :do_replicate_to_target "F:\ROOTFOLDER3"
call :do_replicate_to_target "H:\ROOTFOLDER4"
call :do_replicate_to_target "K:\ROOTFOLDER5"
call :do_replicate_to_target "W:\ROOTFOLDER6"

pause
goto :eof

:do_replicate_to_target
echo.
mkdir "%~1"
echo.
pause
IF /I "%~1" NEQ "X:\ROOTFOLDER1" (
   echo ***** xcopy "X:\ROOTFOLDER1" "%~1" /T /E /Y /F
   xcopy "X:\ROOTFOLDER1" "%~1" /T /E /Y /F
)
IF /I "%~1" NEQ "V:\ROOTFOLDER2" (
   echo ***** xcopy "V:\ROOTFOLDER2" "%~1" /T /E /Y /F
   xcopy "V:\ROOTFOLDER2" "%~1" /T /E /Y /F
)
IF /I "%~1" NEQ "F:\ROOTFOLDER3" (
   echo ***** xcopy "F:\ROOTFOLDER3" "%~1" /T /E /Y /F
   xcopy "F:\ROOTFOLDER3" "%~1" /T /E /Y /F
)
IF /I "%~1" NEQ "H:\ROOTFOLDER4" (
   echo ***** xcopy "H:\ROOTFOLDER4" "%~1" /T /E /Y /F
   xcopy "H:\ROOTFOLDER4" "%~1" /T /E /Y /F
)
IF /I "%~1" NEQ "K:\ROOTFOLDER5" (
   echo ***** xcopy "K:\ROOTFOLDER5" "%~1" /T /E /Y /F
   xcopy "K:\ROOTFOLDER5" "%~1" /T /E /Y /F
)
IF /I "%~1" NEQ "W:\ROOTFOLDER6" (
   echo ***** xcopy "W:\ROOTFOLDER6" "%~1" /T /E /Y /F
   xcopy "W:\ROOTFOLDER6" "%~1" /T /E /Y /F
)
REM   /T           Creates directory structure, but does not copy files. Does not
REM                include empty directories or subdirectories. /T /E includes
REM   /E           Copies directories and subdirectories, including empty ones.
REM                Same as /S /E. May be used to modify /T.
echo.
goto :eof


XCOPY source [destination] [/A | /M] [/D[:date]] [/P] [/S [/E]] [/V] [/W]
                           [/C] [/I] [/-I] [/Q] [/F] [/L] [/G] [/H] [/R] [/T]
                           [/U] [/K] [/N] [/O] [/X] [/Y] [/-Y] [/Z] [/B] [/J]
                           [/EXCLUDE:file1[+file2][+file3]...] [/COMPRESS]

  source       Specifies the file(s) to copy.
  destination  Specifies the location and/or name of new files.
  /A           Copies only files with the archive attribute set,
               doesn't change the attribute.
  /M           Copies only files with the archive attribute set,
               turns off the archive attribute.
  /D:m-d-y     Copies files changed on or after the specified date.
               If no date is given, copies only those files whose
               source time is newer than the destination time.
  /EXCLUDE:file1[+file2][+file3]...
               Specifies a list of files containing strings.  Each string
               should be in a separate line in the files.  When any of the
               strings match any part of the absolute path of the file to be
               copied, that file will be excluded from being copied.  For
               example, specifying a string like \obj\ or .obj will exclude
               all files underneath the directory obj or all files with the
               .obj extension respectively.
  /P           Prompts you before creating each destination file.
  /S           Copies directories and subdirectories except empty ones.
  /E           Copies directories and subdirectories, including empty ones.
               Same as /S /E. May be used to modify /T.
  /V           Verifies the size of each new file.
  /W           Prompts you to press a key before copying.
  /C           Continues copying even if errors occur.
  /I           If destination does not exist and copying more than one file,
               assumes that destination must be a directory.
  /-I          If destination does not exist and copying a single specified file,
               assumes that destination must be a file.
  /Q           Does not display file names while copying.
  /F           Displays full source and destination file names while copying.
  /L           Displays files that would be copied.
  /G           Allows the copying of encrypted files to destination that does
               not support encryption.
  /H           Copies hidden and system files also.
  /R           Overwrites read-only files.
  /T           Creates directory structure, but does not copy files. Does not
               include empty directories or subdirectories. /T /E includes
               empty directories and subdirectories.
  /U           Copies only files that already exist in destination.
  /K           Copies attributes. Normal Xcopy will reset read-only attributes.
  /N           Copies using the generated short names.
  /O           Copies file ownership and ACL information.
  /X           Copies file audit settings (implies /O).
  /Y           Suppresses prompting to confirm you want to overwrite an
               existing destination file.
  /-Y          Causes prompting to confirm you want to overwrite an
               existing destination file.
  /Z           Copies networked files in restartable mode.
  /B           Copies the Symbolic Link itself versus the target of the link.
  /J           Copies using unbuffered I/O. Recommended for very large files.
  /COMPRESS    Request network compression during file transfer where
               applicable.
  /SPARSE      Preserves the sparse state when copying a sparse file.

The switch /Y may be preset in the COPYCMD environment variable.
This may be overridden with /-Y on the command line.