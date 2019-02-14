# latex-pipeline-builder
Dockerfile for latex pipeline, uses Ubuntu image with **texlive-full** (because I'm not going to manage all the packages myself :).

Intended to use from bitbucket pipeline to automate build for latex projects.

Since bitbucket pipeline does not keep artifacts, you can use this image to generate your pdf files and then commit them to your repo.

The docker image is available here: https://hub.docker.com/r/botenvouwer/latex-pipeline-builder

This image gives you the default latex commands to compile tex files. But I also included my own bash script (see next section) to make things easy.

## How to use latex-builder
 This builder starts a pdf build based on tagname.
 
 A tagname should follow these rules "[tex file]-[version]".
 Tagname example: "mythesis-v1.1".
 ```
 [tex file] -> The name of the .tex file. The script looks in 
               local directory and in subdirectory like 
               "./mythesis.tex" and "./mythesis/mythesis.tex".
               
               If you have multiple dashes "-" in your
               tagname, the script will look for spaces and
               dashes. Example:

               Tagname: "my-thesis-v0.1"

               Script will look for:
               "./my thesis.tex", "./my-thesis.tex", "./my thesis/my thesis.tex", "my-thesis/my-thesis.tex"
               
               Note that: search is capital sensitive!
 ```

 ```
 [version] ->  The version of your .tex file. This will be 
               used to suffix the resulting pdf. The script 
               also adds a latex command to the tex file like
               "\newcommand{\PipelineBuildVersion}{v1.1}" 
               which you can use to show the version inside
               your document. 
               Use the following code to use version number
               safely in your tex document:
              
               %Put this in top of your latex file before you use the bellow command
               \ifx\PipelineBuildVersion\undefined
                   \newcommand{\YourVersion}{Latest}
               \else
                   \newcommand{\YourVersion}{\PipelineBuildVersion}
               \fi

               %Use this command where ever you want to use the version number
               \YourVersion
```

## Setup example for bitbucket pipeline
You can create a pdf for every tag you create or push. Setup a `bitbuckit-pipelines.yml` file in the root of your repo. And add this content:

```
image: botenvouwer/latex-pipeline-builder
pipelines:
  tags:
   '*':
      - step:
          name: Compile tex file and commit to repo
          script:
            - latex-builder "${BITBUCKET_TAG}"
            - git add -f '*.pdf'
            - git commit -m "Auto publish ${BITBUCKET_TAG}"
            - git push origin HEAD:master
```

In the above example the tagname is passed using `"${BITBUCKET_TAG}"` as argument. You should name your tag something like `myfile-v0.3` to build myfile.tex into myfile-v0.3.pdf. You could however fill in something else. Some examples:

Statically create file on every push to master:

```
image: botenvouwer/latex-pipeline-builder
pipelines:
  default:
    - step:
       script:
        - latex-builder "myfile-latest"
```

Use branch name as filename to create latest version for specific file. Note that you need to name your branches like your tex files without '.tex':

```
image: botenvouwer/latex-pipeline-builder
pipelines:
  default:
    - step:
       script:
        - latex-builder "$BITBUCKET_BRANCH-latest"
```

