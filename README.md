# explace
*explace* is a python script that works on files that support tags syntax (e.g HTML, XML, HTML.ERB etc)
The script is written in **python 3.7** and tested on **Windows 10** only. The script works for UTF-8 encoded files.
No support is added for python 2.x and running it with said version has unknown behaviours.

To use the script, either to fetch data or to replace it. You need to place it in the root of your working directory.
It will span into the tree of that directory. **You must be able to call python in that directory**
To check if you can call python in your directory, go to your directory through cmd and type
`python --version`
The python version installed on your system will showed, else an error will appear.

To fetch the data; use
`python explace.py -f .html h2`
- .html is file extension, you can specify your own
- h2 is the tag to look for. Notice the absence of opening and closing tags.
This will extract everything written inside h2 elements from all files in the directory tree and save them to a text file

You may want to change the text in that file, but **DO NOT rename it or change other information in that file** if you intend to re-use for replacing

To replace the data, the script will use the file generated by it when used with flag `-f`.
`python explace.py -r h2`
- h2 is the tag whose content will be replaced, you may use one of your choice.
The files will made in a 'generated' folder and will maintain the original heirarchy.
