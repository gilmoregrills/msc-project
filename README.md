MSC PROJECT AND THESIS
======================

Directory Structure: 
--------------------

(Irrelevant for the moment while I refactor and tidy up the project)

- root
    - databases <_in gitignore_>
        - CIPIC
        - MIT
        - ARI
    - first-attempts <_initial investigation scripts_>
    - implementation <_implementation work master folder_>
    - other-work <_other people's work, as research/reference, gitignored_>
    - writing
        - specification
        - bibliography
        - thesis
            - abstract-acknowledgements
            - contents
            - introduction
            - literature-review
            - methodology-and-process
            - analysis-and-results
            - discussion
    - viva
     
The databases used are large, and inefficient to store on github. Any modified HRTF data will be stored inside the implementation folder and synced. 

All implementation work pertinent to the final handin is stored in the implementation folder, the thesis in the thesis subfolder, and the viva presentation/materials in the viva folder. 

The backup script uses rynsc to sync a copy of this folder to my Dropbox folder, which is then synced to Google drive using IFTTT. A slightly reworked version should also take a commit message argument and perform the full git add/commit/push sequence. 
