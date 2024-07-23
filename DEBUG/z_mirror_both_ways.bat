@ECHO OFF
@setlocal ENABLEDELAYEDEXPANSION
@setlocal enableextensions

set "D1=X:\ROOTFOLDER1"
set "D2=V:\ROOTFOLDER2"
set "D3=F:\ROOTFOLDER3"
set "D4=H:\ROOTFOLDER4"
set "D5=K:\ROOTFOLDER5"

set "M01=\2015.11.29-Jess-21st-birthday-party"
set "M02=\BigIdeas"
set "M03=\CharlieWalsh"
set "M04=\ClassicDocumentaries"
set "M05=\ClassicMovies"
set "M06=\Documentaries"
set "M07=\Footy"
set "M08=\HomePics"
set "M09=\Movies"
set "M10=\Movies_unsorted"
set "M11=\Music"
set "M12=\MusicVideos"
set "M13=\OldMovies"
set "M14=\SciFi"
set "M15=\Series"

call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""
call do_robo "" ""

pause
exit

:do_robo
REM *** WARNING: WARNING: WARNING: WARNING: WARNING: 
REM
REM /MIR means MIRRORING which DELETES files in the destination which are not in the source
REM
REM *** WARNING: WARNING: WARNING: WARNING: WARNING: 
REM
REM
set RoboSwitches=/MIR /IT /COPY:DAT /DCOPY:DAT /XJD /XJF /E /Z /J /TIMFIX /TS /R:10 /W:2 /XO /FP /NDL /ETA /TEE 
REM
REM The combination of these switches should help to ensure that files with 
REM the same size but different timestamps are updated without copying the entire file
REM while also handling mirroring operations.
REM
REM Since we use /XO (exclude older files) we must mirror both ways ...
REM
set "src=%~1"
set "dst=%~2"
echo about to: robocopy "%src%" "%dst%" %RoboSwitches%
pause
robocopy "%src%" "%dst%" %RoboSwitches%
pause
echo about to: robocopy "%dst%" "%src%" %RoboSwitches%
pause
robocopy "%dst%" "%src%" %RoboSwitches%
pause
goto :eof




-------------------------------------------------------------------------------
   ROBOCOPY     ::     Robust File Copy for Windows
-------------------------------------------------------------------------------

  Started : Saturday, 20 July 2024 2:21:04 PM
              Usage :: ROBOCOPY source destination [file [file]...] [options]

             source :: Source Directory (drive:\path or \\server\share\path).
        destination :: Destination Dir  (drive:\path or \\server\share\path).
               file :: File(s) to copy  (names/wildcards: default is "*.*").

::
:: Copy options :
::
                 /S :: copy Subdirectories, but not empty ones.
                 /E :: copy subdirectories, including Empty ones.
             /LEV:n :: only copy the top n LEVels of the source directory tree.

                 /Z :: copy files in restartable mode.
                 /B :: copy files in Backup mode.
                /ZB :: use restartable mode; if access denied use Backup mode.
                 /J :: copy using unbuffered I/O (recommended for large files).
            /EFSRAW :: copy all encrypted files in EFS RAW mode.

  /COPY:copyflag[s] :: what to COPY for files (default is /COPY:DAT).
                       (copyflags : D=Data, A=Attributes, T=Timestamps, X=Skip alt data streams (X ignored if /B or /ZB).
                       (S=Security=NTFS ACLs, O=Owner info, U=aUditing info).


               /SEC :: copy files with SECurity (equivalent to /COPY:DATS).
           /COPYALL :: COPY ALL file info (equivalent to /COPY:DATSOU).
            /NOCOPY :: COPY NO file info (useful with /PURGE).
            /SECFIX :: FIX file SECurity on all files, even skipped files.
            /TIMFIX :: FIX file TIMes on all files, even skipped files.

             /PURGE :: delete dest files/dirs that no longer exist in source.
               /MIR :: MIRror a directory tree (equivalent to /E plus /PURGE).

               /MOV :: MOVe files (delete from source after copying).
              /MOVE :: MOVE files AND dirs (delete from source after copying).

     /A+:[RASHCNET] :: add the given Attributes to copied files.
     /A-:[RASHCNETO]:: remove the given Attributes from copied files.

            /CREATE :: CREATE directory tree and zero-length files only.
               /FAT :: create destination files using 8.3 FAT file names only.
               /256 :: turn off very long path (> 256 characters) support.

             /MON:n :: MONitor source; run again when more than n changes seen.
             /MOT:m :: MOnitor source; run again in m minutes Time, if changed.

      /RH:hhmm-hhmm :: Run Hours - times when new copies may be started.
                /PF :: check run hours on a Per File (not per pass) basis.

             /IPG:n :: Inter-Packet Gap (ms), to free bandwidth on slow lines.

                /SJ :: copy Junctions as junctions instead of as the junction targets.
                /SL :: copy Symbolic Links as links instead of as the link targets.

            /MT[:n] :: Do multi-threaded copies with n threads (default 8).
                       n must be at least 1 and not greater than 128.
                       This option is incompatible with the /IPG and /EFSRAW options.
                       Redirect output using /LOG option for better performance.

 /DCOPY:copyflag[s] :: what to COPY for directories (default is /DCOPY:DA).
                       (copyflags : D=Data, A=Attributes, T=Timestamps, E=EAs, X=Skip alt data streams).

           /NODCOPY :: COPY NO directory info (by default /DCOPY:DA is done).

         /NOOFFLOAD :: copy files without using the Windows Copy Offload mechanism.

          /COMPRESS :: Request network compression during file transfer, if applicable.

            /SPARSE :: Enable retaining sparse state during copy
::
:: Copy File Throttling Options :
::
  /IoMaxSize:n[KMG] :: Requested max i/o size per {read,write} cycle, in n [KMG] bytes.

     /IoRate:n[KMG] :: Requested i/o rate, in n [KMG] bytes per second.

  /Threshold:n[KMG] :: File size threshold for throttling, in n [KMG] bytes (see Remarks).

::
:: File Selection Options :
::
                 /A :: copy only files with the Archive attribute set.
                 /M :: copy only files with the Archive attribute and reset it.
    /IA:[RASHCNETO] :: Include only files with any of the given Attributes set.
    /XA:[RASHCNETO] :: eXclude files with any of the given Attributes set.

 /XF file [file]... :: eXclude Files matching given names/paths/wildcards.
 /XD dirs [dirs]... :: eXclude Directories matching given names/paths.

                /XC :: eXclude Changed files.
                /XN :: eXclude Newer files.
                /XO :: eXclude Older files.
                /XX :: eXclude eXtra files and directories.
                /XL :: eXclude Lonely files and directories.
                /IS :: Include Same files.
                /IT :: Include Tweaked files.

             /MAX:n :: MAXimum file size - exclude files bigger than n bytes.
             /MIN:n :: MINimum file size - exclude files smaller than n bytes.

          /MAXAGE:n :: MAXimum file AGE - exclude files older than n days/date.
          /MINAGE:n :: MINimum file AGE - exclude files newer than n days/date.
          /MAXLAD:n :: MAXimum Last Access Date - exclude files unused since n.
          /MINLAD:n :: MINimum Last Access Date - exclude files used since n.
                       (If n < 1900 then n = n days, else n = YYYYMMDD date).

               /FFT :: assume FAT File Times (2-second granularity).
               /DST :: compensate for one-hour DST time differences.

                /XJ :: eXclude symbolic links (for both files and directories) and Junction points.
               /XJD :: eXclude symbolic links for Directories and Junction points.
               /XJF :: eXclude symbolic links for Files.

                /IM :: Include Modified files (differing change times).
::
:: Retry Options :
::
               /R:n :: number of Retries on failed copies: default 1 million.
               /W:n :: Wait time between retries: default is 30 seconds.

               /REG :: Save /R:n and /W:n in the Registry as default settings.

               /TBD :: Wait for sharenames To Be Defined (retry error 67).

               /LFSM :: Operate in low free space mode, enabling copy pause and resume (see Remarks).

        /LFSM:n[KMG] :: /LFSM, specifying the floor size in n [K:kilo,M:mega,G:giga] bytes.

::
:: Logging Options :
::
                 /L :: List only - don't copy, timestamp or delete any files.
                 /X :: report all eXtra files, not just those selected.
                 /V :: produce Verbose output, showing skipped files.
                /TS :: include source file Time Stamps in the output.
                /FP :: include Full Pathname of files in the output.
             /BYTES :: Print sizes as bytes.

                /NS :: No Size - don't log file sizes.
                /NC :: No Class - don't log file classes.
               /NFL :: No File List - don't log file names.
               /NDL :: No Directory List - don't log directory names.

                /NP :: No Progress - don't display percentage copied.
               /ETA :: show Estimated Time of Arrival of copied files.

          /LOG:file :: output status to LOG file (overwrite existing log).
         /LOG+:file :: output status to LOG file (append to existing log).

       /UNILOG:file :: output status to LOG file as UNICODE (overwrite existing log).
      /UNILOG+:file :: output status to LOG file as UNICODE (append to existing log).

               /TEE :: output to console window, as well as the log file.

               /NJH :: No Job Header.
               /NJS :: No Job Summary.

           /UNICODE :: output status as UNICODE.

::
:: Job Options :
::
       /JOB:jobname :: take parameters from the named JOB file.
      /SAVE:jobname :: SAVE parameters to the named job file
              /QUIT :: QUIT after processing command line (to view parameters).
              /NOSD :: NO Source Directory is specified.
              /NODD :: NO Destination Directory is specified.
                /IF :: Include the following Files.

::
:: Remarks :
::
       Using /PURGE or /MIR on the root directory of the volume formerly caused
       robocopy to apply the requested operation on files inside the System
       Volume Information directory as well. This is no longer the case; if
       either is specified, robocopy will skip any files or directories with that
       name in the top-level source and destination directories of the copy session.

       The modified files classification applies only when both source
       and destination filesystems support change timestamps (e.g., NTFS)
       and the source and destination files have different change times but are
       otherwise the same. These files are not copied by default; specify /IM
       to include them.

       The /DCOPY:E flag requests that extended attribute copying should be
       attempted for directories. Note that currently robocopy will continue
       if a directory's EAs could not be copied. This flag is also not included
       in /COPYALL.

       If either /IoMaxSize or /IoRate are specified, robocopy will enable
       copy file throttling (the purpose being to reduce system load).
       Both may be adjusted to allowable or optimal values; i.e., both
       specify desired copy parameters, but the system and robocopy are
       allowed to adjust them to reasonable/allowed values as necessary.
       If /Threshold is also used, it specifies a minimum file size for
       engaging throttling; files below that size will not be throttled.
       Values for all three parameters may be followed by an optional suffix
       character from the set [KMG] (kilo, mega, giga).

       Using /LFSM requests robocopy to operate in 'low free space mode'.
       In this mode, robocopy will pause whenever a file copy would cause the
       destination volume's free space to go below a 'floor' value, which
       can be explicitly specified by the LFSM:n[KMG] form of the flag.
       If /LFSM is specified with no explicit floor value, the floor is set to
       ten percent of the destination volume's size.
       Low free space mode is incompatible with /MT and /EFSRAW.

