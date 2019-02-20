# latex-pipeline-builder v0.2
Dockerfile for latex pipeline, uses Ubuntu image with **texlive-full** (because I'm not going to manage all the packages myself :).

Intended to use from Bitbucket pipeline to automate build for latex projects. It gives you the bash command `tag-run` which will generate pdf files based on tag names. See subsections for more info.

Since Bitbucket pipeline does not keep artifacts, you can use this image to generate your pdf files and then commit them to your repo. If you want to push the resulting pdf files to another place (like Dropbox or Drive) extend this image and add the code to do it. Please contact me if you do. I would like to use it :).

The docker image is available here: https://hub.docker.com/r/botenvouwer/latex-pipeline-builder

## What does 'tag-run' do?

Basically it turns your `.tex` files into `.pdf` files based on the tag names in your git repo. So lets say you have the following tex files:

1. projectplan/project plan.tex
2. thesis/my thesis.tex
3. some-latex-file.tex

Now if you would have the following tags in your git repo:

1. project-plan-v0.1
2. project-plan-v0.2
3. some-latex-file-someversion

It would generate the following pdf files and push them to a branch called `publish`:

1. projectplan/project-plan-v0.1.pdf
2. projectplan/project-plan-v0.2.pdf
3. some-latex-file-someversion.pdf

As you can see the tag follows a pattern like `[file name]-[file version]`. Right now spaces will be turned into dashes '-', maybe I'll change that in the future. Your file can be in a subdirectory or in the root of your repo. 

It will actually checkout the tag and then generate with the tex file attached to the commit. So if you run this it will also generate all the history you already have. If the pdf already exists it will be skipped. If the tex file does not exist in latest master version it will be skipped.

### Inject version 
To make stuff more awesome, the `tag-run` script also injects the version into the tex file before compiling it. 

Use this by adding this somewhere in the top of your latex file:

```
\ifx\PipelineBuildVersion\undefined
  \newcommand{\FileVersion}{Latest}
\else
  \newcommand{\FileVersion}{\PipelineBuildVersion}
\fi
```

Now if you just compile locally or whatever you won't get an error since `PipelineBuildVersion` only exists when using this pipeline. Now to put a version number just use the `\FileVersion` command anywhere in your latex file. 

## How to use 'tag-run' (Bitbuckit)

In your Bitbuckit repo add a `bitbuckit-pipelines.yml` file (in the root). And add this content:

```
image: botenvouwer/latex-pipeline-builder:v0.2
pipelines:
  tags:
     '*':
        - step:
           name: Auto publish on tag name
           script:
             - tag-run
             - echo "Done!"
```

Optionally you can merge the resulting artifacts to master by adding a command to the script section.

