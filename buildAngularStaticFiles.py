# build angular static 

import os, re, shutil

angularProjectPath = 'C:/inetpub/wwwroot/chat-app/ChatAppDev'
staticFilesPath = 'C:/inetpub/wwwroot/chat-app/DjangoHomeApp/DjangoHomeApp/static/angular-files'
htmlTemplatePath = 'C:/inetpub/wwwroot/chat-app/DjangoHomeApp/DjangoHomeApp/templates'

expression = "(main|styles|polyfills|scripts|runtime)[.].+[.](js|css)"

oldFileNames = []
newFileNames = []

print("")

os.chdir(angularProjectPath)
os.system("ng build --prod")

for file in os.listdir(f"{angularProjectPath}/dist"):
    if re.search(expression, file):
        newFileNames.append(re.search(expression, file).group(0))

htmlTemplate = open(f"{htmlTemplatePath}/index.html", "r")
htmlTemplateNew = open(f"{htmlTemplatePath}/index.html.temp", "w")

for line in htmlTemplate:
    if re.search(expression, line):
        fileFound = re.search(expression, line).group(0)
        fileKeywordFound = re.search(expression, line).group(1)
        for file in newFileNames:
            if fileKeywordFound in file:
                line = line.replace(fileFound, file)

    htmlTemplateNew.write(line)

htmlTemplate.close()
htmlTemplateNew.close()

os.remove(f"{htmlTemplatePath}/index.html")
os.rename(f"{htmlTemplatePath}/index.html.temp", f"{htmlTemplatePath}/index.html")

for file in os.listdir(staticFilesPath):
    try:
        os.remove(f"{staticFilesPath}/{file}")
    except:
        print(f"\nCan't delete {file}")

for file in newFileNames:
    shutil.move(f"{angularProjectPath}/dist/{file}", staticFilesPath)

print("\nStatic files built\n")